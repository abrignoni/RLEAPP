# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../../rleappGUI.py'],
    pathex=['../scripts/artifacts'],
    binaries=[],
    datas=[
        ('../', 'scripts'),
        ('../../assets', 'assets'),
        ('../../leapp_functions', 'leapp_functions')
        ],
    hiddenimports=[
        'bencoding',
        'fitz',
        'ijson',
        'mailbox',
        'mammoth',
        'openpyxl',
        'PIL._tkinter_finder',
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
    a.binaries,
    a.datas,
    [],
    name='rleappGUI',
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
)
