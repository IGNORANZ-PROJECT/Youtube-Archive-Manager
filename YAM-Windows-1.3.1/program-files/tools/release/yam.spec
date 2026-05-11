# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

from PyInstaller.building.build_main import Analysis, COLLECT, EXE, PYZ
from PyInstaller.utils.hooks import collect_submodules

if sys.platform == "darwin":
    from PyInstaller.building.osx import BUNDLE


BASE_DIR = Path(SPECPATH).parent.parent
ICON_FILE = os.environ.get("YAM_ICON_FILE", "").strip() or None
APP_VERSION = os.environ.get("YAM_APP_VERSION", "0.0.0").strip() or "0.0.0"

def unique_paths(paths):
    seen = set()
    result = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result

def find_runtime_binary(name):
    candidates = []
    for root in unique_paths(
        [
            Path(sys.base_prefix),
            Path(sys.base_exec_prefix),
            Path(sys.executable).resolve().parent,
        ]
    ):
        candidates.extend([root / name, root / "DLLs" / name, root / "Lib" / "site-packages" / name])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None

extra_binaries = []
if sys.platform.startswith("win"):
    runtime_binary_names = [
        f"python{sys.version_info.major}{sys.version_info.minor}.dll",
        "python3.dll",
        "VCRUNTIME140.dll",
        "VCRUNTIME140_1.dll",
        "MSVCP140.dll",
        "_socket.pyd",
        "select.pyd",
        "_ssl.pyd",
        "_hashlib.pyd",
        "_ctypes.pyd",
        "_decimal.pyd",
        "_bz2.pyd",
        "_lzma.pyd",
        "unicodedata.pyd",
        "libcrypto-3.dll",
        "libssl-3.dll",
        "libffi-9.dll",
        "libffi-8.dll",
        "libffi-7.dll",
    ]
    for name in runtime_binary_names:
        binary_path = find_runtime_binary(name)
        if binary_path is not None:
            extra_binaries.append((str(binary_path), "."))

def unique_strings(values):
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result

package_hiddenimports = []
for package_name in ["flask", "jinja2", "werkzeug", "click", "itsdangerous", "markupsafe"]:
    package_hiddenimports.extend(collect_submodules(package_name))

datas = [
    (str(BASE_DIR / "templates"), "templates"),
    (str(BASE_DIR / "static"), "static"),
    (str(BASE_DIR / "assets"), "assets"),
]
binaries = extra_binaries
hiddenimports = unique_strings(["app"] + package_hiddenimports)

a = Analysis(
    [str(BASE_DIR / "launch_yam.py")],
    pathex=[str(BASE_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name="YAM",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=ICON_FILE,
    contents_directory="_internal",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="YAM",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="YAM.app",
        icon=ICON_FILE,
        bundle_identifier="app.ignoranz.yam",
        info_plist={
            "CFBundleDisplayName": "YAM",
            "CFBundleName": "YAM",
            "CFBundleShortVersionString": APP_VERSION,
            "CFBundleVersion": APP_VERSION,
            "NSHighResolutionCapable": True,
        },
    )
