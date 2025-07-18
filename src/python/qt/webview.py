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

from aqt import mw

from anki.utils import point_version
from aqt.gui_hooks import webview_will_set_content
from aqt.editor import Editor
from aqt.webview import WebContent
from ..config import tooltip_shortcut
from typing import Any

# This is required if you want to load any external resources into Anki's webviews
mw.addonManager.setWebExports(__name__, r"gui/icons|web/editor.*\.(js|css|svg)")


def on_webview_will_set_content(web_content: WebContent, context: Any):
    """
    Load JS and CSS files into Editor
    """
    if isinstance(context, Editor):
        addon_package = context.mw.addonManager.addonFromModule(__name__)
        base_path = f"/_addons/{addon_package}/web/editor"

        web_content.js.append(f"{base_path}/index.js")
        web_content.css.append(f"{base_path}/index.css")

        # Make some variables globally available
        web_content.head += f"""
<script>
    globalThis.tooltipShortcut = "{
        tooltip_shortcut.value.replace("Ctrl", "Control")
    }";
    globalThis.pointVersion = {point_version()};
</script>"""


def init_webview():
    webview_will_set_content.append(on_webview_will_set_content)
