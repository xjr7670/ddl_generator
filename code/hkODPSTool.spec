# -*- mode: python -*-

block_cipher = None


a = Analysis(['hkODPSTool.py'],
             pathex=['G:\\ztesoft\\code\\hkODPSTool\\v2.1\\code'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5'],
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
          [],
          exclude_binaries=True,
          name='hkODPSTool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='iwhalecloud64x64.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='hkODPSTool')
