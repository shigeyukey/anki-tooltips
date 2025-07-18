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
    from ..forms.qt5.model_settings_ui import Ui_Settings
else:
    from ..forms.qt6.model_settings_ui import Ui_Settings


class ModelSettings(QDialog):
    """
    Dialog shown when clicking on "Tooltips..." in Manage Notetypes.
    """

    def __init__(self, mw, mid, callback):
        super().__init__(parent=mw)
        self.mw = mw
        self.mid = mid
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.callback = callback
        self.ui.tippyEnabled.stateChanged.connect(self.ui.generalGroup.setEnabled)
        self.ui.tippyEnabled.stateChanged.connect(self.ui.shortcutGroup.setEnabled)
        self.ui.saveButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def setupUi(
        self,
        tooltips_enabled: bool,
        show_on_front: bool,
        prev_shortcut: str,
        next_shortcut: str,
    ):
        self.ui.tippyEnabled.setChecked(tooltips_enabled)
        self.ui.generalGroup.setEnabled(tooltips_enabled)
        self.ui.shortcutGroup.setEnabled(tooltips_enabled)
        self.ui.showFrontCheckBox.setChecked(show_on_front)
        self.ui.prevShortcut.setKeySequence(QKeySequence(prev_shortcut))
        self.ui.nextShortcut.setKeySequence(QKeySequence(next_shortcut))
        self.ui.versionLabel.setText(f"Version: {version}")

    def accept(self):
        self.callback(
            self.ui.tippyEnabled.isChecked(),
            self.ui.showFrontCheckBox.isChecked(),
            self.ui.prevShortcut.keySequence().toString(),
            self.ui.nextShortcut.keySequence().toString(),
            self.mid,
        )

        super().accept()
