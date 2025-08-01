# -*- mode: python ; coding: utf-8 -*-

# This is a PyInstaller spec file.
# It tells PyInstaller how to build your application into a single executable.

block_cipher = None

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[
                # Add any libraries that PyInstaller might miss.
                # For pandas and tkinter, these are common hidden imports.
                'pandas._libs.tslibs.base',
                'babel.numbers',
             ],
             hookspath=[],
             hooksconfig={},
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
          a.datas,
          [],
          name='ATSS_Scheduler', # This will be the name of your .exe file
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          # This creates a single windowed application, hiding the console window.
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
