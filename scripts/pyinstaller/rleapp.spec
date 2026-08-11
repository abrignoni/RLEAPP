# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
   ['..\\..\\rleapp.py'],
   pathex=['..\\scripts\\artifacts'],
   binaries=[],
   datas=[('..\\', '.\\scripts')],
   hiddenimports=[
      # Artifacts are bundled as data files and imported from disk at runtime,
      # so PyInstaller's import-graph analysis never sees what they import.
      # Collect the packages
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
   name='rleapp',
   debug=False,
   bootloader_ignore_signals=False,
   strip=False,
   upx=True,
   upx_exclude=[],
   runtime_tmpdir=None,
   version='rleapp-file_version_info.txt',
   console=True )
