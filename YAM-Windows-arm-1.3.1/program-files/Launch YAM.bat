@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "STATUS=1"
set "EXE_PATH="

if exist "%~dp0YAM.exe" set "EXE_PATH=%~dp0YAM.exe"

if not defined EXE_PATH (
  for /d %%D in ("%~dp0Release\YAM-Windows-*") do (
    if exist "%%~fD\YAM.exe" (
      set "EXE_PATH=%%~fD\YAM.exe"
      goto run_found_exe
    )
  )
)

if not defined EXE_PATH if exist "%~dp0Release\dist\YAM.exe" set "EXE_PATH=%~dp0Release\dist\YAM.exe"
if not defined EXE_PATH if exist "%~dp0Release\dist\YAM\YAM.exe" set "EXE_PATH=%~dp0Release\dist\YAM\YAM.exe"
if not defined EXE_PATH if exist "%~dp0dist\YAM.exe" set "EXE_PATH=%~dp0dist\YAM.exe"
if not defined EXE_PATH if exist "%~dp0dist\YAM\YAM.exe" set "EXE_PATH=%~dp0dist\YAM\YAM.exe"

if defined EXE_PATH goto run_found_exe

where py >nul 2>nul
if not errorlevel 1 (
  py -3 --version >nul 2>nul
  if not errorlevel 1 goto run_py
)

where python >nul 2>nul
if not errorlevel 1 (
  python --version >nul 2>nul
  if not errorlevel 1 goto run_python
)

echo YAM.exe が見つからず、Python 3.10 以上も利用できません。
echo.
echo このフォルダにスタンドアロン版の YAM.exe が無い場合は、
echo 先に Python 3.10 以上をインストールしてください。
echo.
echo Python を入れた後に、もう一度 Launch YAM.bat を実行してください。
pause
exit /b 1

:run_found_exe
"%EXE_PATH%"
set "STATUS=!ERRORLEVEL!"
goto done

:run_py
call py -3 "%~dp0launch_yam.py"
set "STATUS=!ERRORLEVEL!"
goto done

:run_python
call python "%~dp0launch_yam.py"
set "STATUS=!ERRORLEVEL!"
goto done

:done
if not "%STATUS%"=="0" (
  echo.
  echo 起動に失敗しました。上のメッセージを確認してください。
  pause
)

exit /b %STATUS%
