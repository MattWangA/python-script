# -*- mode: python -*-

block_cipher = None

import os
resources_dir = os.environ['PYTHON_RESOURCES_DIR']

a = Analysis(['main.py'],
             pathex=[resources_dir, 'lib'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['Tkinter', 'PIL', 'optparse', 'doctest', 'difflib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GenerateTopAPACCallsTemplate',
          debug=False,
          strip=False,
          upx=True,
          console=True )
