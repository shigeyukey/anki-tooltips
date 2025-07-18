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

import re
from aqt import mw
from aqt.utils import tooltip
from anki.models import NotetypeDict
from .config import tooltips_enabled, prev_shortcut, next_shortcut, show_on_front

css_regex = re.compile(rf"""\n*@import\s+url\(["']?_anki-tooltips\.css["']?\);\n*""")
js_regex = re.compile(
    rf"""\n*<script src=["']?_anki-tooltips\.js["']?.*?>\s*<\/script>\n*"""
)


def insert_script(txt: str) -> str:
    """Inserts or replaces a custom-tailored <script> tag at the start of a template.
    Parameters:
        txt (str): Template HTML

    Returns:
        str: Template HTML with script inserted at the beginning
    """
    if replaced := re.sub(js_regex, "", txt) == txt:
        return re.sub(
            r"^\n*",
            """<script src="_anki-tooltips.js" """
            f"""data-prev-shortcut="{prev_shortcut.value}" """
            f"""data-next-shortcut="{next_shortcut.value}">"""
            """</script>\n\n""",
            txt,
        )
    else:
        return replaced


def update_model(model: NotetypeDict) -> None:
    """
    If tooltips are enabled, insert script and CSS into all templates of the notetype, else remove them.
    """

    if not tooltips_enabled.value:
        """
        Remove script and CSS from all card templates of this notetype, then return.
        """
        model["css"] = re.sub(css_regex, "", model["css"])

        for template in model["tmpls"]:
            template["qfmt"] = re.sub(js_regex, "", template["qfmt"])
            template["afmt"] = re.sub(js_regex, "", template["afmt"])

        tooltip(f"""Deactivated Tippy on notetype {model["name"]}.""")
        mw.col.models.update_dict(model)

        return

    if not show_on_front.value:
        """
        Remove script from front card templates of this notetype, then return.
        """
        for template in model["tmpls"]:
            template["qfmt"] = re.sub(js_regex, "", template["qfmt"])

        tooltip(f"""Updated Tippy on notetype {model["name"]}.""")
        mw.col.models.update_dict(model)

    """
    If the Style section doesn't already contain the CSS import, add it at the start.
    """
    if not re.search(css_regex, model["css"]):
        model["css"] = re.sub(
            r"^\n*", """@import url("_anki-tooltips.css");\n\n""", model["css"]
        )

    for template in model["tmpls"]:
        if show_on_front.value:
            template["qfmt"] = insert_script(template["qfmt"])
        template["afmt"] = insert_script(template["afmt"])

    tooltip(f"""Activated Tippy on notetype {model["name"]}.""")
    mw.col.models.update_dict(model)
