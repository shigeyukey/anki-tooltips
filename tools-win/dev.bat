@REM #!/usr/bin/env bash
@REM declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
@REM set -e

@REM "$DIR/tools/build.sh"

@REM # Watch for changes in Add-on TypeScript code
@REM yarn --cwd "$DIR/src/ts" dev


REM filepath: /G:/among anki/_00_Github/anki-tooltips/tools-win/dev.bat


set "DIR=%~dp0.."
pushd %DIR%
set "DIR=%CD%"
popd

call "%DIR%\tools-win\build.bat"

REM Watch for changes in Add-on TypeScript code
yarn --cwd "%DIR%\src\ts" dev