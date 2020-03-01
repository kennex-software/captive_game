@echo off
title Turn Captive Into EXE
echo Running Installer
CD /D T:\Git\kennex_files\escape_game\captive\
pyinstaller --onefile -w captive.py control_panel.py credits.py gf.py inventory.py multiline_text.py objects.py puzzles.py room.py scale_points_list.py settings.py stable_items.py tv_channels.py whitespace.py

CD /D T:\Git\kennex_files\escape_game\captive\dist
move *.exe %T:\Git\kennex_files\escape_game\captive\

CD /D T:\Git\kennex_files\escape_game\captive\

del /S /Q T:\Git\kennex_files\escape_game\captive\*.spec
rmdir /S /Q "T:\Git\kennex_files\escape_game\captive\build"
rmdir /S /Q "T:\Git\kennex_files\escape_game\captive\dist"

"C:\Program Files\7-Zip\7z.exe" a "T:\Git\kennex_files\escape_game\captive\Captive_Game.zip" "T:\Git\kennex_files\escape_game\captive\captive.exe" "T:\Git\kennex_files\escape_game\captive\images\" "T:\Git\kennex_files\escape_game\captive\sounds\" "T:\Git\kennex_files\escape_game\captive\saves\"

