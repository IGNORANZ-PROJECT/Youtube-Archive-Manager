@echo off
setlocal
cd /d "%~dp0"

for %%F in ("%~dp0dist\YAM\YAM.exe" "%~dp0release\YAM\YAM.exe" "%~dp0YAM.exe") do (
  if exist "%%~fF" (
    "%%~fF"
    exit /b %errorlevel%
  )
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0launch_yam.py"
  set "STATUS=%errorlevel%"
  goto :done
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0launch_yam.py"
  set "STATUS=%errorlevel%"
  goto :done
)

echo Python 3.10 ^以上が必要です。
pause
exit /b 1

:done
if not "%STATUS%"=="0" (
  echo.
  echo 起動に失敗しました。
  pause
)

exit /b %STATUS%
