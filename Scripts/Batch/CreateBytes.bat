call %~dp0Common\CommonEnv.bat
cd %ENGINE_PATH%

UnrealEditor-Cmd.exe %GAME_PATH%\Elpis.uproject -run=InitDataTableCommandlet -SCCProvider=None
pause