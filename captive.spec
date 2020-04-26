# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['captive.py', 'steamworks\\interfaces\\apps.py', 'steamworks\\interfaces\\friends.py', 'steamworks\\interfaces\\matchmaking.py', 'steamworks\\interfaces\\music.py', 'steamworks\\interfaces\\screenshots.py', 'steamworks\\interfaces\\users.py', 'steamworks\\interfaces\\userstats.py', 'steamworks\\interfaces\\utils.py', 'steamworks\\interfaces\\workshop.py', 'steamworks\\interfaces\\__init__.py', 'control_panel.py', 'credits.py', 'gf.py', 'inventory.py', 'multiline_text.py', 'objects.py', 'puzzles.py', 'room.py', 'scale_points_list.py', 'settings.py', 'stable_items.py', 'tv_channels.py', 'check_steam.py', 'whitespace.py', 'texture_gl.py', 'steamworks\\enums.py', 'steamworks\\exceptions.py', 'steamworks\\methods.py', 'steamworks\\structs.py', 'steamworks\\util.py', 'steamworks\\__init__.py'],
             pathex=['T:\\Git\\kennex_files\\escape_game\\captive'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='captive',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

"""             binaries=[('steam_api64.dll', '.'), ('SteamworksPy64.dll', '.'), ('steam_api64.lib', '.')],
             datas=[('steam_appid.txt', '.')],"""