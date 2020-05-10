@echo off
title Turn Captive Into EXE
echo Running Installer
CD /D T:\Git\kennex_files\escape_game\captive\

pyinstaller --onefile -w -noupx captive.spec

CD /D T:\Git\kennex_files\escape_game\captive\dist
move *.exe %T:\Git\kennex_files\escape_game\captive\

CD /D T:\Git\kennex_files\escape_game\captive\

rmdir /S /Q "T:\Git\kennex_files\escape_game\captive\build"
rmdir /S /Q "T:\Git\kennex_files\escape_game\captive\dist"

"C:\Program Files\7-Zip\7z.exe" a "T:\Git\kennex_files\escape_game\captive\Captive_Game.zip" "T:\Git\kennex_files\escape_game\captive\captive.exe" "T:\Git\kennex_files\escape_game\captive\images\" "T:\Git\kennex_files\escape_game\captive\sounds\" "T:\Git\kennex_files\escape_game\captive\saves\" "T:\Git\kennex_files\escape_game\captive\steam_api64.dll" "T:\Git\kennex_files\escape_game\captive\steam_api64.lib" "T:\Git\kennex_files\escape_game\captive\steam_appid.txt" "T:\Git\kennex_files\escape_game\captive\SteamworksPy64.dll"









