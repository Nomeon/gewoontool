# -*- mode: python -*-

block_cipher = None

# code ...
import OCC
import os
folder_paths = []
occ_pkg_path = os.path.dirname(OCC.__file__)
casroot = os.path.join(occ_pkg_path, '..', '..', '..',
                              'Library', 'share', 'oce')
#casroot_paths = (casroot, os.path.join('app_module', 'casroot'))
casroot_paths = (casroot, 'casroot')
folder_paths.append(casroot_paths)

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/DN51/Anaconda3/envs/gewoontool/Lib/site-packages/ifcopenshell', 'ifcopenshell/'), ('I:/GHO/00 Algemeen/ICT/Applicaties/IFC Tools/Installatiebestanden/wkhtmltopdf', 'wkhtmltopdf/'), ('I:/GHO/00 Algemeen/ICT/Applicaties/IFC Tools/Dev/geWOONtool/gewoontool/assets', 'assets/')],
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
	icon=['I:/GHO/00 Algemeen/ICT/Applicaties/IFC Tools/Dev/geWOONtool/gewoontool/assets/gewoonhout.ico'],
)