# -*- mode: python -*-

block_cipher = None

# code ...
import OCC
import os
import ifcopenshell
folder_paths = []
occ_pkg_path = os.path.dirname(OCC.__file__)
casroot = os.path.join(occ_pkg_path, '..', '..', '..',
                              'Library', 'share', 'oce')
#casroot_paths = (casroot, os.path.join('app_module', 'casroot'))
casroot_paths = (casroot, 'casroot')
folder_paths.append(casroot_paths)

project_dir = os.getcwd()

assets_path = os.path.join(project_dir, 'assets')
icon_path = os.path.join(assets_path, 'gewoonhout.ico')
ifcopenshell_path = os.path.join(ifcopenshell.__file__)

datas_list = [
    (ifcopenshell_path, 'ifcopenshell'),
    (assets_path, 'assets'),
]

a = Analysis(
    ['app.py'],
    pathex=[project_dir],
    binaries=[],
    datas=datas_list,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='geWOONtool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon=[icon_path],
)