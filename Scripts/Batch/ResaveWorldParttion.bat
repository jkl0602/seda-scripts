call %~dp0Common\CommonEnv.bat
cd %ENGINE_PATH%

UnrealEditor-Cmd.exe %GAME_PATH%\Elpis.uproject "/Game/Covenant/BG/Level/Sector/LV_Sector_01_FoliageTest" -run=WorldPartitionBuilderCommandlet -SCCProvider=None -builder=WorldPartitionResaveActorsBuilder

pause