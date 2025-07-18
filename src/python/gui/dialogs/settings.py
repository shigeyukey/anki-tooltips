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

from aqt import QDialog, QLayout, QKeySequence, qtmajor
from ...version import version

if qtmajor < 6:
    from ..forms.qt5.settings_ui import Ui_Settings
else:
    from ..forms.qt6.settings_ui import Ui_Settings


class Settings(QDialog):
    """
    Dialog shown when clicking on "Config" in the Add-ons window.
    """

    def __init__(self, parent, callback):
        super().__init__(parent=parent)

        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cb = callback
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def setupUi(self, tooltip_shortcut: str) -> None:
        self.ui.tippyShortcut.setKeySequence(QKeySequence(tooltip_shortcut))
        self.ui.versionInfo.setText(f"Version: {version}")

    def accept(self):
        tooltip_shortcut = self.ui.tippyShortcut.keySequence().toString()
        self.cb(tooltip_shortcut)
        super().accept()
