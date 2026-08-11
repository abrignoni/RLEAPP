# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['../../rleappGUI.py'],
    pathex=['scripts/artifacts'],
    binaries=[],
    datas=[('../', 'scripts'), ('../../assets', 'assets')],
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
    [],
    exclude_binaries=True,
    name='rleappGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='rleappGUI',
)
app = BUNDLE(
    coll,
    name='rleappGUI.app',
    icon='../../assets/icon.icns',
    bundle_identifier='4n6.brigs.RLEAPP',
    version='2026.2.0',
)
