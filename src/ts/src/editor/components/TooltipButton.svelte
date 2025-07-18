<!--
Anki Tooltips
Copyright (C) Matthias Metelka (kleinerpirat) 2023 <https://github.com/kleinerpirat>
Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
@component
A button with shortcut that uses a Surrounder (class imported from "anki/surround")
to wrap selected content with `<a>` tags and changes its state depending on the current selection.

Components such as this one can be appended to the editor toolbar (@see index.ts)
@see {@link https://github.com/ankitects/anki/tree/main/ts/sveltelib/dynamic-slotting.ts}
-->
<script lang="ts">
    import { onMount } from "svelte/internal";
    import { addTooltipIcon, editTooltipIcon, emptyTooltipIcon } from "../assets/icons";
    import { bubbleSymbol } from "../lib";
    import {
        createTooltipAnchor,
        getCurrentSelection,
        selectionIsEmpty,
        wrapWordFromSelection,
    } from "../utils";
    import type { MatchType } from "@anki/domlib/surround";
    import type { FormattingNode } from "@anki/domlib/surround/tree";
    // @ts-ignore
    import * as NoteEditor from "anki/NoteEditor";
    // @ts-ignore
    import { getPlatformString } from "anki/shortcuts";
    // copy of original Anki component with runtime imports
    import Shortcut from "./anki-components/Shortcut.svelte";

    // not typing Surrounder as its available properties differ between Anki versions
    export let surrounder;

    /**
     * @see {@link https://github.com/ankitects/anki/blob/main/ts/editor/base.ts}
     * for all Svelte components currently exposed by Anki.
     */
    const { IconButton, WithState } = globalThis.components;

    export let keyCombination: string;

    const key = "tooltip";
    let disabled: boolean;

    let currentAnchor: HTMLAnchorElement;

    function isTooltipAnchor(element: HTMLElement | SVGElement) {
        return element.tagName === "A" && element.hasAttribute("data-tippy-content");
    }

    function matcher(
        element: HTMLElement | SVGElement,
        match: MatchType<string>,
    ): void {
        if (isTooltipAnchor(element)) {
            currentAnchor = element as HTMLAnchorElement;
            /**
             * We need to confirm the match either with .remove or .clear.
             * match.remove() would destroy the anchor, so we confirm the match with .clear,
             * which requires a callback as argument.
             */
            match.clear(() => {});
        }
    }

    /**
     * Surround selection with `<a class="new" data-tippy-content>` and dispatch event.
     */
    async function formatter(node: FormattingNode<string>): Promise<boolean> {
        const extension = node.extensions.find(
            (element: HTMLElement | SVGElement): boolean => isTooltipAnchor(element),
        );
        if (extension || !node.insideRange) {
            return false;
        }

        const anchor = createTooltipAnchor();
        node.range.toDOMRange().surroundContents(anchor);

        anchor.dispatchEvent(new Event("newTooltip", { bubbles: true }));

        return true;
    }

    const format = {
        matcher,
        merger: () => false,
        formatter,
    };

    async function updateStateFromActiveInput(): Promise<boolean> {
        return disabled
            ? false
            : surrounder.isSurrounded(globalThis.pointVersion <= 54 ? format : key);
    }

    /**
     * Either wraps selected text with a new <a> element or uses an existing one,
     * then dispatches a custom event to instantiate the TooltipEditor.
     *
     * @param active - Whether the caret is currently inside an anchor
     */
    async function createTooltip(active: boolean): Promise<void> {
        const selection = await getCurrentSelection();

        if (!selection) {
            return;
        }

        /**
         * Dispatch event from existing anchor
         */
        if (active) {
            currentAnchor.classList.add("new");
            currentAnchor.dispatchEvent(new Event("newTooltip", { bubbles: true }));
            return;
        }

        /**
         * If selection contains nothing but whitespace, insert anchor with bubble.
         */
        if (selectionIsEmpty(selection)) {
            if (wrapWordFromSelection(selection)) {
                return;
            }
            const range = selection.getRangeAt(0);
            const anchor = createTooltipAnchor(bubbleSymbol);
            range.insertNode(anchor);
            anchor.dispatchEvent(new Event("newTooltip", { bubbles: true }));
            return;
        }

        /**
         * @see formatter
         */
        surrounder.surround(globalThis.pointVersion <= 54 ? format : key);
    }

    const { focusedInput } = NoteEditor.context.get();
    /**
     * @deprecated Check if an `<anki-editable>` is focused or not.
     * On 2.1.55+ you can subscribe to Surrounder.active (@see onMount)
     */
    $: if (globalThis.pointVersion <= 54) {
        disabled = $focusedInput?.name !== "rich-text";
    }

    onMount(() => {
        if (globalThis.pointVersion >= 55) {
            surrounder.active.subscribe((value) => (disabled = !value));
            surrounder.registerFormat(key, format);
        }
    });
</script>

<WithState {key} update={updateStateFromActiveInput} let:state={active} let:updateState>
    <IconButton
        tooltip={`${active ? "Edit" : "Add"} Tooltip (${getPlatformString(
            keyCombination,
        )})`}
        {active}
        {disabled}
        on:click={(event) => {
            createTooltip(active);
            updateState(event);
        }}
    >
        {#if disabled}
            {@html emptyTooltipIcon}
        {:else if active}
            {@html editTooltipIcon}
        {:else}
            {@html addTooltipIcon}
        {/if}
    </IconButton>

    <Shortcut
        {keyCombination}
        on:action={(event) => {
            createTooltip(active);
            updateState(event);
        }}
    />
</WithState>
