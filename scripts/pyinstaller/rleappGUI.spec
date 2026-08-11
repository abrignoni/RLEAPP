# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
   ['..\\..\\rleappGUI.py'],
   pathex=['..\\scripts\\artifacts'],
   binaries=[],
   datas=[('..\\', '.\\scripts'), ('..\\..\\assets', '.\\assets')],
   hiddenimports=[
      # Artifacts are bundled as data files and imported from disk at runtime,
      # so PyInstaller's import-graph analysis never sees what they import.
      # hook-plugin_loader.py was meant to cover this but targets a bare
      # 'plugin_loader' module that no longer exists (it moved to
      # scripts.plugin_loader), so it never fires. Collect the packages
      # artifacts import wholesale; a missing submodule here is a startup
      # crash in the frozen build only. pdfminer is imported lazily by the
      # Kik artifact with a graceful fallback, so without it the frozen
      # build silently loses a capability dev runs have.
      *collect_submodules('leapp_functions'),
      *collect_submodules('PIL'),
      *collect_submodules('pdfminer'),
      'bs4',
      'bencoding',
      'fitz',
      'ijson',
      'mailbox',
      'mammoth',
      'openpyxl',
      'pillow_heif',
      'pypdf',
      'requests',
      'simplekml',
      'xlrd',
      ],
   hookspath=['.\\'],
   runtime_hooks=[],
   excludes=[],
   win_no_prefer_redirects=False,
   win_private_assemblies=False,
   cipher=block_cipher,
   noarchive=False)

pyz = PYZ(
   a.pure,
   a.zipped_data,
   cipher=block_cipher)

exe = EXE(
   pyz,
   a.scripts,
   a.binaries,
   a.zipfiles,
   a.datas,
   [],
   name='rleappGUI',
   debug=False,
   bootloader_ignore_signals=False,
   strip=False,
   upx=True,
   console=True,
   hide_console='hide-early',
   disable_windowed_traceback=False,
   upx_exclude=[],
   version='rleappGUI-file_version_info.txt',
   runtime_tmpdir=None )
