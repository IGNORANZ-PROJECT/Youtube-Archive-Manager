@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "PAUSE_ON_EXIT=1"
set "STATUS=1"

if not exist "%~dp0build_release.py" (
  echo build_release.py が見つかりません。
  goto finish
)

where py >nul 2>nul
if not errorlevel 1 goto run_py

where python >nul 2>nul
if not errorlevel 1 goto run_python

echo Python 3.10 ^以上が必要です。
goto finish

:run_py
call py -3 "%~dp0build_release.py"
set "STATUS=!ERRORLEVEL!"
goto done

:run_python
call python "%~dp0build_release.py"
set "STATUS=!ERRORLEVEL!"
goto done

:done
if "%STATUS%"=="0" (
  echo.
  echo ビルドが完了しました。
  echo Release フォルダ内の YAM-Windows-<version> を確認してください。
) else (
  echo.
  echo ビルドに失敗しました。
)

:finish
if "%PAUSE_ON_EXIT%"=="1" (
  echo.
  pause
)

exit /b %STATUS%
