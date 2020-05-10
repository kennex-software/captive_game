# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['captive.py'],
             pathex=['T:\\Git\\kennex_files\\escape_game\\captive'],
             binaries=[],
             datas=[('T:\\Git\\kennex_files\\escape_game\\captive\\*.py', '.'),
                    ('T:\\Git\\kennex_files\\escape_game\\captive\\steamworks\\*.py', 'steamworks'),
                    ('T:\\Git\\kennex_files\\escape_game\\captive\\steamworks\\interfaces\\*.py', 'interfaces'),
                    ('T:\\Git\\kennex_files\\escape_game\\captive\\steam_appid.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.binaries = a.binaries + [('steam_api64.dll', 'T:\\Git\\kennex_files\\escape_game\\captive\\steam_api64.dll', 'BINARY'),
                           ('steam_api64.lib', 'T:\\Git\\kennex_files\\escape_game\\captive\\steam_api64.lib', 'BINARY'),
                           ('SteamworksPy64.dll', 'T:\\Git\\kennex_files\\escape_game\\captive\\SteamworksPy64.dll', 'BINARY')]
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

