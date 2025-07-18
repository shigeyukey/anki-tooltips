# Anki Tooltips
# Copyright (C) Matthias Metelka (kleinerpirat) 2023 <https://github.com/kleinerpirat>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from anki.models import NotetypeId
from aqt import mw
from aqt.gui_hooks import models_did_init_buttons
from aqt.models import Models
from typing import Callable

from anki.lang import _

from ..config import tooltips_enabled, prev_shortcut, next_shortcut, show_on_front
from ..gui.dialogs.model_settings import ModelSettings
from ..utils import insert_script, update_model


def set_settings(
    enabled: bool,
    show_front: bool,
    prev: str,
    next: str,
    mid: NotetypeId,
) -> None:
    """
    Stores each setting in corresponding ModelConfig, then updates templates.
    """
    tooltips_enabled.value = enabled
    show_on_front.value = show_front
    prev_shortcut.value = prev
    next_shortcut.value = next

    update_model(mw.col.models.get(mid))


def on_tooltips_button_clicked(models: Models) -> None:
    current_row: int = models.form.modelsList.currentRow()
    mid: int = models.models[current_row].id

    tooltips_enabled.model_id = mid
    show_on_front.model_id = mid
    prev_shortcut.model_id = mid
    next_shortcut.model_id = mid

    dialog = ModelSettings(mw, mid, set_settings)

    dialog.setupUi(
        tooltips_enabled.value,
        show_on_front.value,
        prev_shortcut.value,
        next_shortcut.value,
    )

    return dialog.exec()


def init_tooltips_button(
    buttons: list[tuple[str, Callable[[], None]]], models: Models
) -> list[tuple[str, Callable[[], None]]]:
    buttons.append(
        (
            _("Tooltips..."),
            lambda: on_tooltips_button_clicked(models),
        )
    )
    return buttons


def init_models_button():
    models_did_init_buttons.append(init_tooltips_button)
