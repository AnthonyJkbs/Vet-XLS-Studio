@echo off
REM ============================================================
REM  Vet XLS Studio - Windows build script
REM  Produces dist\VetXLSStudio.exe then the setup exe via Inno Setup
REM ============================================================
setlocal

REM --- locate project root (two levels up from this file) ------
set ROOT=%~dp0..\..

cd /d "%ROOT%"

REM --- dependencies --------------------------------------------
pip install --upgrade pyinstaller pillow openpyxl || goto :err

REM --- build the application bundle ----------------------------
pyinstaller --noconfirm --clean packaging\windows\VetXLSStudio.spec || goto :err

REM --- build the installer (needs Inno Setup 6 installed) -------
set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo Inno Setup 6 not found - skipping installer.
    echo Get it free at https://jrsoftware.org/isdl.php
    goto :done
)
%ISCC% "%ROOT%\packaging\windows\VetXLSStudio.iss" || goto :err

:done
echo.
echo BUILD OK:
echo   app exe   : %ROOT%\dist\VetXLSStudio.exe
echo   installer : %ROOT%\dist\installer\VetXLSStudio-Setup-0.5.exe
exit /b 0

:err
echo BUILD FAILED
exit /b 1
