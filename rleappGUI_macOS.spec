# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['rleappGUI.py'],
    pathex=['scripts/artifacts'],
    binaries=[],
    datas=[('scripts/', 'scripts')],
    hiddenimports=[
        'bencoding',
        'fitz',
        'ijson',
        'mailbox',
        'mammoth',
        'openpyxl',
        'pillow_heif',
        'pypdf',
        'requests',
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
    icon='scripts/icon.icns',
    bundle_identifier='4n6.brigs.RLEAPP',
    version='1.1.2',
)
