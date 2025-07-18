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
-->

<script lang="ts">
    // @ts-ignore
    import { registerShortcut } from "anki/shortcuts";
    import { createEventDispatcher, onMount } from "svelte/internal";

    export let keyCombination: string;
    export let event: "keydown" | "keyup" | undefined = undefined;

    const dispatch = createEventDispatcher();

    onMount(() =>
        registerShortcut(
            (event: KeyboardEvent) => {
                event.preventDefault();
                dispatch("action", { originalEvent: event });
            },
            keyCombination,
            { event },
        ),
    );
</script>
