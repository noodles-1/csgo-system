# -*- mode: python ; coding: utf-8 -*-
import ultralytics

from PyInstaller.utils.hooks import collect_data_files

ultralytics_files = collect_data_files('ultralytics')

extra_files = [
    ('yolov8n.pt', '.'),
    ('controllers', 'controllers'),
    ('models', 'models'),
    ('trained_models', 'trained_models'),
    ('views', 'views'),
    ('videos', 'videos'),
    ('.env', '.'),
    ('yolov8n.pt', '.')
]

a = Analysis(
    ['views/view.py'],
    pathex=['C:/Users/Adriane/Documents/VSCode Python/csgo_ai/venv'],
    binaries=[],
    datas=ultralytics_files + extra_files,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='main',
)
