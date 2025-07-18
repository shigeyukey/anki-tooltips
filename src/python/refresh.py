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
import os
from glob import glob
from os import remove
from os.path import basename, dirname, realpath
from pathlib import Path

from typing import Callable

from aqt import mw
from aqt.gui_hooks import profile_did_open


def get_source(source_name: str) -> Callable[[], str]:
    """
    Returns compiled template js and css from add-on folder.
    """
    filepath = Path(dirname(realpath(__file__)), "web", source_name)

    with open(filepath, mode="r", encoding="utf-8") as file:
        return file.read().strip()


template_js = get_source("template/index.js")
template_css = get_source("template/index.css")


def refresh_media(*args) -> None:
    """
    Overwrites script files in collection.media with current version.
    This ensures the files get synced to AnkiWeb at all times.
    Executing this at startup should suffice for most development workflows.
    """
    if not (basepath := mw.col.media.dir()):
        return

    js_file = Path(basepath, "_anki-tooltips.js")
    css_file = Path(basepath, "_anki-tooltips.css")

    # Don't use Anki deletion API, otherwise files end up in Anki trash
    if os.path.exists(js_file):
        remove(js_file)

    if os.path.exists(css_file):
        remove(css_file)

    # Using redundant f-string to circumvent a bug that prevents filenames starting with a single low dash
    mw.col.media.write_data(f"_anki-tooltips.js", template_js.encode())
    mw.col.media.write_data(f"_anki-tooltips.css", template_css.encode())


def init_refresh():
    profile_did_open.append(refresh_media)
