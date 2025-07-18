@REM #!/usr/bin/env bash
@REM declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
@REM set -e

@REM git clean -fdx "$DIR/dist"

@REM # Python
@REM rsync -rai "$DIR/src/python/" "$DIR/dist" --filter=":- $DIR/.gitignore" --delete-after

@REM # Qt5 GUI compatibility
@REM mkdir -p "$DIR/dist/gui/forms/qt5" "$DIR/dist/gui/forms/qt6"
@REM for filename in "$DIR/designer/"*'.ui'; do
@REM   python -m PyQt5.uic.pyuic "$filename" > "$DIR/dist/gui/forms/qt5/$(basename ${filename%.*})_ui.py"
@REM   python -m PyQt6.uic.pyuic "$filename" > "$DIR/dist/gui/forms/qt6/$(basename ${filename%.*})_ui.py"
@REM done

@REM # Typescript
@REM mkdir -p "$DIR/dist/web"
@REM yarn --cwd "$DIR/src/ts" && yarn --cwd "$DIR/src/ts" build

@REM echo 'Build successful!'

set "DIR=%~dp0.."
pushd %DIR%
set "DIR=%CD%"
popd

git clean -fdx "%DIR%\dist"

if not exist "%DIR%\dist" mkdir "%DIR%\dist"
robocopy "%DIR%\src\python" "%DIR%\dist" /E

@REM if not exist "%DIR%\dist\gui\forms\qt5" mkdir "%DIR%\dist\gui\forms\qt5"
if not exist "%DIR%\dist\gui\forms\qt6" mkdir "%DIR%\dist\gui\forms\qt6"

for %%F in ("%DIR%\designer\*.ui") do (
  echo Processing %%F
  python -m PyQt6.uic.pyuic "%%F" > "%DIR%\dist\gui\forms\qt6\%%~nF_ui.py"
  echo errorlevel: %ERRORLEVEL%
)

if not exist "%DIR%\dist\web" mkdir "%DIR%\dist\web"
yarn --cwd "%DIR%\src\ts" && yarn --cwd "%DIR%\src\ts" build

echo Build successful!