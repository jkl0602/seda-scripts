call %~dp0Common\CommonEnv.bat

cd %ENGINE_PATH%
UnrealEditor.exe %GAME_PATH%\Elpis.uproject "/Game/Developers/JK/Levels/WPTest" -run=WorldPartitionBuilderCommandlet -SCCProvider=None -AllowCommandletRendering -builder=WorldPartitionHLODsBuilder