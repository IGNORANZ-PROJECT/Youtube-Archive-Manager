import os
import platform
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent.parent
RELEASE_ROOT_DIR = BASE_DIR / "Release"
DIST_DIR = RELEASE_ROOT_DIR / "dist"
BUILD_DIR = RELEASE_ROOT_DIR / "build"
BUILD_ASSETS_DIR = RELEASE_ROOT_DIR / "build-assets"
SPEC_PATH = SCRIPT_DIR / "yam.spec"
ICON_SOURCE_PATH = BASE_DIR / "assets" / "icon.png"
SPEC_TEMPLATE = textwrap.dedent(
    """\
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
    hiddenimports = unique_strings(
        [
            "app",
            "socket",
            "_socket",
            "ssl",
            "_ssl",
            "hashlib",
            "_hashlib",
            "select",
            "multiprocessing",
            "multiprocessing.context",
            "multiprocessing.reduction",
            "multiprocessing.util",
            "_multiprocessing",
            "_overlapped",
            "_queue",
            "pyexpat",
            "unicodedata",
        ]
        + package_hiddenimports
    )

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
    """
)
PROGRAM_FILE_PATHS = [
    ".gitignore",
    "app.py",
    "launch_yam.py",
    "requirements.txt",
    "Launch YAM.bat",
    "Launch YAM.command",
    "assets",
    "static",
    "templates",
    "tools/release",
]
IGNORED_SOURCE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "__pycache__",
    ".git",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    ".pyinstaller",
}
IGNORED_SOURCE_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def print_step(message: str) -> None:
    print(f"[YAM Build] {message}", flush=True)


def platform_label() -> str:
    if sys.platform == "darwin":
        return "macOS"
    if sys.platform.startswith("win"):
        return "Windows"
    return sys.platform


def platform_arch_label() -> str:
    return platform.machine() or "unknown"


def load_app_version() -> str:
    app_path = BASE_DIR / "app.py"
    match = re.search(r'__version__\s*=\s*"([^"]+)"', app_path.read_text(encoding="utf-8"))
    return match.group(1) if match else "0.0.0"


def release_folder_name(version: str) -> str:
    return f"YAM-{platform_label()}-{version}"


def ensure_spec_file() -> None:
    current = None
    if SPEC_PATH.exists():
        try:
            current = SPEC_PATH.read_text(encoding="utf-8")
        except OSError:
            current = None
    if current == SPEC_TEMPLATE:
        return
    SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(SPEC_TEMPLATE, encoding="utf-8")
    action = "updated" if current is not None else "generated"
    print_step(f"spec {action}: {SPEC_PATH}")


