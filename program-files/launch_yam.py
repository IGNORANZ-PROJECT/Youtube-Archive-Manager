import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any, Dict


FROZEN_APP = bool(getattr(sys, "frozen", False))


def resolve_base_dir() -> Path:
    if not FROZEN_APP:
        return Path(__file__).resolve().parent

    executable_path = Path(sys.executable).resolve()
    if sys.platform == "darwin":
        executable_dir = executable_path.parent
        if executable_dir.name == "MacOS" and executable_dir.parent.name == "Contents":
            app_bundle_dir = executable_dir.parent.parent
            if app_bundle_dir.suffix.lower() == ".app":
                return app_bundle_dir.parent
    return executable_path.parent


BASE_DIR = resolve_base_dir()
VENV_DIR = BASE_DIR / ".venv"
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"
BOOTSTRAP_STATE_PATH = VENV_DIR / ".yam-bootstrap.json"
STARTUP_LOG_PATH = BASE_DIR / "yam_startup.log"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


def is_windows() -> bool:
    return os.name == "nt"


def venv_python_path() -> Path:
    return VENV_DIR / ("Scripts/python.exe" if is_windows() else "bin/python")


def print_step(message: str) -> None:
    print(f"[YAM] {message}", flush=True)


def write_startup_log() -> Path:
    try:
        STARTUP_LOG_PATH.write_text(traceback.format_exc(), encoding="utf-8")
    except OSError:
        return STARTUP_LOG_PATH
    return STARTUP_LOG_PATH


def show_startup_error(log_path: Path) -> None:
    message = f"YAM の起動に失敗しました。\nログを確認してください:\n{log_path}"

    if is_windows():
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message, "YAM startup error", 0x10)
            return
        except Exception:
            pass

    if sys.platform == "darwin":
        try:
            escaped_lines = [
                line.replace("\\", "\\\\").replace("\"", "\\\"")
                for line in message.splitlines()
            ]
            escaped = "\" & return & \"".join(escaped_lines) if escaped_lines else ""
            script = (
                f'display dialog "{escaped}" '
                'with title "YAM startup error" buttons {"OK"} default button "OK" with icon stop'
            )
            subprocess.run(["osascript", "-e", script], check=False)
            return
        except Exception:
            pass

    print_step(message)


def run_step(command: list[str], label: str) -> None:
    print_step(label)
    subprocess.run(command, cwd=BASE_DIR, check=True)


def requirements_signature() -> Dict[str, Any]:
    digest = hashlib.sha256(REQUIREMENTS_PATH.read_bytes()).hexdigest()
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "requirements_sha256": digest,
    }


def load_bootstrap_state() -> Dict[str, Any]:
    if not BOOTSTRAP_STATE_PATH.exists():
        return {}
    try:
        return json.loads(BOOTSTRAP_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def save_bootstrap_state(state: Dict[str, Any]) -> None:
    VENV_DIR.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=VENV_DIR, suffix=".tmp")
    os.close(fd)
    try:
        Path(temp_path).write_text(
            json.dumps(state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temp_path, BOOTSTRAP_STATE_PATH)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def ensure_virtualenv() -> None:
    if venv_python_path().exists():
        return
    run_step([sys.executable, "-m", "venv", str(VENV_DIR)], "初回環境を作成しています...")


def venv_dependencies_are_ready() -> bool:
    python_bin = venv_python_path()
    if not python_bin.exists():
        return False

    try:
        result = subprocess.run(
            [str(python_bin), "-c", "import flask, jinja2, werkzeug"],
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return False

    return result.returncode == 0


def ensure_requirements() -> None:
    expected = requirements_signature()
    if load_bootstrap_state() == expected and venv_dependencies_are_ready():
        return

    if not venv_dependencies_are_ready():
        print_step("仮想環境の依存関係を修復しています...")

    python_bin = str(venv_python_path())
    run_step([python_bin, "-m", "pip", "install", "--upgrade", "pip"], "pip を更新しています...")
    run_step([python_bin, "-m", "pip", "install", "-r", str(REQUIREMENTS_PATH)], "依存関係をインストールしています...")
    if not venv_dependencies_are_ready():
        raise RuntimeError("依存関係のインストール後も Flask を読み込めません。")
    save_bootstrap_state(expected)


def choose_port(host: str, preferred: int) -> int:
    preferred = int(preferred or DEFAULT_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, preferred))
            return preferred
        except OSError:
            sock.bind((host, 0))
            return int(sock.getsockname()[1])


def wait_for_server(url: str, timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    probe_url = f"{url}api/sync-status"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(probe_url, timeout=1):
                return
        except Exception:
            time.sleep(0.35)


def open_browser_when_ready(url: str) -> None:
    try:
        wait_for_server(url)
    finally:
        webbrowser.open(url, new=1)


def relaunch_in_venv(arguments: list[str]) -> None:
    python_bin = str(venv_python_path())
    os.execv(python_bin, [python_bin, str(BASE_DIR / "launch_yam.py"), *arguments])


def serve(host: str, port: int, no_browser: bool) -> int:
    os.environ["YAM_HOST"] = host
    os.environ["YAM_PORT"] = str(port)
    os.environ["YAM_DEBUG"] = "0"

    url = f"http://127.0.0.1:{port}/"
    print_step(f"起動URL: {url}")
    print_step("終了するには、このウィンドウを閉じるか Ctrl+C を押してください。")

    if not no_browser:
        threading.Thread(target=open_browser_when_ready, args=(url,), daemon=True).start()

    from app import run_server

    run_server(host=host, port=port, debug=False)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--help", action="help")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.check:
        print_step(f"project: {BASE_DIR}")
        print_step(f"python: {sys.executable}")
        print_step(f"venv: {venv_python_path()}")
        from app import run_server  # noqa: F401
        print_step("imports: ok")
        print_step("check: ok")
        return 0

    if args.serve:
        return serve(args.host, args.port, args.no_browser)

    if FROZEN_APP:
        return serve(args.host, choose_port(args.host, args.port), args.no_browser)

    ensure_virtualenv()
    ensure_requirements()
    port = choose_port(args.host, args.port)
    next_args = ["--serve", "--host", args.host, "--port", str(port)]
    if args.no_browser:
        next_args.append("--no-browser")
    relaunch_in_venv(next_args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        log_path = write_startup_log()
        if FROZEN_APP:
            show_startup_error(log_path)
            raise SystemExit(1)
        raise
