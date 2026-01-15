call %~dp0Common\CommonEnv.bat

%ENGINE_BATCH_PATH%\RunUAT BuildCookRun -project=%GAME_PATH%\Elpis.uproject -noP4 -platform=Win64 -clientconfig=Shipping -serverconfig=Shipping -clean -build -compile -cook -stage -compressed -pak -iterate -maps=/Game/Covenant/BG/Level/Sector/LV_Sector_01.umap -archive -archivedirectory=C:\JK\tmp\build