def ensure_clean_artifacts() -> None:
    for path in (DIST_DIR, BUILD_DIR, BUILD_ASSETS_DIR, RELEASE_ROOT_DIR / ".pyinstaller", RELEASE_ROOT_DIR / "packages"):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
    for path in RELEASE_ROOT_DIR.glob(f"YAM-{platform_label()}-*"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    for path in (DIST_DIR, BUILD_DIR, BUILD_ASSETS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def create_icns_icon(target_path: Path) -> Optional[Path]:
    if sys.platform != "darwin" or not ICON_SOURCE_PATH.exists() or Image is None:
        return None

    image = Image.open(ICON_SOURCE_PATH)
    image.save(target_path, format="ICNS")
    return target_path if target_path.exists() else None


def create_ico_icon(target_path: Path) -> Optional[Path]:
    if not sys.platform.startswith("win") or not ICON_SOURCE_PATH.exists() or Image is None:
        return None

    image = Image.open(ICON_SOURCE_PATH)
    image.save(
        target_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    return target_path if target_path.exists() else None


def prepare_icon_file() -> Optional[Path]:
    if not ICON_SOURCE_PATH.exists():
        return None

    try:
        if sys.platform == "darwin":
            return create_icns_icon(BUILD_ASSETS_DIR / "YAM.icns")
        if sys.platform.startswith("win"):
            return create_ico_icon(BUILD_ASSETS_DIR / "YAM.ico")
    except Exception as error:
        print_step(f"アイコン変換に失敗したため既定アイコンで続行します: {error}")
    return None


def build_env(icon_file: Optional[Path], version: str) -> dict[str, str]:
    env = os.environ.copy()
    env["YAM_APP_VERSION"] = version
    env["PYINSTALLER_CONFIG_DIR"] = str(RELEASE_ROOT_DIR / ".pyinstaller")
    if icon_file is not None:
        env["YAM_ICON_FILE"] = str(icon_file)
    return env


def smoke_check_env(stage_dir: Path) -> dict[str, str]:
    env = os.environ.copy()

    for key in list(env):
        upper = key.upper()
        if upper.startswith("PYTHON") or upper in {"VIRTUAL_ENV", "__PYVENV_LAUNCHER__"}:
            env.pop(key, None)

    if sys.platform.startswith("win"):
        system_root = env.get("SystemRoot") or env.get("WINDIR") or r"C:\Windows"
        windir = env.get("WINDIR") or system_root
        path_entries = [
            str(stage_dir),
            str(stage_dir / "_internal"),
            os.path.join(system_root, "System32"),
            system_root,
            os.path.join(system_root, "System32", "Wbem"),
            os.path.join(system_root, "System32", "WindowsPowerShell", "v1.0"),
            windir,
        ]
        env["PATH"] = os.pathsep.join(entry for entry in path_entries if entry)

    return env


def run_pyinstaller(icon_file: Optional[Path], version: str) -> None:
    print_step("PyInstaller でスタンドアロン版をビルドしています...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--distpath",
            str(DIST_DIR),
            "--workpath",
            str(BUILD_DIR),
            str(SPEC_PATH),
        ],
        cwd=BASE_DIR,
        env=build_env(icon_file, version),
        check=True,
    )


def find_built_target() -> Path:
    if sys.platform == "darwin":
        app_bundle = DIST_DIR / "YAM.app"
        if app_bundle.exists():
            return app_bundle
    folder = DIST_DIR / "YAM"
    if folder.exists():
        return folder
    exe_path = DIST_DIR / "YAM.exe"
    if exe_path.exists():
        return exe_path
    raise FileNotFoundError("PyInstaller の出力が見つかりません。")


def copytree_contents(source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for child in source_dir.iterdir():
        destination = target_dir / child.name
        if child.is_dir():
            shutil.copytree(child, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(child, destination)


def optional_doc_path(*relative_candidates: str) -> Optional[Path]:
    for relative_path in relative_candidates:
        candidate = BASE_DIR / relative_path
        if candidate.exists():
            return candidate
    return None


def copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignore_source_junk)
    else:
        if should_skip_path(source):
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def should_skip_path(path: Path) -> bool:
    return path.name in IGNORED_SOURCE_NAMES or path.suffix.lower() in IGNORED_SOURCE_SUFFIXES


def ignore_source_junk(_dir_path: str, names: list[str]) -> list[str]:
    ignored_names: list[str] = []
    for name in names:
        if should_skip_path(Path(name)):
            ignored_names.append(name)
    return ignored_names


def cleanup_release_junk() -> None:
    for pattern in (".DS_Store", "Thumbs.db", "desktop.ini"):
        for path in RELEASE_ROOT_DIR.rglob(pattern):
            if path.is_file():
                path.unlink(missing_ok=True)


def stage_program_files(stage_dir: Path) -> None:
    source_dir = stage_dir / "program-files"
    source_dir.mkdir(parents=True, exist_ok=True)

    for relative_path in PROGRAM_FILE_PATHS:
        source_path = BASE_DIR / relative_path
        if not source_path.exists():
            continue
        copy_path(source_path, source_dir / relative_path)


def stage_release_bundle(built_target: Path, version: str) -> Path:
    stage_dir = RELEASE_ROOT_DIR / release_folder_name(version)
    if stage_dir.exists():
        shutil.rmtree(stage_dir, ignore_errors=True)
    stage_dir.mkdir(parents=True, exist_ok=True)

    if built_target.is_dir() and built_target.suffix.lower() == ".app":
        shutil.copytree(built_target, stage_dir / built_target.name, dirs_exist_ok=True)
    elif built_target.is_dir():
        copytree_contents(built_target, stage_dir)
    else:
        shutil.copy2(built_target, stage_dir / built_target.name)

    readme_path = optional_doc_path("Release/README.md", "README.md")
    if readme_path is not None:
        shutil.copy2(readme_path, stage_dir / "README.md")

    license_path = optional_doc_path("Release/LICENSE", "LICENSE")
    if license_path is not None:
        shutil.copy2(license_path, stage_dir / "LICENSE")

    stage_program_files(stage_dir)
    return stage_dir


def python_runtime_filename() -> str:
    return f"python{sys.version_info.major}{sys.version_info.minor}.dll"


def verify_windows_bundle(stage_dir: Path) -> None:
    if not sys.platform.startswith("win"):
        return

    runtime_dir = stage_dir / "_internal"
    required_names = [
        "YAM.exe",
        "_internal",
    ]
    missing = [name for name in required_names if not (stage_dir / name).exists()]
    runtime_missing = [
        name
        for name in ["base_library.zip", "_socket.pyd", "select.pyd", python_runtime_filename()]
        if not (runtime_dir / name).exists()
    ]
    missing.extend(runtime_missing)
    if missing:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(f"Windows 配布物に必要なランタイムが不足しています: {missing_text}")

    print_step("Windows ランタイム検査: ok")


def stage_executable_path(stage_dir: Path) -> Path:
    if sys.platform == "darwin":
        return stage_dir / "YAM.app" / "Contents" / "MacOS" / "YAM"
    return stage_dir / "YAM.exe"


def run_built_smoke_check(stage_dir: Path) -> None:
    executable_path = stage_executable_path(stage_dir)
    if not executable_path.exists():
        raise FileNotFoundError(f"ビルド済み実行ファイルが見つかりません: {executable_path}")

    subprocess.run(
        [str(executable_path), "--check"],
        cwd=stage_dir,
        env=smoke_check_env(stage_dir),
        check=True,
    )
    print_step("スタンドアロン起動チェック: ok")


def cleanup_release_workspace() -> None:
    if sys.platform == "darwin":
        redundant_dir = DIST_DIR / "YAM"
        if redundant_dir.exists():
            shutil.rmtree(redundant_dir, ignore_errors=True)

    for path in (BUILD_DIR, BUILD_ASSETS_DIR, RELEASE_ROOT_DIR / ".pyinstaller"):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
    cleanup_release_junk()


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print_step("PyInstaller がありません。")
        print_step("まず `python -m pip install pyinstaller` を実行してください。")
        return 1
    if Image is None:
        print_step("Pillow がありません。")
        print_step("まず `python -m pip install pillow` を実行してください。")
        return 1

    version = load_app_version()
    ensure_spec_file()
    ensure_clean_artifacts()
    icon_file = prepare_icon_file()
    if icon_file is not None:
        print_step(f"icon: {icon_file}")
    print_step(f"platform: {platform_label()} / arch: {platform_arch_label()}")

    run_pyinstaller(icon_file, version)
    built_target = find_built_target()
    stage_dir = stage_release_bundle(built_target, version)
    verify_windows_bundle(stage_dir)
    run_built_smoke_check(stage_dir)
    cleanup_release_workspace()

    print_step(f"built: {built_target}")
    print_step(f"release folder: {stage_dir}")
    print_step("このフォルダをそのまま配布すれば、利用者側に Python は不要です。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
