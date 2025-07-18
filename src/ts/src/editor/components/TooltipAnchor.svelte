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
A dynamic HTMLAnchorElement that serves as a reference for the tippy.js tooltip,
which in turn hosts the TooltipEditor component.
-->
<script context="module" lang="ts">
    export enum TooltipState {
        EDIT,
        RECYCLE,
        SCRAP,
        ACCEPT,
    }
</script>

<script lang="ts">
    import tippy from "tippy.js";
    import type { Instance } from "tippy.js";
    import { createEventDispatcher, onDestroy } from "svelte/internal";
    import { bubbleSymbol } from "../lib";
    import { encodeAttribute, decodeAttribute } from "../utils";

    import TooltipEditor, { EditorButton } from "./TooltipEditor.svelte";

    export let editable: HTMLElement;
    export let anchorContent: string;
    export let tooltipContent: string;

    const dispatch = createEventDispatcher();

    let anchor: HTMLAnchorElement;

    /**
     * Determines what's left behind after destruction.
     */
    let state = TooltipState.EDIT;
    /**
     * Which TooltipEditor button is currently hovered, if any.
     */
    let hoveredButton: EditorButton;

    /**
     * The contentEditable attribute messes up Svelte component communication,
     * so you should remove it while working with Svelte inside <anki-editable>
     * (this probably applies to other frameworks too).
     */
    editable.removeAttribute("contentEditable");

    function createTooltip(anchor: HTMLAnchorElement) {
        /**
         * Tippy.js doesn't offer Svelte components, so we need to insert
         * our TooltipEditor component manually into the tippy instance via this container.
         */
        const container = document.createElement("div");
        /**
         * TooltipEditor instance to be appended to a Tippy.js instance.
         */
        const editor = new TooltipEditor({
            target: container,
            props: {
                content: tooltipContent,
            },
        });

        /**
         * Tippy.js instance that contains the TooltipEditor.
         *
         * As this is appended to <anki-editable>, we can use all of Anki's formatting
         * features and paste media into the TooltipEditor.
         */
        tippy(anchor, {
            inertia: true,
            allowHTML: true,
            interactive: true,
            showOnCreate: true,
            appendTo: editable,
            placement: "bottom",
            animation: "scale",
            trigger: "manual",
            theme: "input",
            duration: 180,

            onCreate(instance) {
                // Insert TooltipEditor into tippy instance
                instance.setContent(container);
                setupMessageHandlers(editor, instance);
            },
            onShown() {
                editor.focusInput();
            },
            onHidden(instance) {
                editor.$destroy();
                instance.destroy();
            },
            onDestroy() {
                editable.style.removeProperty("padding-bottom");
                dispatch("destroyComponent");
            },
        });
    }

    /**
     * Workaround to provide reactivity between TooltipEditor and TooltipAnchor.
     */
    function setupMessageHandlers(editor: TooltipEditor, instance: Instance) {
        editor.$on("input", ({ detail }) => (tooltipContent = detail.content));
        /**
         * Ensure absolutely positioned tippy instance is visible inside field
         */
        editor.$on("height", ({ detail }) =>
            editable.style.setProperty("padding-bottom", `${detail.height + 40}px`),
        );
        /**
         * Button hovered inside TooltipEditor
         */
        editor.$on(
            "hoveredButton",
            ({ detail }) => (hoveredButton = detail.hoveredButton),
        );
        /**
         * Button clicked inside TooltipEditor
         */
        editor.$on("action", ({ detail }) => {
            state = detail.state as TooltipState;
            instance.hide();
        });
    }

    onDestroy(() => {
        switch (state) {
            case TooltipState.SCRAP:
                if (anchorContent != bubbleSymbol) {
                    anchor.insertAdjacentHTML("afterend", anchorContent);
                }
                break;
            case TooltipState.RECYCLE:
                anchor.insertAdjacentHTML(
                    "afterend",
                    `${anchorContent != bubbleSymbol ? anchorContent : ""}${
                        tooltipContent ? " " + tooltipContent : ""
                    }`,
                );
                break;
            default:
                anchor.insertAdjacentHTML(
                    "afterend",
                    tooltipContent.trim() != ""
                        ? `<a class="edited" data-tippy-content="${encodeAttribute(
                              tooltipContent,
                          )}">${anchorContent}</a>`
                        : anchorContent != bubbleSymbol
                        ? anchorContent
                        : "",
                );
        }
        // Attribute was removed at beginning of component lifecycle
        editable.setAttribute("contentEditable", "");
    });
</script>

<!-- svelte-ignore a11y-missing-attribute -->
<a
    bind:this={anchor}
    class="active"
    class:recycle-preview={hoveredButton == EditorButton.RECYCLE}
    class:scrap-preview={hoveredButton == EditorButton.SCRAP}
    class:bubble={anchorContent == bubbleSymbol}
    data-tippy-content={encodeAttribute(tooltipContent)}
    use:createTooltip
>
    {@html anchorContent}
</a>
{#if hoveredButton == EditorButton.RECYCLE}
    <span class="preview transient">
        {@html decodeAttribute(tooltipContent)}
    </span>
{/if}

<style lang="scss">
    /* 
     * Styles that should apply to all tooltip anchors in the field are selected with
     * the :global modifier. It prevents selectors from getting scoped to the component.
     */
    :global(a[data-tippy-content]) {
        cursor: pointer;
        position: relative;
        text-decoration: underline dotted var(--fg-link, var(--link));

        &:hover {
            text-decoration-style: solid;
        }
        &.recycle-preview,
        &.scrap-preview {
            text-decoration-color: var(--fg-disabled, var(--disabled));
        }
        &.bubble {
            &.recycle-preview {
                display: none;
            }
            &.scrap-preview {
                opacity: 0.4;
            }
        }
    }
    .preview {
        color: var(--fg-disabled, var(--disabled));
    }
</style>
