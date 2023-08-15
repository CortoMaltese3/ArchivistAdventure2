# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['code/main.py'],
             pathex=['/'],
             binaries=[],
             datas=[('audio/', 'audio/'),
                    ('graphics/', 'graphics/'),
                    ('maps/', 'maps/'),
                    ('src/', 'src/')],
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
          name='ArchivistAdventure2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          upx_compress=False,
          runtime_tmpdir=None,
          console=False,
          icon='graphics/icons/icon.ico')
