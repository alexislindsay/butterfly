# -*- mode: python ; coding: utf-8 -*-
# LexOS Voice Engine Build Spec
# This spec file compiles LexOS_TTS_Engine.py into a standalone .exe using PyInstaller.
# Ensure LexOS_TTS_Engine.py and LexOS_Symbolic_Voice_Tree.json are in the SAME directory as this file when building.

block_cipher = None

a = Analysis(
    ['LexOS_TTS_Engine.py'],  # Python script that drives the voice engine
    pathex=[],  # Leave empty to use current working directory
    binaries=[],
    datas=[('LexOS_Symbolic_Voice_Tree.json', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LexOS_Voice_Engine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False if you want no terminal window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LexOS_Voice_Engine'
)
