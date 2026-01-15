call %~dp0Common\CommonEnv.bat

cd %ENGINE_PATH%
UnrealEditor.exe %GAME_PATH%\Elpis.uproject /Game/Covenant/BG/Level/Sector/LV_Sector_01_FoliageTest -game
rem -Windowed -ResX=1280 -ResY=720