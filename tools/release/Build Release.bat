@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0build_release.py"
  set "STATUS=%errorlevel%"
  goto :done
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0build_release.py"
  set "STATUS=%errorlevel%"
  goto :done
)

echo Python 3.10 ^以上が必要です。
pause
exit /b 1

:done
if not "%STATUS%"=="0" (
  echo.
  echo ビルドに失敗しました。
  pause
)

exit /b %STATUS%
