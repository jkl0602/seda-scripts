call %~dp0Common\CommonEnv.bat

cd %ENGINE_PATH%
UnrealEditor.exe %GAME_PATH%\Elpis.uproject -run=WorldPartitionConvertCommandlet "/Game/Developers/USER/MatTest.umap" -SCCProvider=None -AllowCommandletRendering

pause