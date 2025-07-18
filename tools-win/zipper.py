import os
import subprocess
import shutil
from pathlib import Path

def main():
    DIR = Path(__file__).resolve().parent.parent

    zipped_dir = DIR / "zipped"
    dist_dir = DIR / "dist"
    build_sh = DIR / "tools-win" / "build.bat"
    addon_zip = zipped_dir / "anki-tooltips.ankiaddon"

    zipped_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([str(build_sh)], shell=True, check=True)

    if addon_zip.exists():
        addon_zip.unlink()
    shutil.make_archive(str(addon_zip.with_suffix('')), 'zip', root_dir=dist_dir)

    zip_path = addon_zip.with_suffix('.zip')
    if zip_path.exists():
        zip_path.rename(addon_zip)

if __name__ == "__main__":
    main()