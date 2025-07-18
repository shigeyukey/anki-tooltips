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

from typing import Union, Optional

from aqt import mw, QDialog, QLayout, QKeySequence, qtmajor
from aqt.addons import AddonsDialog
from aqt.gui_hooks import addons_dialog_will_show

from ..gui.dialogs.settings import Settings
from ..config import tooltip_shortcut
from ..version import version


def set_settings(shortcut: str) -> None:
    tooltip_shortcut.value = shortcut


addons_current: Optional[AddonsDialog] = None


def save_addons_window(addons) -> None:
    global addons_current
    addons_current = addons


def show_settings() -> None:
    dialog = Settings(addons_current, set_settings)

    dialog.setupUi(
        tooltip_shortcut.value,
    )
    return dialog.open()


def init_config_button() -> None:
    addons_dialog_will_show.append(save_addons_window)
    mw.addonManager.setConfigAction(__name__, show_settings)
