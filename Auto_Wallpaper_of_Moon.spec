# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Auto_Wallpaper_of_Moon.py'],
             pathex=['F:\\Users\\QQT\\Documents\\Python Projects\\Auto_Wallpaper_spider'],
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
          name='Auto_Wallpaper_of_Moon',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , version='version_file_moon.txt', icon='F:\\Users\\QQT\\Documents\\Python Projects\\Auto_Wallpaper_spider\\icon\\moon.ico')
