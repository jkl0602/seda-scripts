call %~dp0Common\CommonEnv.bat

%ENGINE_PATH%\\Build\\BatchFiles\\Build ElpisEditor Win64 Development -Project=%GAME_PATH%\\Elpis.uproject -TargetType=Editor -Progress -NoHotReloadFromIDE -WaitMutex -FromMsBuild