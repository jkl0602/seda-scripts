call %~dp0Common\CommonEnv.bat

set PAK_PATH=C:\Users\USER\Downloads\291\Elpis\Content\Paks
set FILE=%PAK_PATH%\pakchunk0-Windows.pak
%ENGINE_PATH%\Binaries\Win64\UnrealPak %FILE% -Extract %PAK_PATH%\Unpak