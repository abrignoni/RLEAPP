# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['../../rleapp.py'],
    pathex=['../scripts/artifacts'],
    binaries=[],
    datas=[('../', 'scripts')],
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
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='rleapp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
