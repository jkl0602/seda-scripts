call %~dp0Common\CommonEnv.bat

%ENGINE_BATCH_PATH%\RunUAT BuildCookRun -project=%GAME_PATH%\Elpis.uproject -noP4 -platform=Win64 -clientconfig=Development -serverconfig=Development -clean -build -compile -cook -stage -compressed -pak -archive -archivedirectory=C:\JK\tmp\build