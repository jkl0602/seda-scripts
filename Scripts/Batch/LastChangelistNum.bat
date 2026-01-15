set GAME_PATH=C:\JK\src

cd %GAME_PATH%
p4 -u program01 changes -m 1 -s submitted > version.txt

pause