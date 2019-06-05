@echo off
:-------------------------------------
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)
if '%errorlevel%' NEQ '0' (
    echo [Info] Waiting for administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------
echo Python script folder location where pyuic4.exe is located:
set /p pythonScriptFolderLocation="Path: "
echo.
echo Path to .ui file:
set /p uiFileName="Path: "
echo Name of compiled file:
set /p compiledFileName="Name: "
CD /D %pythonScriptFolderLocation%
pyuic5.exe %uiFileName% > %~dp0%compiledFileName%
ECHO Finished Compiling
pause