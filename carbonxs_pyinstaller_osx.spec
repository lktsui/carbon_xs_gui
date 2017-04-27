# -*- mode: python -*-

block_cipher = None


a = Analysis(['CarbonXS_GUI.py'],
             pathex=['/Users/rune_devros/Documents/carbon_xs_gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='CarbonXS_GUI',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='CarbonXS_GUI')
app = BUNDLE(coll,
             name='CarbonXS_GUI.app',
             icon=None,
             bundle_identifier=None,
             info_plist={'CFBundleVersion':'1.3.0',
                         'CFBundleShortVersionString':'1.3.0',
                         'NSHighResolutionCapable':'True',
                         'LSMinimumSystemVersion':'10.10.0',
             }

             )
