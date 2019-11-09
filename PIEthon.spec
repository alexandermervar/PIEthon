# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PIEthon.py'],
             pathex=['C:\\Users\\brfunk\\Documents\\PIEthon'],
             binaries=[],
             datas=[('resources/chromedriver.exe', 'resources'), ('resources/iu_stylesheet.qss', 'resources'), ('resources/down_arrow_3.png', 'resources'), ('resources/PIEcon.png', 'resources'), ('resources/PIEcon.ico', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [('v', None, 'OPTION')],
          exclude_binaries=True,
          name='PIEthon',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='resources\\PIEcon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PIEthon')
