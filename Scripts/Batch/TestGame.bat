call %~dp0Common\CommonEnv.bat

cd %ENGINE_PATH%
UnrealEditor.exe %GAME_PATH%\Elpis.uproject -game -trace=default,default,counter,stats,file,loadtime,assetloadtime,task
rem -Windowed -ResX=1280 -ResY=720