import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent.parent
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"
RELEASE_DIR = BASE_DIR / "release"
SPEC_PATH = SCRIPT_DIR / "yam.spec"


def print_step(message: str) -> None:
    print(f"[YAM Build] {message}", flush=True)


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print_step("PyInstaller がありません。")
        print_step("まず `python -m pip install pyinstaller` を実行してください。")
        return 1

    for path in (DIST_DIR, BUILD_DIR, RELEASE_DIR):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

    print_step("PyInstaller でスタンドアロン版をビルドしています...")
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--noconfirm", str(SPEC_PATH)],
        cwd=BASE_DIR,
        check=True,
    )

    built_dir = DIST_DIR / "YAM"
    release_target = RELEASE_DIR / "YAM"
    release_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(built_dir, release_target, dirs_exist_ok=True)

    print_step(f"release: {release_target}")
    print_step("このフォルダを配布すれば、利用者側に Python は不要です。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
