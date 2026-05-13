import csv
import io
import json
import locale
import os
import re
import shutil
import socket
import sys
import tempfile
import threading
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from flask import Flask, Response, has_request_context, jsonify, render_template, request, send_file, stream_with_context
from werkzeug.serving import BaseWSGIServer, make_server

__author__ = "Arata"
__version__ = "1.3.1"


FROZEN_APP = bool(getattr(sys, "frozen", False))


def resolve_app_dir() -> str:
    if not FROZEN_APP:
        return os.path.dirname(os.path.abspath(__file__))

    executable_dir = os.path.dirname(sys.executable)
    if sys.platform == "darwin":
        contents_dir = os.path.dirname(executable_dir)
        app_bundle_dir = os.path.dirname(contents_dir)
        if app_bundle_dir.lower().endswith(".app"):
            return os.path.dirname(app_bundle_dir)

    return executable_dir


APP_DIR = resolve_app_dir()
RESOURCE_DIR = getattr(sys, "_MEIPASS", APP_DIR)
DATA_DIR = os.path.join(APP_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
ASSETS_DIR = os.path.join(APP_DIR, "assets")
PACKAGED_ASSETS_DIR = os.path.join(RESOURCE_DIR, "assets")
DEFAULT_UI_ICON_URL = "/assets/icon.png"

VIDEOS_CSV = os.path.join(DATA_DIR, "videos.csv")
PROGRESS_CSV = os.path.join(DATA_DIR, "progress.csv")
PROGRESS_HISTORY_CSV = os.path.join(DATA_DIR, "progress_history.csv")
NOTES_CSV = os.path.join(DATA_DIR, "notes.csv")
CONFIG_JSON = os.path.join(DATA_DIR, "config.json")

VIDEO_HEADERS = [
    "video_id",
    "title",
    "url",
    "duration_seconds",
    "published_at",
    "thumbnail_url",
    "channel_id",
    "channel_title",
    "source",
    "manual_tags",
    "youtube_tags",
    "deleted",
    "last_seen_at",
    "created_at",
    "updated_at",
]
PROGRESS_HEADERS = ["video_id", "status", "watched_seconds", "last_position_seconds", "updated_at"]
PROGRESS_HISTORY_HEADERS = [
    "video_id",
    "delta_seconds",
    "previous_watched_seconds",
    "watched_seconds",
    "status",
    "logged_at",
]
NOTE_HEADERS = ["video_id", "note", "updated_at"]

DEFAULT_CONFIG = {
    "youtube_api_key": "",
    "channel_reference": "",
    "channel_id": "",
    "channel_title": "",
    "uploads_playlist_id": "",
    "channel_details": [],
    "auto_sync_minutes": 30,
    "backup_limit": 5,
    "sync_excluded_tags": "",
    "stats_ratio_query": "",
    "stats_average_query": "",
    "ui_icon_url": DEFAULT_UI_ICON_URL,
    "ui_language": "",
    "default_sort": "published_desc",
    "last_synced_at": "",
    "last_sync_status": "idle",
    "last_sync_message": "YouTube同期は未設定です。",
}

SORT_OPTIONS = {"published_desc", "published_asc"}
SUPPORTED_UI_LANGUAGES = {"ja", "en"}
DEFAULT_UI_LANGUAGE = "en"
UI_LOCALE_MAP = {
    "ja": "ja-JP",
    "en": "en-US",
}
TEMPLATE_TEXT = {
    "ja": {
        "index_title": "Youtube Archive Manager (YAM)",
        "settings_title": "Youtube Archive Manager (YAM) - Settings",
        "index_sub": "同期は設定・統計から設定できます。",
        "settings_sub": "APIキーとチャンネルを設定すると同期できます。",
        "nav_index": "一覧",
        "nav_settings": "設定・統計",
        "button_add": "追加",
        "button_sync": "同期",
        "search": "検索",
        "search_placeholder": "キーワード検索 例: 歌枠 -切り抜き",
        "tags": "タグ",
        "none_selected": "未選択",
        "clear": "解除",
        "watch_status": "視聴状態",
        "status_all": "全て",
        "status_watched": "見た",
        "status_partial": "途中",
        "status_unseen": "未視聴",
        "sort": "並び順",
        "sort_newest": "新しい順",
        "sort_oldest": "古い順",
        "button_search": "検索",
        "button_reset": "リセット",
        "progress": "進捗",
        "watched_total": "視聴済み",
        "partial": "途中",
        "unseen": "未視聴",
        "watched_total_time": "見た総時間",
        "remaining": "残り",
        "list_title": "一覧",
        "zero_items": "0件",
        "select_visible": "表示中を全選択",
        "clear_selection": "選択解除",
        "zero_selected": "0件選択中",
        "button_mark_watched": "視聴済み",
        "button_mark_unwatched": "未視聴",
        "bulk_add_tags_placeholder": "一括追加タグ",
        "bulk_add_tags": "タグ追加",
        "bulk_remove_tags_placeholder": "一括削除タグ",
        "bulk_remove_tags": "タグ削除",
        "button_delete": "削除",
        "manual_add": "手動追加",
        "button_close": "閉じる",
        "label_url": "URL",
        "label_current_progress": "現在の視聴進捗",
        "label_add_as_watched": "視聴済みとして追加",
        "details_input": "詳細入力",
        "label_title": "タイトル",
        "label_title_placeholder": "必要な場合のみ入力",
        "label_duration": "全体の長さ",
        "label_tags_placeholder": "タグをカンマ区切りで入力",
        "label_thumbnail": "サムネ画像",
        "label_note": "感想 / メモ",
        "label_note_placeholder": "感想、補足、メモ",
        "button_add_submit": "追加する",
        "button_open": "開く",
        "button_resume": "続き",
        "button_thumb": "サムネ",
        "button_edit": "編集",
        "label_watch_time": "視聴時間",
        "button_save": "保存",
        "button_clear_progress": "解除",
        "tag_summary": "タグ",
        "button_save_tags": "タグ保存",
        "label_note_editor_placeholder": "感想、見どころ、旧タイトル履歴",
        "button_save_note": "感想保存",
        "section_sync_settings": "同期設定",
        "label_api_key": "YouTube APIキー",
        "label_channel_reference": "チャンネルID / URL / @handle",
        "label_channel_reference_placeholder": "UC... / URL / @handle を改行またはカンマ区切りで入力",
        "label_auto_sync_minutes": "自動同期間隔(分)",
        "label_backup_limit": "バックアップ保持数",
        "label_language": "言語",
        "language_japanese": "日本語",
        "language_english": "English",
        "label_sync_excluded_tags": "同期で除外するタグ",
        "label_sync_excluded_tags_placeholder": "例: 切り抜き, Shorts",
        "label_icon": "アイコン",
        "button_save_icon": "アイコン保存",
        "label_default_sort": "一覧の初期並び順",
        "button_save_settings": "設定保存",
        "button_apply_existing": "既存へ適用",
        "section_stats": "統計",
        "button_day": "日別",
        "button_month": "月別",
        "button_prev": "前へ",
        "button_today": "今日",
        "button_next": "次へ",
        "label_watch_progress": "視聴進捗",
        "label_window_average": "表示平均 00:00:00",
        "label_overall_average": "全体平均 00:00:00",
        "label_tag_ratio": "指定タグの割合",
        "label_condition": "条件",
        "label_ratio_placeholder": "例: コラボ -切り抜き",
        "label_average_duration": "1日の平均配信時間",
        "label_average_placeholder": "例: 生配信 -切り抜き",
        "button_stats_apply": "統計更新",
        "button_stats_save": "条件保存",
        "credits_summary": "©IGNORANZ PROJECT",
        "credits_planning": "企画：じょしゅのうち",
        "credits_system": "システム：江上 新",
        "credits_x": "IGNORANZ PROJECT X",
        "credits_site": "IGNORANZ PROJECT 公式サイト",
    },
    "en": {
        "index_title": "Youtube Archive Manager (YAM)",
        "settings_title": "Youtube Archive Manager (YAM) - Settings",
        "index_sub": "Configure sync from Settings & Stats.",
        "settings_sub": "Set your API key and one or more channels to enable sync.",
        "nav_index": "Library",
        "nav_settings": "Settings & Stats",
        "button_add": "Add",
        "button_sync": "Sync",
        "search": "Search",
        "search_placeholder": "Keywords e.g. karaoke -clip",
        "tags": "Tags",
        "none_selected": "None",
        "clear": "Clear",
        "watch_status": "Watch status",
        "status_all": "All",
        "status_watched": "Watched",
        "status_partial": "In progress",
        "status_unseen": "Unwatched",
        "sort": "Sort",
        "sort_newest": "Newest first",
        "sort_oldest": "Oldest first",
        "button_search": "Search",
        "button_reset": "Reset",
        "progress": "Progress",
        "watched_total": "Watched",
        "partial": "Partial",
        "unseen": "Unwatched",
        "watched_total_time": "Watched time",
        "remaining": "Remaining",
        "list_title": "Library",
        "zero_items": "0 items",
        "select_visible": "Select visible",
        "clear_selection": "Clear selection",
        "zero_selected": "0 selected",
        "button_mark_watched": "Watched",
        "button_mark_unwatched": "Unwatched",
        "bulk_add_tags_placeholder": "Tags to add",
        "bulk_add_tags": "Add tags",
        "bulk_remove_tags_placeholder": "Tags to remove",
        "bulk_remove_tags": "Remove tags",
        "button_delete": "Delete",
        "manual_add": "Add manually",
        "button_close": "Close",
        "label_url": "URL",
        "label_current_progress": "Current progress",
        "label_add_as_watched": "Add as watched",
        "details_input": "More fields",
        "label_title": "Title",
        "label_title_placeholder": "Optional",
        "label_duration": "Total duration",
        "label_tags_placeholder": "Enter tags separated by commas",
        "label_thumbnail": "Thumbnail image",
        "label_note": "Notes / Memo",
        "label_note_placeholder": "Notes, highlights, memo",
        "button_add_submit": "Add",
        "button_open": "Open",
        "button_resume": "Resume",
        "button_thumb": "Thumb",
        "button_edit": "Edit",
        "label_watch_time": "Watch time",
        "button_save": "Save",
        "button_clear_progress": "Clear",
        "tag_summary": "Tags",
        "button_save_tags": "Save tags",
        "label_note_editor_placeholder": "Notes, highlights, old title history",
        "button_save_note": "Save notes",
        "section_sync_settings": "Sync settings",
        "label_api_key": "YouTube API key",
        "label_channel_reference": "Channel ID / URL / @handle",
        "label_channel_reference_placeholder": "Enter one or more UC... / URLs / @handles separated by lines or commas",
        "label_auto_sync_minutes": "Auto sync interval (min)",
        "label_backup_limit": "Backup retention",
        "label_language": "Language",
        "language_japanese": "Japanese",
        "language_english": "English",
        "label_sync_excluded_tags": "Excluded tags on sync",
        "label_sync_excluded_tags_placeholder": "e.g. clip, Shorts",
        "label_icon": "Icon",
        "button_save_icon": "Save icon",
        "label_default_sort": "Default library sort",
        "button_save_settings": "Save settings",
        "button_apply_existing": "Apply to existing",
        "section_stats": "Stats",
        "button_day": "Day",
        "button_month": "Month",
        "button_prev": "Prev",
        "button_today": "Today",
        "button_next": "Next",
        "label_watch_progress": "Watch progress",
        "label_window_average": "Window avg 00:00:00",
        "label_overall_average": "Overall avg 00:00:00",
        "label_tag_ratio": "Matching tag ratio",
        "label_condition": "Query",
        "label_ratio_placeholder": "e.g. collab -clip",
        "label_average_duration": "Average stream duration per day",
        "label_average_placeholder": "e.g. livestream -clip",
        "button_stats_apply": "Refresh stats",
        "button_stats_save": "Save query",
        "credits_summary": "©IGNORANZ PROJECT",
        "credits_planning": "Planning: Joshu no Uchi",
        "credits_system": "System: Arata Egami",
        "credits_x": "IGNORANZ PROJECT X",
        "credits_site": "IGNORANZ PROJECT Website",
    },
}
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
DAY_CHART_POINTS = 14
MONTH_CHART_POINTS = 12
AUTO_BACKUP_INTERVAL = timedelta(hours=24)
RECENT_DETAILS_REFRESH_LIMIT = 24

DATA_CACHE: Dict[str, Any] = {
    "key": None,
    "videos": [],
    "summary": {},
}
PROGRESS_HISTORY_CACHE: Dict[str, Any] = {
    "key": None,
    "rows": [],
}
CONFIG_CACHE: Dict[str, Any] = {
    "loaded": False,
    "data": {},
}
SYNC_LOCK = threading.Lock()
STORAGE_LOCK = threading.Lock()
STORAGE_READY = False
APP_CLIENT_LOCK = threading.Lock()
APP_CLIENT_STREAM_PING_SECONDS = 4.0
APP_CLIENT_TTL_SECONDS = 12.0
APP_AUTO_EXIT_GRACE_SECONDS = 6.0
APP_AUTO_EXIT_POLL_SECONDS = 0.5
APP_LIFECYCLE_STATE: Dict[str, Any] = {
    "clients": {},
    "armed": False,
    "zero_clients_since": None,
}
SERVER_STATE: Dict[str, Any] = {
    "server": None,
    "shutdown_requested": False,
    "monitor_thread": None,
}
SYNC_STATE: Dict[str, Any] = {
    "running": False,
    "started_at": "",
    "mode": "",
}

app = Flask(
    __name__,
    static_folder=os.path.join(RESOURCE_DIR, "static"),
    template_folder=os.path.join(RESOURCE_DIR, "templates"),
)


def runtime_host() -> str:
    return str(os.environ.get("YAM_HOST", "127.0.0.1")).strip() or "127.0.0.1"


def runtime_port() -> int:
    return max(1, parse_int(os.environ.get("YAM_PORT", 5000), 5000))


def runtime_debug() -> bool:
    return truthy(os.environ.get("YAM_DEBUG", "0"))


def runtime_auto_exit() -> bool:
    if "YAM_AUTO_EXIT" in os.environ:
        return truthy(os.environ.get("YAM_AUTO_EXIT", "0"))
    return not runtime_debug()


def choose_runtime_port(host: str, preferred_port: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, max(1, int(preferred_port))))
            return max(1, int(preferred_port))
        except OSError:
            sock.bind((host, 0))
            return int(sock.getsockname()[1])


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_utc_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def monotonic_now() -> float:
    return time.monotonic()


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def split_channel_references(raw: Any) -> List[str]:
    values: List[str] = []
    seen = set()
    for item in re.split(r"[\n\r,]+", str(raw or "")):
        normalized = normalize_channel_reference(item.strip())
        if not normalized:
            continue
        lowered = normalized.casefold()
        if lowered in seen:
            continue
        seen.add(lowered)
        values.append(normalized)
    return values


def normalize_channel_reference_text(raw: Any) -> str:
    return "\n".join(split_channel_references(raw))


def normalize_supported_language(value: Any) -> str:
    raw = str(value or "").strip().lower().replace("_", "-")
    if raw.startswith("ja"):
        return "ja"
    if raw.startswith("en"):
        return "en"
    return ""


def detect_system_language() -> str:
    candidates: List[str] = []

    if has_request_context():
        candidates.extend([value for value, _quality in request.accept_languages])

    try:
        default_locale = locale.getdefaultlocale()[0]
    except (ValueError, TypeError, IndexError, AttributeError):
        default_locale = ""

    candidates.extend([
        default_locale,
        os.getenv("LC_ALL", ""),
        os.getenv("LC_MESSAGES", ""),
        os.getenv("LANG", ""),
    ])

    for candidate in candidates:
        normalized = normalize_supported_language(candidate)
        if normalized:
            return normalized

    return DEFAULT_UI_LANGUAGE


def resolve_ui_language(config: Dict[str, Any]) -> str:
    saved = normalize_supported_language(config.get("ui_language", ""))
    if saved:
        return saved
    return detect_system_language()


def get_template_text(language: str) -> Dict[str, str]:
    normalized = normalize_supported_language(language) or DEFAULT_UI_LANGUAGE
    return TEMPLATE_TEXT.get(normalized, TEMPLATE_TEXT[DEFAULT_UI_LANGUAGE])


def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None

    raw = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass

    normalized = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is not None:
            return parsed.replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


def parse_duration_input(value: Any, default: int = 0) -> int:
    if value is None:
        return default

    if isinstance(value, (int, float)):
        return max(0, int(value))

    text = str(value).strip()
    if not text:
        return default

    if re.fullmatch(r"\d+", text):
        return max(0, int(text))

    parts = text.split(":")
    if len(parts) not in {2, 3}:
        return default
    if any(not part.isdigit() for part in parts):
        return default

    if len(parts) == 2:
        hours = 0
        minutes, seconds = [int(part) for part in parts]
    else:
        hours, minutes, seconds = [int(part) for part in parts]

    if minutes >= 60 or seconds >= 60:
        return default

    return max(0, hours * 3600 + minutes * 60 + seconds)


def format_seconds(seconds: int) -> str:
    seconds = max(0, seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{hours:02}:{minutes:02}:{sec:02}"


def split_tags(raw: str) -> List[str]:
    if not raw:
        return []

    values = re.split(r"[,\n、]+", raw)
    normalized: List[str] = []
    seen = set()

    for value in values:
        tag = re.sub(r"\s+", " ", value.strip())
        if not tag:
            continue
        lowered = tag.casefold()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(tag)

    return normalized


def join_tags(tags: List[str]) -> str:
    ordered = sorted(split_tags(", ".join(tags)), key=lambda item: item.casefold())
    return ", ".join(ordered)


def split_setting_values(raw: str) -> List[str]:
    if not raw:
        return []

    values = re.split(r"[,\n、]+", raw)
    normalized: List[str] = []
    seen = set()
    for value in values:
        word = value.strip()
        if not word:
            continue
        lowered = word.casefold()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(word)
    return normalized


def split_search_terms(raw: str) -> Tuple[List[str], List[str]]:
    if not raw:
        return [], []

    include_terms: List[str] = []
    exclude_terms: List[str] = []
    for term in re.split(r"[\s,]+", raw.strip()):
        if not term:
            continue
        if term.startswith("-") and len(term) > 1:
            exclude_terms.append(term[1:].casefold())
        else:
            include_terms.append(term.casefold())
    return include_terms, exclude_terms


def normalize_sort(sort_name: str) -> str:
    if sort_name in SORT_OPTIONS:
        return sort_name
    return DEFAULT_CONFIG["default_sort"]


def slugify_filename(text: str, fallback: str = "thumbnail") -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", text.strip(), flags=re.UNICODE).strip("_")
    return cleaned or fallback


def ensure_directories() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    ensure_csv(VIDEOS_CSV, VIDEO_HEADERS)
    ensure_csv(PROGRESS_CSV, PROGRESS_HEADERS)
    ensure_csv(PROGRESS_HISTORY_CSV, PROGRESS_HISTORY_HEADERS)
    ensure_csv(NOTES_CSV, NOTE_HEADERS)
    ensure_config()
    migrate_existing_data()


def ensure_csv(file_path: str, headers: List[str]) -> None:
    if not os.path.exists(file_path):
        atomic_write_csv(file_path, headers, [])
        return

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        current_headers = next(reader, [])

    if current_headers == headers:
        return

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    atomic_write_csv(file_path, headers, rows)


def atomic_write_csv(file_path: str, headers: List[str], rows: List[Dict[str, Any]]) -> None:
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    os.close(fd)

    try:
        with open(temp_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                safe_row = {key: row.get(key, "") for key in headers}
                writer.writerow(safe_row)
        os.replace(temp_path, file_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    invalidate_data_caches()


def read_csv(file_path: str) -> List[Dict[str, str]]:
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_json(file_path: str, default: Any) -> Any:
    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return default


def atomic_write_json(file_path: str, payload: Dict[str, Any]) -> None:
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    os.close(fd)

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, file_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def invalidate_data_caches() -> None:
    DATA_CACHE["key"] = None
    DATA_CACHE["videos"] = []
    DATA_CACHE["summary"] = {}
    PROGRESS_HISTORY_CACHE["key"] = None
    PROGRESS_HISTORY_CACHE["rows"] = []


def file_signature(*paths: str) -> Tuple[Tuple[str, float, int], ...]:
    signature: List[Tuple[str, float, int]] = []
    for path in paths:
        if not os.path.exists(path):
            signature.append((path, 0.0, 0))
            continue
        stat = os.stat(path)
        signature.append((path, stat.st_mtime, stat.st_size))
    return tuple(signature)


def load_config() -> Dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    stored = read_json(CONFIG_JSON, None)
    if isinstance(stored, dict):
        CONFIG_CACHE["loaded"] = True
        CONFIG_CACHE["data"] = dict(stored)
    elif CONFIG_CACHE["loaded"]:
        stored = dict(CONFIG_CACHE["data"])
    else:
        stored = {}
    if isinstance(stored, dict):
        for key, value in stored.items():
            if key in config:
                config[key] = value

    if not config["youtube_api_key"]:
        config["youtube_api_key"] = os.getenv("YOUTUBE_API_KEY", "").strip()

    if not config["channel_reference"]:
        env_channel = (
            os.getenv("YOUTUBE_CHANNEL_REFERENCE", "").strip()
            or os.getenv("YOUTUBE_CHANNEL_ID", "").strip()
        )
        config["channel_reference"] = env_channel

    config["channel_reference"] = normalize_channel_reference_text(config.get("channel_reference", ""))
    config["auto_sync_minutes"] = max(1, parse_int(config.get("auto_sync_minutes", 30), 30))
    config["backup_limit"] = max(1, parse_int(config.get("backup_limit", DEFAULT_CONFIG["backup_limit"]), DEFAULT_CONFIG["backup_limit"]))
    config["sync_excluded_tags"] = ", ".join(split_tags(str(config.get("sync_excluded_tags", ""))))
    config["ui_icon_url"] = str(config.get("ui_icon_url", "")).strip() or DEFAULT_UI_ICON_URL
    config["ui_language"] = normalize_supported_language(config.get("ui_language", ""))
    config["default_sort"] = normalize_sort(str(config.get("default_sort", DEFAULT_CONFIG["default_sort"])))
    config["uploads_playlist_id"] = str(config.get("uploads_playlist_id", "")).strip()
    config["channel_details"] = channel_details_from_config(config)
    return config


def save_config(config: Dict[str, Any]) -> Dict[str, Any]:
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    merged["youtube_api_key"] = str(merged.get("youtube_api_key", "")).strip()
    merged["channel_reference"] = normalize_channel_reference_text(merged.get("channel_reference", ""))
    merged["channel_id"] = str(merged.get("channel_id", "")).strip()
    merged["channel_title"] = str(merged.get("channel_title", "")).strip()
    merged["uploads_playlist_id"] = str(merged.get("uploads_playlist_id", "")).strip()
    merged["channel_details"] = channel_details_from_config(merged)
    merged["auto_sync_minutes"] = max(1, parse_int(merged.get("auto_sync_minutes", 30), 30))
    merged["backup_limit"] = max(1, parse_int(merged.get("backup_limit", DEFAULT_CONFIG["backup_limit"]), DEFAULT_CONFIG["backup_limit"]))
    merged["sync_excluded_tags"] = ", ".join(split_tags(str(merged.get("sync_excluded_tags", ""))))
    merged["ui_icon_url"] = str(merged.get("ui_icon_url", "")).strip() or DEFAULT_UI_ICON_URL
    merged["ui_language"] = normalize_supported_language(merged.get("ui_language", ""))
    merged["default_sort"] = normalize_sort(str(merged.get("default_sort", DEFAULT_CONFIG["default_sort"])))
    merged["last_sync_status"] = str(merged.get("last_sync_status", "idle")).strip() or "idle"
    merged["last_sync_message"] = str(merged.get("last_sync_message", "")).strip()
    atomic_write_json(CONFIG_JSON, merged)
    CONFIG_CACHE["loaded"] = True
    CONFIG_CACHE["data"] = dict(merged)
    return merged


def ensure_config() -> None:
    if os.path.exists(CONFIG_JSON):
        return
    save_config(DEFAULT_CONFIG.copy())


def ensure_storage_ready() -> None:
    global STORAGE_READY
    if STORAGE_READY:
        return

    with STORAGE_LOCK:
        if STORAGE_READY:
            return
        ensure_directories()
        STORAGE_READY = True


def build_sync_info(config: Dict[str, Any]) -> Dict[str, Any]:
    channel_details = channel_details_from_config(config)
    channel_titles = [detail["channel_title"] for detail in channel_details if detail.get("channel_title")]
    configured = bool(config.get("youtube_api_key") and split_channel_references(config.get("channel_reference", "")))
    runtime_running = bool(SYNC_STATE.get("running"))
    status = str(config.get("last_sync_status", "idle"))
    message = str(config.get("last_sync_message", ""))

    if not configured:
        status = "unconfigured"
        message = "未設定"
    elif runtime_running:
        status = "syncing"
        message = "同期中"

    return {
        "configured": configured,
        "channel_reference": config.get("channel_reference", ""),
        "channel_id": config.get("channel_id", ""),
        "channel_title": config.get("channel_title", ""),
        "channel_titles": channel_titles,
        "channel_count": len(channel_titles),
        "uploads_playlist_id": config.get("uploads_playlist_id", ""),
        "auto_sync_minutes": config.get("auto_sync_minutes", 30),
        "last_synced_at": config.get("last_synced_at", ""),
        "last_sync_status": status,
        "last_sync_message": message,
        "running": runtime_running,
        "started_at": SYNC_STATE.get("started_at", ""),
    }


def resolve_ui_icon_url(config: Dict[str, Any]) -> str:
    return str(config.get("ui_icon_url", "")).strip() or DEFAULT_UI_ICON_URL


def resolve_asset_path(filename: str) -> str:
    safe_name = os.path.basename(filename)
    if safe_name != filename:
        return ""

    external_path = os.path.join(ASSETS_DIR, safe_name)
    if os.path.exists(external_path):
        return external_path

    packaged_path = os.path.join(PACKAGED_ASSETS_DIR, safe_name)
    if os.path.exists(packaged_path):
        return packaged_path

    return ""


def build_settings_payload(config: Dict[str, Any]) -> Dict[str, Any]:
    ui_language = resolve_ui_language(config)
    return {
        "youtube_api_key": config.get("youtube_api_key", ""),
        "channel_reference": config.get("channel_reference", ""),
        "channel_id": config.get("channel_id", ""),
        "channel_title": config.get("channel_title", ""),
        "auto_sync_minutes": config.get("auto_sync_minutes", 30),
        "backup_limit": config.get("backup_limit", DEFAULT_CONFIG["backup_limit"]),
        "sync_excluded_tags": config.get("sync_excluded_tags", ""),
        "stats_ratio_query": str(config.get("stats_ratio_query", "")).strip(),
        "stats_average_query": str(config.get("stats_average_query", "")).strip(),
        "ui_icon_url": resolve_ui_icon_url(config),
        "ui_language": ui_language,
        "default_sort": config.get("default_sort", DEFAULT_CONFIG["default_sort"]),
        "sync": build_sync_info(config),
    }


def should_refresh_channel_details(config: Dict[str, Any], next_api_key: str, next_channel_reference: str) -> bool:
    if not next_api_key or not next_channel_reference:
        return False

    next_references = split_channel_references(next_channel_reference)
    current_references = split_channel_references(config.get("channel_reference", ""))
    stored_details = channel_details_from_config(config)

    if not stored_details:
        return True

    if next_api_key != str(config.get("youtube_api_key", "")).strip():
        return True

    if current_references != next_references:
        return True

    return len(stored_details) != len(next_references)


def normalize_video_rows(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], bool]:
    changed = False
    normalized: List[Dict[str, str]] = []
    seed_time = datetime.now() - timedelta(seconds=max(len(rows), 1))

    for index, original_row in enumerate(rows):
        row = {key: original_row.get(key, "") for key in VIDEO_HEADERS}
        fallback_created = (seed_time + timedelta(seconds=index)).strftime("%Y-%m-%d %H:%M:%S")
        created_at = row.get("created_at", "").strip() or row.get("updated_at", "").strip() or row.get("published_at", "").strip() or fallback_created
        updated_at = row.get("updated_at", "").strip() or created_at
        source = row.get("source", "").strip() or ("manual" if row.get("video_id", "").startswith("manual-") else "youtube")

        row["duration_seconds"] = str(max(0, parse_int(row.get("duration_seconds", 0), 0)))
        row["created_at"] = created_at
        row["updated_at"] = updated_at
        row["source"] = source
        merged_editable_tags = split_tags(", ".join([
            row.get("manual_tags", ""),
            row.get("youtube_tags", ""),
        ]))
        row["manual_tags"] = join_tags(merged_editable_tags)
        row["youtube_tags"] = join_tags(split_tags(row.get("youtube_tags", "")))
        row["deleted"] = "1" if truthy(row.get("deleted", "")) else "0"

        normalized.append(row)
        if any(row.get(key, "") != original_row.get(key, "") for key in VIDEO_HEADERS):
            changed = True

    return normalized, changed


def migrate_existing_data() -> None:
    video_rows = read_csv(VIDEOS_CSV)
    normalized_video_rows, video_changed = normalize_video_rows(video_rows)
    if video_changed:
        atomic_write_csv(VIDEOS_CSV, VIDEO_HEADERS, normalized_video_rows)


def read_video_rows() -> List[Dict[str, str]]:
    return read_csv(VIDEOS_CSV)


def write_video_rows(rows: List[Dict[str, Any]]) -> None:
    atomic_write_csv(VIDEOS_CSV, VIDEO_HEADERS, rows)


def build_watch_url(url: str, seconds: int) -> str:
    if not url:
        return ""
    seconds = max(0, seconds)
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}t={seconds}s"


def normalize_status(watched_seconds: int, duration_seconds: int, mark_watched: bool = False) -> str:
    if mark_watched:
        return "watched"
    if watched_seconds <= 0:
        return "unseen"
    if duration_seconds <= 0:
        return "partial"
    if watched_seconds >= int(duration_seconds * 0.9):
        return "watched"
    return "partial"


def get_progress_map() -> Dict[str, Dict[str, str]]:
    return {row["video_id"]: row for row in read_csv(PROGRESS_CSV) if row.get("video_id")}


def get_notes_map() -> Dict[str, Dict[str, str]]:
    return {row["video_id"]: row for row in read_csv(NOTES_CSV) if row.get("video_id")}


def append_progress_history(
    video_id: str,
    previous_watched_seconds: int,
    watched_seconds: int,
    status: str,
) -> None:
    if previous_watched_seconds == watched_seconds:
        return

    rows = read_csv(PROGRESS_HISTORY_CSV)
    rows.append({
        "video_id": video_id,
        "delta_seconds": str(watched_seconds - previous_watched_seconds),
        "previous_watched_seconds": str(previous_watched_seconds),
        "watched_seconds": str(watched_seconds),
        "status": status,
        "logged_at": now_iso(),
    })
    atomic_write_csv(PROGRESS_HISTORY_CSV, PROGRESS_HISTORY_HEADERS, rows)


def get_progress_history_rows() -> List[Dict[str, str]]:
    signature = file_signature(PROGRESS_HISTORY_CSV, PROGRESS_CSV, VIDEOS_CSV)
    if PROGRESS_HISTORY_CACHE["key"] == signature:
        return list(PROGRESS_HISTORY_CACHE["rows"])

    history_rows = read_csv(PROGRESS_HISTORY_CSV)
    history_video_ids = {row.get("video_id", "") for row in history_rows if row.get("video_id")}
    video_map = {row.get("video_id", ""): row for row in read_video_rows() if row.get("video_id")}

    rows: List[Dict[str, str]] = list(history_rows)
    for row in read_csv(PROGRESS_CSV):
        video_id = row.get("video_id", "")
        if not video_id or video_id in history_video_ids:
            continue

        status = str(row.get("status", "")).strip().lower()
        watched_seconds = max(0, parse_int(row.get("watched_seconds", 0), 0))
        video = video_map.get(video_id, {})
        duration_seconds = max(0, parse_int(video.get("duration_seconds", 0), 0))

        if status == "watched" and watched_seconds <= 0:
            watched_seconds = duration_seconds
            logged_at = video.get("published_at", "").strip() or row.get("updated_at", "").strip() or video.get("created_at", "").strip()
        else:
            logged_at = row.get("updated_at", "").strip()

        if watched_seconds <= 0 or not logged_at:
            continue

        rows.append({
            "video_id": video_id,
            "delta_seconds": str(watched_seconds),
            "previous_watched_seconds": "0",
            "watched_seconds": str(watched_seconds),
            "status": status,
            "logged_at": logged_at,
        })

    PROGRESS_HISTORY_CACHE["key"] = signature
    PROGRESS_HISTORY_CACHE["rows"] = list(rows)
    return rows


def collect_system_tags(video: Dict[str, str]) -> List[str]:
    tags: List[str] = []
    if truthy(video.get("deleted", "")):
        tags.append("削除")
    if str(video.get("source", "")).strip().lower() == "manual":
        tags.append("手動追加")
    return tags


def merge_video_data() -> List[Dict[str, Any]]:
    signature = file_signature(VIDEOS_CSV, PROGRESS_CSV, NOTES_CSV)
    if DATA_CACHE["key"] == signature:
        return list(DATA_CACHE["videos"])

    videos = read_video_rows()
    progress_map = get_progress_map()
    notes_map = get_notes_map()
    merged: List[Dict[str, Any]] = []

    for video in videos:
        video_id = video.get("video_id", "")
        duration_seconds = parse_int(video.get("duration_seconds", 0), 0)
        progress = progress_map.get(video_id, {})
        note_row = notes_map.get(video_id, {})

        watched_seconds = max(0, parse_int(progress.get("watched_seconds", 0), 0))
        status = progress.get("status", "") or normalize_status(watched_seconds, duration_seconds)
        if status == "watched" and watched_seconds <= 0 and duration_seconds > 0:
            watched_seconds = duration_seconds

        last_position_seconds = max(0, parse_int(progress.get("last_position_seconds", watched_seconds), watched_seconds))
        if status == "watched" and last_position_seconds <= 0:
            last_position_seconds = watched_seconds
        note = note_row.get("note", "")

        watched_percent = 0.0
        if duration_seconds > 0:
            watched_percent = min(100.0, (watched_seconds / duration_seconds) * 100.0)

        manual_tags = split_tags(video.get("manual_tags", ""))
        all_tags = sorted(
            split_tags(", ".join(collect_system_tags(video) + manual_tags)),
            key=lambda item: item.casefold(),
        )

        merged.append({
            "video_id": video_id,
            "title": video.get("title", ""),
            "url": video.get("url", ""),
            "duration_seconds": duration_seconds,
            "published_at": video.get("published_at", ""),
            "thumbnail_url": video.get("thumbnail_url", ""),
            "channel_id": video.get("channel_id", ""),
            "channel_title": video.get("channel_title", ""),
            "source": video.get("source", "") or "youtube",
            "deleted": truthy(video.get("deleted", "")),
            "status": status,
            "watched_seconds": watched_seconds,
            "watched_time_text": format_seconds(watched_seconds),
            "last_position_seconds": last_position_seconds,
            "watched_percent": round(watched_percent, 1),
            "remaining_seconds": max(0, duration_seconds - watched_seconds) if duration_seconds > 0 else 0,
            "remaining_time_text": format_seconds(max(0, duration_seconds - watched_seconds) if duration_seconds > 0 else 0),
            "note": note,
            "manual_tags": manual_tags,
            "manual_tags_text": join_tags(manual_tags),
            "tags": all_tags,
            "created_at": video.get("created_at", ""),
            "updated_at": video.get("updated_at", ""),
            "watch_url": build_watch_url(video.get("url", ""), watched_seconds),
            "resume_url": build_watch_url(video.get("url", ""), last_position_seconds),
            "thumbnail_download_url": f"/api/thumbnail/{video_id}/download",
        })

    DATA_CACHE["key"] = signature
    DATA_CACHE["videos"] = list(merged)
    DATA_CACHE["summary"] = calculate_summary(merged)
    return merged


def get_cached_summary() -> Dict[str, Any]:
    merge_video_data()
    return dict(DATA_CACHE["summary"])


def calculate_summary(videos: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_count = len(videos)
    watched_count = sum(1 for video in videos if video["status"] == "watched")
    partial_count = sum(1 for video in videos if video["status"] == "partial")
    unseen_count = sum(1 for video in videos if video["status"] == "unseen")
    watched_total_seconds = sum(video["watched_seconds"] for video in videos)
    remaining_total_seconds = sum(video["remaining_seconds"] for video in videos)

    watched_percent = 0.0
    if total_count > 0:
        watched_percent = (watched_count / total_count) * 100.0

    return {
        "total_count": total_count,
        "watched_count": watched_count,
        "partial_count": partial_count,
        "unseen_count": unseen_count,
        "watched_percent": round(watched_percent, 1),
        "watched_total_seconds": watched_total_seconds,
        "remaining_total_seconds": remaining_total_seconds,
        "watched_total_text": format_seconds(watched_total_seconds),
        "remaining_total_text": format_seconds(remaining_total_seconds),
    }


def title_has_exclude_word(title: str, exclude_words: List[str]) -> bool:
    lower_title = title.casefold()
    return any(word.casefold() in lower_title for word in exclude_words)


def matches_terms(text: str, include_terms: List[str], exclude_terms: List[str]) -> bool:
    normalized = text.casefold()
    if any(term not in normalized for term in include_terms):
        return False
    if any(term in normalized for term in exclude_terms):
        return False
    return True


def filter_videos(
    videos: List[Dict[str, Any]],
    keyword: str,
    tag_query: str,
    status: str,
) -> List[Dict[str, Any]]:
    keyword_terms, keyword_excludes = split_search_terms(keyword)
    tag_terms, tag_excludes = split_search_terms(tag_query)
    status = status.strip().lower()

    filtered: List[Dict[str, Any]] = []

    for video in videos:
        searchable_text = " ".join([
            video.get("title", ""),
            video.get("note", ""),
            " ".join(video.get("tags", [])),
            video.get("channel_title", ""),
        ])
        tag_text = " ".join(video.get("tags", []))

        if not matches_terms(searchable_text, keyword_terms, keyword_excludes):
            continue
        if not matches_terms(tag_text, tag_terms, tag_excludes):
            continue
        if status and status != "all" and video.get("status") != status:
            continue

        filtered.append(video)

    return filtered


def filter_videos_without_tag_query(
    videos: List[Dict[str, Any]],
    keyword: str,
    status: str,
) -> List[Dict[str, Any]]:
    keyword_terms, keyword_excludes = split_search_terms(keyword)
    status = status.strip().lower()
    filtered: List[Dict[str, Any]] = []

    for video in videos:
        searchable_text = " ".join([
            video.get("title", ""),
            video.get("note", ""),
            " ".join(video.get("tags", [])),
            video.get("channel_title", ""),
        ])
        if not matches_terms(searchable_text, keyword_terms, keyword_excludes):
            continue
        if status and status != "all" and video.get("status") != status:
            continue
        filtered.append(video)

    return filtered


def sort_videos(videos: List[Dict[str, Any]], sort_name: str) -> List[Dict[str, Any]]:
    sort_name = normalize_sort(sort_name)

    def sort_key(video: Dict[str, Any]) -> Tuple[datetime, datetime]:
        published_at = parse_datetime(video.get("published_at", "")) or datetime.min
        created_at = parse_datetime(video.get("created_at", "")) or datetime.min
        return published_at, created_at

    return sorted(videos, key=sort_key, reverse=(sort_name != "published_asc"))


def tag_entries(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = defaultdict(int)
    for video in videos:
        for tag in video.get("tags", []):
            counts[tag] += 1

    return [
        {"tag": tag, "count": count}
        for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold()))
    ]


def manual_tag_entries(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        for tag in split_tags(row.get("manual_tags", "")):
            counts[tag] += 1

    return [
        {"tag": tag, "count": counts[tag]}
        for tag in sorted(counts.keys(), key=lambda item: item.casefold())
    ]


def get_video_row(video_id: str) -> Dict[str, str]:
    for row in read_video_rows():
        if row.get("video_id") == video_id:
            return row
    raise ValueError(f"動画が見つかりません: {video_id}")


def update_progress(
    video_id: str,
    watched_input: Any,
    mark_watched: bool = False,
    clear_progress: bool = False,
) -> Dict[str, Any]:
    videos = read_video_rows()
    target_video = next((row for row in videos if row.get("video_id") == video_id), None)
    if target_video is None:
        raise ValueError(f"動画が見つかりません: {video_id}")

    duration_seconds = parse_int(target_video.get("duration_seconds", 0), 0)
    watched_seconds = parse_duration_input(watched_input, 0)

    rows = read_csv(PROGRESS_CSV)
    timestamp = now_iso()
    previous_watched_seconds = 0
    previous_index = None

    for index, row in enumerate(rows):
        if row.get("video_id") == video_id:
            previous_index = index
            previous_watched_seconds = max(0, parse_int(row.get("watched_seconds", 0), 0))
            break

    if clear_progress:
        watched_seconds = 0
        last_position_seconds = 0
        status = "unseen"
    elif mark_watched:
        if duration_seconds > 0:
            watched_seconds = duration_seconds
        else:
            watched_seconds = max(watched_seconds, previous_watched_seconds, 1)
        last_position_seconds = watched_seconds
        status = "watched"
    else:
        if duration_seconds > 0:
            watched_seconds = min(watched_seconds, duration_seconds)
            last_position_seconds = watched_seconds
        else:
            watched_seconds = max(0, watched_seconds)
            last_position_seconds = watched_seconds
        status = normalize_status(watched_seconds, duration_seconds)

    payload = {
        "video_id": video_id,
        "status": status,
        "watched_seconds": str(watched_seconds),
        "last_position_seconds": str(last_position_seconds),
        "updated_at": timestamp,
    }

    if previous_index is None:
        rows.append(payload)
    else:
        rows[previous_index] = payload

    atomic_write_csv(PROGRESS_CSV, PROGRESS_HEADERS, rows)
    append_progress_history(video_id, previous_watched_seconds, watched_seconds, status)
    maybe_auto_backup()

    return {
        "video_id": video_id,
        "status": status,
        "watched_seconds": watched_seconds,
        "watched_time_text": format_seconds(watched_seconds),
        "last_position_seconds": last_position_seconds,
    }


def update_note(video_id: str, note: str) -> Dict[str, Any]:
    get_video_row(video_id)
    rows = read_csv(NOTES_CSV)
    timestamp = now_iso()

    for row in rows:
        if row.get("video_id") == video_id:
            row["note"] = note
            row["updated_at"] = timestamp
            atomic_write_csv(NOTES_CSV, NOTE_HEADERS, rows)
            maybe_auto_backup()
            return {"video_id": video_id, "note": note}

    rows.append({
        "video_id": video_id,
        "note": note,
        "updated_at": timestamp,
    })
    atomic_write_csv(NOTES_CSV, NOTE_HEADERS, rows)
    maybe_auto_backup()
    return {"video_id": video_id, "note": note}


def update_video_tags(video_id: str, manual_tags_text: str) -> Dict[str, Any]:
    rows = read_video_rows()
    timestamp = now_iso()

    for row in rows:
        if row.get("video_id") == video_id:
            row["manual_tags"] = join_tags(split_tags(manual_tags_text))
            row["updated_at"] = timestamp
            write_video_rows(rows)
            maybe_auto_backup()
            return {
                "video_id": video_id,
                "manual_tags": split_tags(row["manual_tags"]),
            }

    raise ValueError(f"動画が見つかりません: {video_id}")


def bulk_update_videos(
    video_ids: List[str],
    add_tags_text: str = "",
    remove_tags_text: str = "",
    delete_videos: bool = False,
    mark_watched: bool = False,
    clear_progress: bool = False,
) -> Dict[str, Any]:
    normalized_ids = [str(video_id).strip() for video_id in video_ids if str(video_id).strip()]
    target_ids = list(dict.fromkeys(normalized_ids))
    if not target_ids:
        raise ValueError("対象の動画を選択してください。")

    video_rows = read_video_rows()
    existing_ids = {row.get("video_id", "") for row in video_rows if row.get("video_id")}
    matched_ids = {video_id for video_id in target_ids if video_id in existing_ids}
    if not matched_ids:
        raise ValueError("対象の動画が見つかりません。")

    timestamp = now_iso()
    added_tags = split_tags(add_tags_text)
    removed_tags = split_tags(remove_tags_text)

    if delete_videos:
        kept_video_rows = [row for row in video_rows if row.get("video_id", "") not in matched_ids]
        kept_progress_rows = [row for row in read_csv(PROGRESS_CSV) if row.get("video_id", "") not in matched_ids]
        kept_history_rows = [row for row in read_csv(PROGRESS_HISTORY_CSV) if row.get("video_id", "") not in matched_ids]
        kept_note_rows = [row for row in read_csv(NOTES_CSV) if row.get("video_id", "") not in matched_ids]

        atomic_write_csv(VIDEOS_CSV, VIDEO_HEADERS, kept_video_rows)
        atomic_write_csv(PROGRESS_CSV, PROGRESS_HEADERS, kept_progress_rows)
        atomic_write_csv(PROGRESS_HISTORY_CSV, PROGRESS_HISTORY_HEADERS, kept_history_rows)
        atomic_write_csv(NOTES_CSV, NOTE_HEADERS, kept_note_rows)
        maybe_auto_backup()
        return {
            "deleted_videos": len(matched_ids),
            "changed_videos": len(matched_ids),
            "added_tags": [],
            "removed_tags": [],
        }

    if not added_tags and not removed_tags and not mark_watched and not clear_progress:
        raise ValueError("追加または削除するタグを入力してください。")

    removed_lower = {tag.casefold() for tag in removed_tags}
    changed_videos = 0
    progress_changed_videos = 0
    for row in video_rows:
        if row.get("video_id", "") not in matched_ids:
            continue

        current_tags = split_tags(row.get("manual_tags", ""))
        next_tags = [tag for tag in current_tags if tag.casefold() not in removed_lower]
        existing_lower = {tag.casefold() for tag in next_tags}
        for tag in added_tags:
            lowered = tag.casefold()
            if lowered in existing_lower:
                continue
            next_tags.append(tag)
            existing_lower.add(lowered)

        normalized_next = join_tags(next_tags)
        if normalized_next != join_tags(current_tags):
            row["manual_tags"] = normalized_next
            row["updated_at"] = timestamp
            changed_videos += 1

    progress_rows = read_csv(PROGRESS_CSV) if (mark_watched or clear_progress) else []
    progress_index_map = {
        row.get("video_id", ""): index
        for index, row in enumerate(progress_rows)
        if row.get("video_id", "")
    }
    history_rows = read_csv(PROGRESS_HISTORY_CSV) if (mark_watched or clear_progress) else []
    video_map = {row.get("video_id", ""): row for row in video_rows if row.get("video_id")}

    if mark_watched or clear_progress:
        for video_id in matched_ids:
            video_row = video_map.get(video_id, {})
            duration_seconds = max(0, parse_int(video_row.get("duration_seconds", 0), 0))
            existing_index = progress_index_map.get(video_id)
            existing_row = progress_rows[existing_index] if existing_index is not None else {}
            previous_watched_seconds = max(0, parse_int(existing_row.get("watched_seconds", 0), 0))

            if clear_progress:
                watched_seconds = 0
                last_position_seconds = 0
                status = "unseen"
            else:
                if duration_seconds > 0:
                    watched_seconds = duration_seconds
                else:
                    watched_seconds = max(previous_watched_seconds, 1)
                last_position_seconds = watched_seconds
                status = "watched"

            payload = {
                "video_id": video_id,
                "status": status,
                "watched_seconds": str(watched_seconds),
                "last_position_seconds": str(last_position_seconds),
                "updated_at": timestamp,
            }

            if (
                existing_row
                and str(existing_row.get("status", "")) == status
                and parse_int(existing_row.get("watched_seconds", 0), 0) == watched_seconds
                and parse_int(existing_row.get("last_position_seconds", 0), 0) == last_position_seconds
            ):
                continue

            if existing_index is None:
                progress_rows.append(payload)
                progress_index_map[video_id] = len(progress_rows) - 1
            else:
                progress_rows[existing_index] = payload

            if previous_watched_seconds != watched_seconds:
                history_rows.append({
                    "video_id": video_id,
                    "delta_seconds": str(watched_seconds - previous_watched_seconds),
                    "previous_watched_seconds": str(previous_watched_seconds),
                    "watched_seconds": str(watched_seconds),
                    "status": status,
                    "logged_at": timestamp,
                })
            progress_changed_videos += 1

    if changed_videos == 0 and progress_changed_videos == 0:
        raise ValueError("変更対象のタグがありません。")

    write_video_rows(video_rows)
    if mark_watched or clear_progress:
        atomic_write_csv(PROGRESS_CSV, PROGRESS_HEADERS, progress_rows)
        atomic_write_csv(PROGRESS_HISTORY_CSV, PROGRESS_HISTORY_HEADERS, history_rows)
    maybe_auto_backup()
    return {
        "deleted_videos": 0,
        "changed_videos": changed_videos,
        "progress_changed_videos": progress_changed_videos,
        "added_tags": added_tags,
        "removed_tags": removed_tags,
        "mark_watched": mark_watched,
        "clear_progress": clear_progress,
    }


def rename_manual_tag_across_videos(old_tag: str, new_tag: str) -> Dict[str, Any]:
    old_tag = old_tag.strip()
    new_tag = new_tag.strip()
    if not old_tag or not new_tag:
        raise ValueError("変更前と変更後のタグが必要です。")
    if old_tag.casefold() == new_tag.casefold():
        raise ValueError("変更前と変更後のタグが同じです。")

    rows = read_video_rows()
    timestamp = now_iso()
    changed_count = 0

    for row in rows:
        tags = split_tags(row.get("manual_tags", ""))
        updated_tags = [new_tag if tag.casefold() == old_tag.casefold() else tag for tag in tags]
        if tags != updated_tags:
            row["manual_tags"] = join_tags(updated_tags)
            row["updated_at"] = timestamp
            changed_count += 1

    if changed_count == 0:
        raise ValueError("対象の手動タグが見つかりません。")

    write_video_rows(rows)
    maybe_auto_backup()
    return {"changed_videos": changed_count, "old_tag": old_tag, "new_tag": new_tag}


def delete_manual_tag_across_videos(target_tag: str) -> Dict[str, Any]:
    target_tag = target_tag.strip()
    if not target_tag:
        raise ValueError("削除するタグが必要です。")

    rows = read_video_rows()
    timestamp = now_iso()
    changed_count = 0

    for row in rows:
        tags = split_tags(row.get("manual_tags", ""))
        updated_tags = [tag for tag in tags if tag.casefold() != target_tag.casefold()]
        if tags != updated_tags:
            row["manual_tags"] = join_tags(updated_tags)
            row["updated_at"] = timestamp
            changed_count += 1

    if changed_count == 0:
        raise ValueError("対象の手動タグが見つかりません。")

    write_video_rows(rows)
    maybe_auto_backup()
    return {"changed_videos": changed_count, "deleted_tag": target_tag}


def extract_video_id_from_url(url: str) -> str:
    if not url:
        return ""

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [part for part in parsed.path.split("/") if part]

    if host.endswith("youtu.be") and path_parts:
        return path_parts[0]

    if "youtube.com" not in host:
        return ""

    if parsed.path == "/watch":
        return parse_qs(parsed.query).get("v", [""])[0]

    if path_parts and path_parts[0] in {"shorts", "live", "embed"} and len(path_parts) > 1:
        return path_parts[1]

    return ""


def make_thumbnail_url(video_id: str) -> str:
    if not video_id or video_id.startswith("manual-"):
        return ""
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


def make_uploaded_thumbnail_url(filename: str) -> str:
    return f"/uploads/{filename}"


def save_uploaded_image(file_storage: Any, base_name: str, fallback: str = "upload") -> str:
    if file_storage is None:
        return ""

    filename = str(getattr(file_storage, "filename", "") or "").strip()
    if not filename:
        return ""

    extension = os.path.splitext(filename)[1].lower() or ".jpg"
    safe_name = slugify_filename(base_name, fallback)
    final_name = f"{safe_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}{extension}"
    path = os.path.join(UPLOAD_DIR, final_name)
    file_storage.save(path)
    return make_uploaded_thumbnail_url(final_name)


def save_uploaded_thumbnail(file_storage: Any, title: str, video_id: str) -> str:
    return save_uploaded_image(file_storage, title or video_id, video_id)


def build_manual_title(title: str, url: str, video_id: str) -> str:
    title = title.strip()
    if title:
        return title
    if video_id and not video_id.startswith("manual-"):
        return f"手動追加 {video_id}"
    if url.strip():
        return f"手動追加 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    raise ValueError("URLかタイトルを入力してください。")


def add_manual_video(
    title: str,
    url: str,
    duration_input: Any,
    manual_tags_text: str,
    note: str = "",
    watched_input: Any = 0,
    mark_watched: bool = False,
    thumbnail_file: Any = None,
) -> Dict[str, Any]:
    url = url.strip()
    video_id = extract_video_id_from_url(url)
    if not video_id:
        video_id = f"manual-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    title = build_manual_title(title, url, video_id)
    duration_seconds = parse_duration_input(duration_input, 0)
    rows = read_video_rows()
    if any(row.get("video_id") == video_id for row in rows):
        raise ValueError("同じ動画IDの項目が既に存在します。")

    timestamp = now_iso()
    thumbnail_url = save_uploaded_thumbnail(thumbnail_file, title, video_id) or make_thumbnail_url(video_id)
    rows.append({
        "video_id": video_id,
        "title": title,
        "url": url,
        "duration_seconds": str(duration_seconds),
        "published_at": now_utc_iso(),
        "thumbnail_url": thumbnail_url,
        "channel_id": "",
        "channel_title": "",
        "source": "manual",
        "manual_tags": join_tags(split_tags(manual_tags_text)),
        "youtube_tags": "",
        "deleted": "0",
        "last_seen_at": "",
        "created_at": timestamp,
        "updated_at": timestamp,
    })
    write_video_rows(rows)

    if note.strip():
        update_note(video_id, note)
    if watched_input or mark_watched:
        update_progress(video_id, watched_input, mark_watched=mark_watched)

    maybe_auto_backup()
    return {"video_id": video_id, "title": title, "thumbnail_url": thumbnail_url}


def create_backup() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    os.makedirs(backup_path, exist_ok=True)

    for file_path in [VIDEOS_CSV, PROGRESS_CSV, PROGRESS_HISTORY_CSV, NOTES_CSV, CONFIG_JSON]:
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_path)

    return backup_name


def list_backups() -> List[str]:
    if not os.path.exists(BACKUP_DIR):
        return []
    return sorted(
        [name for name in os.listdir(BACKUP_DIR) if os.path.isdir(os.path.join(BACKUP_DIR, name))],
        reverse=True,
    )


def prune_backups(limit: int) -> None:
    for backup_name in list_backups()[max(1, limit):]:
        shutil.rmtree(os.path.join(BACKUP_DIR, backup_name), ignore_errors=True)


def latest_backup_time() -> Optional[datetime]:
    backups = list_backups()
    if not backups:
        return None
    latest = backups[0].replace("backup_", "", 1)
    try:
        return datetime.strptime(latest, "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def maybe_auto_backup(force: bool = False) -> Optional[str]:
    config = load_config()
    latest_time = latest_backup_time()
    if not force and latest_time is not None and datetime.now() - latest_time < AUTO_BACKUP_INTERVAL:
        prune_backups(config.get("backup_limit", DEFAULT_CONFIG["backup_limit"]))
        return None

    backup_name = create_backup()
    prune_backups(config.get("backup_limit", DEFAULT_CONFIG["backup_limit"]))
    return backup_name


def chunked(values: List[str], size: int) -> List[List[str]]:
    return [values[index:index + size] for index in range(0, len(values), size)]


def parse_iso8601_duration(value: str) -> int:
    if not value:
        return 0

    pattern = re.compile(
        r"^P(?:(?P<days>\d+)D)?T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?$"
    )
    match = pattern.match(value)
    if not match:
        return 0

    days = parse_int(match.group("days"), 0)
    hours = parse_int(match.group("hours"), 0)
    minutes = parse_int(match.group("minutes"), 0)
    seconds = parse_int(match.group("seconds"), 0)
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def pick_thumbnail(thumbnails: Dict[str, Any]) -> str:
    for key in ("maxres", "standard", "high", "medium", "default"):
        candidate = thumbnails.get(key, {})
        url = candidate.get("url", "")
        if url:
            return url
    return ""


def youtube_api_request(resource: str, params: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    query = {key: value for key, value in params.items() if value not in (None, "")}
    query["key"] = api_key
    url = f"{YOUTUBE_API_BASE}/{resource}?{urlencode(query)}"
    request_obj = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urlopen(request_obj, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        try:
            payload = json.loads(error.read().decode("utf-8"))
            message = payload.get("error", {}).get("message", str(error))
        except (json.JSONDecodeError, UnicodeDecodeError):
            message = str(error)
        raise ValueError(f"YouTube APIエラー: {message}") from error
    except URLError as error:
        raise ValueError(f"YouTube APIへ接続できませんでした: {error}") from error


def normalize_channel_reference(channel_reference: str) -> str:
    reference = channel_reference.strip()
    if not reference:
        return ""

    if reference.startswith("UC") or reference.startswith("@"):
        return reference

    parsed = urlparse(reference)
    if parsed.scheme and parsed.netloc:
        parts = [part for part in parsed.path.split("/") if part]
        if not parts:
            return reference
        if parts[0] == "channel" and len(parts) > 1:
            return parts[1]
        if parts[0].startswith("@"):
            return parts[0]
        if parts[0] == "user" and len(parts) > 1:
            return parts[1]
        if parts[0] == "c" and len(parts) > 1:
            return parts[1]

    return reference


def normalize_channel_detail(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "channel_reference": normalize_channel_reference(item.get("channel_reference", "")),
        "channel_id": str(item.get("channel_id", "")).strip(),
        "channel_title": str(item.get("channel_title", "")).strip(),
        "uploads_playlist_id": str(item.get("uploads_playlist_id", "")).strip(),
    }


def channel_details_from_config(config: Dict[str, Any]) -> List[Dict[str, str]]:
    raw_details = config.get("channel_details", [])
    details: List[Dict[str, str]] = []

    if isinstance(raw_details, list):
        for item in raw_details:
            if not isinstance(item, dict):
                continue
            detail = normalize_channel_detail(item)
            if all(detail.values()):
                details.append(detail)

    if details:
        return details

    references = split_channel_references(config.get("channel_reference", ""))
    if (
        len(references) == 1
        and config.get("channel_id")
        and config.get("channel_title")
        and config.get("uploads_playlist_id")
    ):
        return [{
            "channel_reference": references[0],
            "channel_id": str(config.get("channel_id", "")).strip(),
            "channel_title": str(config.get("channel_title", "")).strip(),
            "uploads_playlist_id": str(config.get("uploads_playlist_id", "")).strip(),
        }]

    return []


def sync_primary_channel_fields(config: Dict[str, Any], channel_details: List[Dict[str, str]]) -> None:
    if not channel_details:
        config["channel_id"] = ""
        config["channel_title"] = ""
        config["uploads_playlist_id"] = ""
        config["channel_details"] = []
        return

    primary = channel_details[0]
    config["channel_id"] = primary.get("channel_id", "")
    config["channel_title"] = primary.get("channel_title", "")
    config["uploads_playlist_id"] = primary.get("uploads_playlist_id", "")
    config["channel_details"] = [normalize_channel_detail(item) for item in channel_details]


def resolve_channel_details(api_key: str, channel_reference: str) -> Dict[str, str]:
    reference = normalize_channel_reference(channel_reference)
    if not reference:
        raise ValueError("チャンネルIDまたは @handle を入力してください。")

    request_candidates: List[Dict[str, Any]] = []
    if reference.startswith("UC"):
        request_candidates.append({"id": reference})
    if reference.startswith("@"):
        request_candidates.append({"forHandle": reference.lstrip("@")})
    if not reference.startswith("UC"):
        request_candidates.append({"forUsername": reference.lstrip("@")})

    tried = set()
    for candidate in request_candidates:
        key = tuple(sorted(candidate.items()))
        if key in tried:
            continue
        tried.add(key)

        payload = youtube_api_request(
            "channels",
            {
                "part": "snippet,contentDetails",
                **candidate,
            },
            api_key,
        )
        items = payload.get("items", [])
        if not items:
            continue

        channel = items[0]
        uploads_playlist_id = (
            channel.get("contentDetails", {})
            .get("relatedPlaylists", {})
            .get("uploads", "")
        )
        if not uploads_playlist_id:
            raise ValueError("チャンネルのアップロード一覧を取得できませんでした。")

        return {
            "channel_id": channel.get("id", ""),
            "channel_title": channel.get("snippet", {}).get("title", ""),
            "uploads_playlist_id": uploads_playlist_id,
        }

    raise ValueError("チャンネルが見つかりません。UCから始まるチャンネルIDか @handle を指定してください。")


def resolve_channel_details_list(api_key: str, channel_reference_text: str) -> List[Dict[str, str]]:
    references = split_channel_references(channel_reference_text)
    if not references:
        raise ValueError("チャンネルIDまたはURLを1件以上入力してください。")

    details: List[Dict[str, str]] = []
    seen_channel_ids = set()
    for reference in references:
        detail = resolve_channel_details(api_key, reference)
        detail["channel_reference"] = reference
        lowered = detail.get("channel_id", "").casefold()
        if lowered in seen_channel_ids:
            continue
        seen_channel_ids.add(lowered)
        details.append(normalize_channel_detail(detail))
    return details


def fetch_upload_entries(api_key: str, uploads_playlist_id: str) -> List[Dict[str, Any]]:
    collected: List[Dict[str, Any]] = []
    seen_ids = set()
    page_token = ""

    while True:
        payload = youtube_api_request(
            "playlistItems",
            {
                "part": "snippet,contentDetails",
                "playlistId": uploads_playlist_id,
                "maxResults": 50,
                "pageToken": page_token,
            },
            api_key,
        )

        for item in payload.get("items", []):
            snippet = item.get("snippet", {})
            video_id = (
                item.get("contentDetails", {}).get("videoId", "")
                or snippet.get("resourceId", {}).get("videoId", "")
            )
            if not video_id or video_id in seen_ids:
                continue

            seen_ids.add(video_id)
            collected.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail_url": pick_thumbnail(snippet.get("thumbnails", {})),
            })

        page_token = payload.get("nextPageToken", "")
        if not page_token:
            break

    return collected


def fetch_video_details(api_key: str, video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    detail_map: Dict[str, Dict[str, Any]] = {}

    for batch in chunked(video_ids, 50):
        payload = youtube_api_request(
            "videos",
            {
                "part": "snippet,contentDetails",
                "id": ",".join(batch),
                "maxResults": 50,
            },
            api_key,
        )

        for item in payload.get("items", []):
            snippet = item.get("snippet", {})
            detail_map[item.get("id", "")] = {
                "video_id": item.get("id", ""),
                "title": snippet.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={item.get('id', '')}",
                "duration_seconds": parse_iso8601_duration(item.get("contentDetails", {}).get("duration", "")),
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail_url": pick_thumbnail(snippet.get("thumbnails", {})),
                "youtube_tags": join_tags(snippet.get("tags", [])) if "tags" in snippet else None,
            }

    return detail_map


def detail_refresh_candidates(upload_entries: List[Dict[str, Any]], video_map: Dict[str, Dict[str, str]]) -> List[str]:
    candidates: List[str] = []
    for index, entry in enumerate(upload_entries):
        video_id = entry["video_id"]
        existing = video_map.get(video_id, {})
        if (
            not existing
            or parse_int(existing.get("duration_seconds", 0), 0) <= 0
            or index < RECENT_DETAILS_REFRESH_LIMIT
        ):
            candidates.append(video_id)
    return candidates


def remove_excluded_synced_tags(tags: List[str], excluded_tags: List[str]) -> List[str]:
    if not excluded_tags:
        return tags
    excluded_lower = {tag.casefold() for tag in excluded_tags}
    return [tag for tag in tags if tag.casefold() not in excluded_lower]


def append_title_history(notes_map: Dict[str, Dict[str, str]], video_id: str, old_title: str) -> None:
    old_title = old_title.strip()
    if not old_title:
        return

    timestamp = now_iso()
    title_note = f"[旧タイトル {timestamp}] {old_title}"
    existing = notes_map.get(video_id, {})
    current_note = existing.get("note", "").strip()
    next_note = title_note if not current_note else f"{current_note}\n{title_note}"
    notes_map[video_id] = {
        "video_id": video_id,
        "note": next_note,
        "updated_at": timestamp,
    }


def materially_changed(old_row: Dict[str, str], new_row: Dict[str, str]) -> bool:
    tracked_fields = [
        "title",
        "url",
        "duration_seconds",
        "published_at",
        "thumbnail_url",
        "channel_id",
        "channel_title",
        "source",
        "manual_tags",
        "youtube_tags",
        "deleted",
    ]
    return any((old_row.get(field, "") or "") != (new_row.get(field, "") or "") for field in tracked_fields)


def merge_synced_tags(
    existing_row: Dict[str, str],
    fetched_tags_raw: Optional[str],
    excluded_tags: List[str],
) -> Tuple[str, str]:
    current_tags = split_tags(existing_row.get("manual_tags", ""))
    previous_fetched_tags = split_tags(existing_row.get("youtube_tags", ""))
    fetched_tags = remove_excluded_synced_tags(split_tags(fetched_tags_raw or ""), excluded_tags)

    removed_fetched = {
        tag.casefold()
        for tag in previous_fetched_tags
        if all(tag.casefold() != current.casefold() for current in current_tags)
    }

    next_tags = list(current_tags)
    existing_lower = {tag.casefold() for tag in next_tags}
    for tag in fetched_tags:
        lowered = tag.casefold()
        if lowered in removed_fetched or lowered in existing_lower:
            continue
        next_tags.append(tag)
        existing_lower.add(lowered)

    return join_tags(next_tags), join_tags(fetched_tags)


def apply_sync_tag_exclusions_to_rows(rows: List[Dict[str, str]], excluded_tags: List[str]) -> int:
    if not excluded_tags:
        return 0

    excluded_lower = {tag.casefold() for tag in excluded_tags}
    changed = 0
    timestamp = now_iso()
    for row in rows:
        current_tags = split_tags(row.get("manual_tags", ""))
        synced_tags = split_tags(row.get("youtube_tags", ""))
        youtube_source = str(row.get("source", "")).strip().lower() == "youtube"
        next_tags = [
            tag
            for tag in current_tags
            if not (tag.casefold() in excluded_lower and youtube_source)
        ]
        next_synced_tags = [tag for tag in synced_tags if tag.casefold() not in excluded_lower]
        if current_tags != next_tags or synced_tags != next_synced_tags:
            row["manual_tags"] = join_tags(next_tags)
            row["youtube_tags"] = join_tags(next_synced_tags)
            row["updated_at"] = timestamp
            changed += 1
    return changed


def apply_sync_tag_exclusions_to_existing(sync_excluded_tags_text: Optional[str] = None) -> Dict[str, Any]:
    config = load_config()
    if sync_excluded_tags_text is not None:
        config["sync_excluded_tags"] = sync_excluded_tags_text
        config = save_config(config)

    rows = read_video_rows()
    changed = apply_sync_tag_exclusions_to_rows(rows, split_tags(config.get("sync_excluded_tags", "")))
    if changed:
        write_video_rows(rows)
        maybe_auto_backup()

    videos = merge_video_data()
    return {
        "changed_videos": changed,
        "settings": build_settings_payload(config),
        "tag_entries": tag_entries(videos),
    }


def sync_channel_videos() -> Dict[str, Any]:
    config = load_config()
    api_key = config.get("youtube_api_key", "").strip()
    channel_reference_text = config.get("channel_reference", "").strip()
    channel_references = split_channel_references(channel_reference_text)
    if not api_key or not channel_references:
        raise ValueError("YouTube APIキーとチャンネル設定が必要です。")

    timestamp = now_iso()

    try:
        excluded_sync_tags = split_tags(config.get("sync_excluded_tags", ""))
        channels = channel_details_from_config(config)
        if len(channels) != len(channel_references):
            channels = resolve_channel_details_list(api_key, channel_reference_text)

        video_rows = read_video_rows()
        notes_rows = read_csv(NOTES_CSV)
        video_map = {row["video_id"]: row for row in video_rows if row.get("video_id")}
        notes_map = {row["video_id"]: row for row in notes_rows if row.get("video_id")}
        upload_entries_by_channel: Dict[str, List[Dict[str, Any]]] = {}
        merged_upload_entries: List[Dict[str, Any]] = []
        for channel in channels:
            entries = fetch_upload_entries(api_key, channel["uploads_playlist_id"])
            upload_entries_by_channel[channel["channel_id"]] = entries
            merged_upload_entries.extend(entries)

        detail_ids = detail_refresh_candidates(merged_upload_entries, video_map)
        detail_map = fetch_video_details(api_key, detail_ids) if detail_ids else {}

        stats = {
            "added": 0,
            "updated": 0,
            "deleted": 0,
            "restored": 0,
            "title_changes": 0,
            "fetched": len(merged_upload_entries),
        }
        active_ids_by_channel: Dict[str, set] = defaultdict(set)

        for channel in channels:
            upload_entries = upload_entries_by_channel.get(channel["channel_id"], [])
            for entry in upload_entries:
                video_id = entry["video_id"]
                active_ids_by_channel[channel["channel_id"]].add(video_id)
                existing = video_map.get(video_id, {})
                previous_deleted = truthy(existing.get("deleted", ""))

                if existing and existing.get("title", "").strip() and existing.get("title", "").strip() != entry["title"].strip():
                    append_title_history(notes_map, video_id, existing.get("title", ""))
                    stats["title_changes"] += 1

                details = detail_map.get(video_id, {})
                merged_tags, youtube_tags = merge_synced_tags(
                    existing,
                    details.get("youtube_tags", existing.get("youtube_tags", "")),
                    excluded_sync_tags,
                )

                updated_row = {
                    "video_id": video_id,
                    "title": entry["title"] or existing.get("title", ""),
                    "url": entry["url"] or existing.get("url", ""),
                    "duration_seconds": str(parse_int(details.get("duration_seconds", existing.get("duration_seconds", 0)), 0)),
                    "published_at": entry["published_at"] or existing.get("published_at", ""),
                    "thumbnail_url": details.get("thumbnail_url") or entry["thumbnail_url"] or existing.get("thumbnail_url", ""),
                    "channel_id": channel["channel_id"],
                    "channel_title": channel["channel_title"],
                    "source": "youtube",
                    "manual_tags": merged_tags,
                    "youtube_tags": youtube_tags or "",
                    "deleted": "0",
                    "last_seen_at": timestamp,
                    "created_at": existing.get("created_at", "") or timestamp,
                    "updated_at": timestamp,
                }

                if not existing:
                    stats["added"] += 1
                elif previous_deleted:
                    stats["restored"] += 1
                elif materially_changed(existing, updated_row):
                    stats["updated"] += 1

                video_map[video_id] = updated_row

        synced_channel_ids = {channel["channel_id"] for channel in channels}
        for row in video_map.values():
            if row.get("source", "") != "youtube":
                continue
            row_channel_id = row.get("channel_id", "")
            if row_channel_id not in synced_channel_ids:
                continue
            if row.get("video_id", "") in active_ids_by_channel.get(row_channel_id, set()):
                continue
            if not truthy(row.get("deleted", "")):
                row["deleted"] = "1"
                row["updated_at"] = timestamp
                stats["deleted"] += 1

        final_video_rows = sorted(
            video_map.values(),
            key=lambda row: (
                parse_datetime(row.get("published_at", "")) or datetime.min,
                parse_datetime(row.get("created_at", "")) or datetime.min,
            ),
            reverse=True,
        )
        final_notes_rows = sorted(
            notes_map.values(),
            key=lambda row: parse_datetime(row.get("updated_at", "")) or datetime.min,
            reverse=True,
        )

        atomic_write_csv(VIDEOS_CSV, VIDEO_HEADERS, final_video_rows)
        atomic_write_csv(NOTES_CSV, NOTE_HEADERS, final_notes_rows)

        sync_primary_channel_fields(config, channels)
        config.update({
            "last_synced_at": timestamp,
            "last_sync_status": "success",
            "last_sync_message": (
                f"同期完了: 追加 {stats['added']} / 更新 {stats['updated']} / "
                f"削除 {stats['deleted']} / タイトル変更 {stats['title_changes']}"
            ),
        })
        save_config(config)
        maybe_auto_backup(force=True)
        return {"stats": stats, "sync": build_sync_info(config)}
    except Exception as error:
        config.update({
            "last_sync_status": "error",
            "last_sync_message": str(error),
        })
        save_config(config)
        raise


def should_auto_sync(config: Dict[str, Any]) -> bool:
    if not config.get("youtube_api_key") or not split_channel_references(config.get("channel_reference", "")):
        return False
    if SYNC_STATE.get("running"):
        return False
    last_synced_at = parse_datetime(config.get("last_synced_at", ""))
    if last_synced_at is None:
        return True
    delta = datetime.now() - last_synced_at
    return delta >= timedelta(minutes=max(1, parse_int(config.get("auto_sync_minutes", 30), 30)))


def run_sync_job() -> None:
    try:
        sync_channel_videos()
    finally:
        with SYNC_LOCK:
            SYNC_STATE["running"] = False
            SYNC_STATE["started_at"] = ""
            SYNC_STATE["mode"] = ""


def start_background_sync(mode: str = "manual") -> Dict[str, Any]:
    config = load_config()
    if not config.get("youtube_api_key") or not split_channel_references(config.get("channel_reference", "")):
        return build_sync_info(config)

    with SYNC_LOCK:
        if not SYNC_STATE["running"]:
            SYNC_STATE["running"] = True
            SYNC_STATE["started_at"] = now_iso()
            SYNC_STATE["mode"] = mode
            config.update({
                "last_sync_status": "syncing",
                "last_sync_message": "同期中",
            })
            save_config(config)
            thread = threading.Thread(target=run_sync_job, daemon=True)
            thread.start()

    return build_sync_info(load_config())


def maybe_auto_sync() -> Dict[str, Any]:
    config = load_config()
    if not should_auto_sync(config):
        return build_sync_info(config)
    return start_background_sync(mode="auto")


def prune_app_clients(now_monotonic: Optional[float] = None) -> None:
    current = monotonic_now() if now_monotonic is None else float(now_monotonic)
    clients = APP_LIFECYCLE_STATE["clients"]
    stale_tab_ids = [
        tab_id
        for tab_id, last_seen in list(clients.items())
        if current - float(last_seen) > APP_CLIENT_TTL_SECONDS
    ]
    for tab_id in stale_tab_ids:
        clients.pop(tab_id, None)


def register_app_client(tab_id: str) -> None:
    with APP_CLIENT_LOCK:
        prune_app_clients()
        APP_LIFECYCLE_STATE["clients"][tab_id] = monotonic_now()
        APP_LIFECYCLE_STATE["armed"] = True
        APP_LIFECYCLE_STATE["zero_clients_since"] = None


def touch_app_client(tab_id: str) -> bool:
    with APP_CLIENT_LOCK:
        prune_app_clients()
        if tab_id not in APP_LIFECYCLE_STATE["clients"]:
            return False
        APP_LIFECYCLE_STATE["clients"][tab_id] = monotonic_now()
        APP_LIFECYCLE_STATE["zero_clients_since"] = None
        return True


def unregister_app_client(tab_id: str) -> None:
    with APP_CLIENT_LOCK:
        prune_app_clients()
        APP_LIFECYCLE_STATE["clients"].pop(tab_id, None)
        if APP_LIFECYCLE_STATE["armed"] and not APP_LIFECYCLE_STATE["clients"]:
            APP_LIFECYCLE_STATE["zero_clients_since"] = monotonic_now()


def active_app_client_count() -> int:
    with APP_CLIENT_LOCK:
        prune_app_clients()
        return len(APP_LIFECYCLE_STATE["clients"])


def reset_app_lifecycle_state() -> None:
    with APP_CLIENT_LOCK:
        APP_LIFECYCLE_STATE["clients"].clear()
        APP_LIFECYCLE_STATE["armed"] = False
        APP_LIFECYCLE_STATE["zero_clients_since"] = None


def request_server_shutdown(reason: str = "") -> None:
    server = SERVER_STATE.get("server")
    if SERVER_STATE.get("shutdown_requested"):
        return
    SERVER_STATE["shutdown_requested"] = True
    if reason:
        print(f"YAM auto-exit: {reason}")
    if isinstance(server, BaseWSGIServer):
        threading.Thread(target=server.shutdown, daemon=True).start()


def lifecycle_monitor_loop() -> None:
    while not SERVER_STATE.get("shutdown_requested"):
        time.sleep(APP_AUTO_EXIT_POLL_SECONDS)
        if not runtime_auto_exit():
            continue

        shutdown_due = False
        with APP_CLIENT_LOCK:
            current = monotonic_now()
            prune_app_clients(current)
            clients = APP_LIFECYCLE_STATE["clients"]
            armed = bool(APP_LIFECYCLE_STATE["armed"])
            zero_clients_since = APP_LIFECYCLE_STATE["zero_clients_since"]

            if clients:
                APP_LIFECYCLE_STATE["zero_clients_since"] = None
            elif armed:
                if zero_clients_since is None:
                    APP_LIFECYCLE_STATE["zero_clients_since"] = current
                elif current - float(zero_clients_since) >= APP_AUTO_EXIT_GRACE_SECONDS:
                    shutdown_due = True

        if shutdown_due:
            request_server_shutdown("last browser tab was closed")
            return


def shift_months(base: datetime, months: int) -> datetime:
    year = base.year + ((base.month - 1 + months) // 12)
    month = ((base.month - 1 + months) % 12) + 1
    return datetime(year, month, 1)


def normalize_chart_offset(value: Any) -> int:
    return min(0, parse_int(value, 0))


def build_time_buckets(granularity: str, chart_offset: int = 0) -> List[Tuple[str, str]]:
    chart_offset = normalize_chart_offset(chart_offset)
    now = datetime.now()
    if granularity == "month":
        current = shift_months(datetime(now.year, now.month, 1), chart_offset * MONTH_CHART_POINTS)
        buckets = []
        for offset in range(-(MONTH_CHART_POINTS - 1), 1):
            bucket = shift_months(current, offset)
            buckets.append((bucket.strftime("%Y-%m"), bucket.strftime("%Y/%m")))
        return buckets

    end_day = datetime(now.year, now.month, now.day) + timedelta(days=chart_offset * DAY_CHART_POINTS)
    start_day = end_day - timedelta(days=DAY_CHART_POINTS - 1)
    buckets = []
    for offset in range(DAY_CHART_POINTS):
        day = start_day + timedelta(days=offset)
        buckets.append((day.strftime("%Y-%m-%d"), day.strftime("%m/%d")))
    return buckets


def history_bucket_key(moment: datetime, granularity: str) -> str:
    return moment.strftime("%Y-%m") if granularity == "month" else moment.strftime("%Y-%m-%d")


def build_bucket_range(granularity: str, start_at: datetime, end_at: datetime) -> List[str]:
    if end_at < start_at:
        return []

    if granularity == "month":
        current = datetime(start_at.year, start_at.month, 1)
        last = datetime(end_at.year, end_at.month, 1)
        keys: List[str] = []
        while current <= last:
            keys.append(current.strftime("%Y-%m"))
            current = shift_months(current, 1)
        return keys

    current = datetime(start_at.year, start_at.month, start_at.day)
    last = datetime(end_at.year, end_at.month, end_at.day)
    keys = []
    while current <= last:
        keys.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return keys


def build_progress_chart(granularity: str, chart_offset: int = 0) -> Dict[str, Any]:
    buckets = build_time_buckets(granularity, chart_offset)
    bucket_map = {key: 0 for key, _ in buckets}
    bucket_items: Dict[str, Dict[str, Dict[str, Any]]] = {key: {} for key, _ in buckets}
    all_bucket_totals: Dict[str, int] = defaultdict(int)
    history_rows = get_progress_history_rows()
    video_lookup = {video.get("video_id", ""): video for video in merge_video_data() if video.get("video_id")}

    history_moments: List[datetime] = []
    for row in history_rows:
        logged_at = parse_datetime(row.get("logged_at", ""))
        if logged_at is None:
            continue

        history_moments.append(logged_at)
        key = history_bucket_key(logged_at, granularity)
        delta_seconds = parse_int(row.get("delta_seconds", 0), 0)
        all_bucket_totals[key] += delta_seconds

        if key not in bucket_map:
            continue

        bucket_map[key] += delta_seconds
        video_id = row.get("video_id", "")
        video = video_lookup.get(video_id, {})
        item = bucket_items[key].setdefault(video_id, {
            "video_id": video_id,
            "title": video.get("title", "") or video_id or "不明な動画",
            "url": video.get("url", ""),
            "thumbnail_url": video.get("thumbnail_url", ""),
            "seconds": 0,
        })
        item["seconds"] += delta_seconds

    points = []
    for key, label in buckets:
        seconds = bucket_map.get(key, 0)
        items = sorted(
            bucket_items.get(key, {}).values(),
            key=lambda item: (-abs(parse_int(item.get("seconds", 0), 0)), str(item.get("title", "")).casefold()),
        )
        points.append({
            "key": key,
            "label": label,
            "seconds": seconds,
            "text": format_seconds(abs(seconds)),
            "is_negative": seconds < 0,
            "items": [
                {
                    "video_id": item.get("video_id", ""),
                    "title": item.get("title", "") or "不明な動画",
                    "url": item.get("url", ""),
                    "thumbnail_url": item.get("thumbnail_url", ""),
                    "seconds": parse_int(item.get("seconds", 0), 0),
                    "text": format_seconds(abs(parse_int(item.get("seconds", 0), 0))),
                    "is_negative": parse_int(item.get("seconds", 0), 0) < 0,
                }
                for item in items
                if parse_int(item.get("seconds", 0), 0) != 0
            ],
        })

    total_seconds = sum(point["seconds"] for point in points)
    window_average_seconds = int(total_seconds / len(points)) if points else 0

    if history_moments:
        overall_bucket_keys = build_bucket_range(granularity, min(history_moments), max(history_moments))
    else:
        overall_bucket_keys = []
    overall_total_seconds = sum(all_bucket_totals.get(key, 0) for key in overall_bucket_keys)
    overall_average_seconds = int(overall_total_seconds / len(overall_bucket_keys)) if overall_bucket_keys else 0

    return {
        "points": points,
        "total_seconds": total_seconds,
        "total_text": format_seconds(abs(total_seconds)),
        "average_seconds": window_average_seconds,
        "average_text": format_seconds(abs(window_average_seconds)),
        "window_average_seconds": window_average_seconds,
        "window_average_text": format_seconds(abs(window_average_seconds)),
        "overall_average_seconds": overall_average_seconds,
        "overall_average_text": format_seconds(abs(overall_average_seconds)),
        "displayed_bucket_count": len(points),
        "overall_bucket_count": len(overall_bucket_keys),
        "offset": normalize_chart_offset(chart_offset),
        "has_next": normalize_chart_offset(chart_offset) < 0,
    }


def matches_query_text(video: Dict[str, Any], raw_query: str) -> bool:
    include_terms, exclude_terms = split_search_terms(raw_query)
    searchable_text = " ".join([
        video.get("title", ""),
        video.get("note", ""),
        " ".join(video.get("tags", [])),
        video.get("channel_title", ""),
    ])
    return matches_terms(searchable_text, include_terms, exclude_terms)


def calculate_tag_ratio(videos: List[Dict[str, Any]], filter_query: str) -> Dict[str, Any]:
    active_videos = [video for video in videos if not video.get("deleted")]
    matching_videos = [video for video in active_videos if matches_query_text(video, filter_query)] if filter_query.strip() else []
    matching_count = len(matching_videos)
    total_count = len(active_videos)
    ratio_percent = (matching_count / total_count * 100.0) if total_count else 0.0
    return {
        "filter_query": filter_query,
        "matching_count": matching_count,
        "other_count": max(0, total_count - matching_count),
        "total_count": total_count,
        "ratio_percent": round(ratio_percent, 1),
        "segments": [
            {"label": "一致", "count": matching_count},
            {"label": "その他", "count": max(0, total_count - matching_count)},
        ],
    }


def calculate_average_duration(videos: List[Dict[str, Any]], filter_query: str, granularity: str) -> Dict[str, Any]:
    active_videos = []

    for video in videos:
        if video.get("deleted"):
            continue
        if video.get("duration_seconds", 0) <= 0:
            continue
        if filter_query.strip() and not matches_query_text(video, filter_query):
            continue
        active_videos.append(video)

    grouped_seconds: Dict[str, int] = defaultdict(int)
    for video in active_videos:
        published_at = parse_datetime(video.get("published_at", "")) or parse_datetime(video.get("created_at", ""))
        if published_at is None:
            continue
        key = published_at.strftime("%Y-%m") if granularity == "month" else published_at.strftime("%Y-%m-%d")
        grouped_seconds[key] += video.get("duration_seconds", 0)

    period_count = len(grouped_seconds)
    average_seconds = int(sum(grouped_seconds.values()) / period_count) if period_count else 0

    return {
        "filter_query": filter_query,
        "average_seconds": average_seconds,
        "average_text": format_seconds(average_seconds),
        "period_count": period_count,
        "video_count": len(active_videos),
        "label": "1か月の平均配信時間" if granularity == "month" else "1日の平均配信時間",
    }


def calculate_statistics(granularity: str, chart_offset: int, ratio_query: str, average_query: str) -> Dict[str, Any]:
    granularity = "month" if granularity == "month" else "day"
    videos = merge_video_data()

    return {
        "granularity": granularity,
        "progress_chart": build_progress_chart(granularity, chart_offset),
        "tag_ratio": calculate_tag_ratio(videos, ratio_query),
        "average_duration": calculate_average_duration(videos, average_query, granularity),
    }


@app.before_request
def prepare_storage() -> None:
    ensure_storage_ready()


@app.route("/")
def index() -> str:
    config = load_config()
    ui_language = resolve_ui_language(config)
    return render_template(
        "index.html",
        icon_url=resolve_ui_icon_url(config),
        ui_language=ui_language,
        ui_locale=UI_LOCALE_MAP.get(ui_language, UI_LOCALE_MAP[DEFAULT_UI_LANGUAGE]),
        text=get_template_text(ui_language),
    )


@app.route("/settings")
def settings_page() -> str:
    config = load_config()
    ui_language = resolve_ui_language(config)
    return render_template(
        "settings.html",
        icon_url=resolve_ui_icon_url(config),
        ui_language=ui_language,
        ui_locale=UI_LOCALE_MAP.get(ui_language, UI_LOCALE_MAP[DEFAULT_UI_LANGUAGE]),
        text=get_template_text(ui_language),
    )


@app.route("/api/settings", methods=["GET"])
def api_get_settings():
    config = load_config()
    videos = merge_video_data()
    return jsonify({
        "ok": True,
        "settings": build_settings_payload(config),
        "tag_entries": tag_entries(videos),
    })


@app.route("/api/settings", methods=["POST"])
def api_save_settings():
    data = request.get_json(silent=True) or {}
    config = load_config()
    previous_sync_excluded_tags = ", ".join(split_tags(str(config.get("sync_excluded_tags", ""))))

    next_api_key = str(data.get("youtube_api_key", "")).strip()
    next_channel_reference = normalize_channel_reference_text(data.get("channel_reference", ""))
    refresh_channel_details = should_refresh_channel_details(config, next_api_key, next_channel_reference)

    config["youtube_api_key"] = next_api_key
    config["channel_reference"] = next_channel_reference
    config["auto_sync_minutes"] = max(1, parse_int(data.get("auto_sync_minutes", 30), 30))
    config["backup_limit"] = max(1, parse_int(data.get("backup_limit", DEFAULT_CONFIG["backup_limit"]), DEFAULT_CONFIG["backup_limit"]))
    config["sync_excluded_tags"] = ", ".join(split_tags(str(data.get("sync_excluded_tags", ""))))
    config["stats_ratio_query"] = str(data.get("stats_ratio_query", "")).strip()
    config["stats_average_query"] = str(data.get("stats_average_query", "")).strip()
    config["ui_language"] = normalize_supported_language(data.get("ui_language", "")) or DEFAULT_UI_LANGUAGE
    config["default_sort"] = normalize_sort(str(data.get("default_sort", DEFAULT_CONFIG["default_sort"])))

    if next_api_key and next_channel_reference:
        if refresh_channel_details:
            try:
                sync_primary_channel_fields(config, resolve_channel_details_list(next_api_key, next_channel_reference))
            except Exception as error:
                return jsonify({"ok": False, "error": str(error)}), 400
        else:
            sync_primary_channel_fields(config, channel_details_from_config(config))
        config["last_sync_status"] = "idle"
        config["last_sync_message"] = "設定を保存しました。"
    else:
        sync_primary_channel_fields(config, [])
        config["last_synced_at"] = ""
        config["last_sync_status"] = "idle"
        config["last_sync_message"] = "未設定"

    saved = save_config(config)
    apply_result = None
    if (
        saved.get("sync_excluded_tags", "") != previous_sync_excluded_tags
        or truthy(data.get("apply_sync_excluded_tags", False))
    ):
        apply_result = apply_sync_tag_exclusions_to_existing(saved.get("sync_excluded_tags", ""))

    return jsonify({
        "ok": True,
        "settings": build_settings_payload(saved),
        "tag_entries": tag_entries(merge_video_data()),
        "apply_result": apply_result,
    })


@app.route("/api/stats-preferences", methods=["POST"])
def api_save_stats_preferences():
    data = request.get_json(silent=True) or {}
    config = load_config()
    config["stats_ratio_query"] = str(data.get("stats_ratio_query", "")).strip()
    config["stats_average_query"] = str(data.get("stats_average_query", "")).strip()
    saved = save_config(config)
    return jsonify({
        "ok": True,
        "settings": build_settings_payload(saved),
    })


@app.route("/api/ui-icon", methods=["POST"])
def api_save_ui_icon():
    icon_file = request.files.get("icon")
    if icon_file is None or not str(getattr(icon_file, "filename", "") or "").strip():
        return jsonify({"ok": False, "error": "画像ファイルを選択してください。"}), 400

    try:
        icon_url = save_uploaded_image(icon_file, "yam_icon", "icon")
        config = load_config()
        config["ui_icon_url"] = icon_url
        saved = save_config(config)
        maybe_auto_backup()
        return jsonify({
            "ok": True,
            "settings": build_settings_payload(saved),
        })
    except Exception as error:
        return jsonify({"ok": False, "error": f"アイコン保存に失敗しました: {error}"}), 500


@app.route("/api/sync", methods=["POST"])
def api_sync():
    sync_info = start_background_sync(mode="manual")
    if not sync_info.get("configured"):
        return jsonify({"ok": False, "error": "YouTube APIキーとチャンネル設定が必要です。", "sync": sync_info}), 400
    return jsonify({"ok": True, "sync": sync_info})


@app.route("/api/sync-tag-exclusions/apply", methods=["POST"])
def api_apply_sync_tag_exclusions():
    data = request.get_json(silent=True) or {}
    sync_excluded_tags = data.get("sync_excluded_tags")

    try:
        result = apply_sync_tag_exclusions_to_existing(sync_excluded_tags)
        return jsonify({
            "ok": True,
            "result": result,
            "settings": result["settings"],
            "tag_entries": result["tag_entries"],
        })
    except Exception as error:
        return jsonify({"ok": False, "error": f"同期除外タグの適用に失敗しました: {error}"}), 500


@app.route("/api/sync-status", methods=["GET"])
def api_sync_status():
    return jsonify({"ok": True, "sync": build_sync_info(load_config())})


@app.route("/api/app-lifecycle", methods=["POST"])
def api_app_lifecycle():
    data = request.get_json(silent=True) or {}
    action = str(data.get("action", "heartbeat")).strip().lower()
    tab_id = str(data.get("tab_id", "")).strip()

    if not tab_id:
        return jsonify({"ok": False, "error": "tab_id が必要です。"}), 400

    if action == "register":
        register_app_client(tab_id)
    elif action == "heartbeat":
        touch_app_client(tab_id)
    elif action == "unregister":
        unregister_app_client(tab_id)
    else:
        return jsonify({"ok": False, "error": "action が不正です。"}), 400

    return jsonify({"ok": True, "active_clients": active_app_client_count()})


@app.route("/api/app-lifecycle/stream", methods=["GET"])
def api_app_lifecycle_stream():
    tab_id = str(request.args.get("tab_id", "")).strip()
    if not tab_id:
        return jsonify({"ok": False, "error": "tab_id が必要です。"}), 400

    register_app_client(tab_id)

    @stream_with_context
    def event_stream():
        try:
            while not SERVER_STATE.get("shutdown_requested"):
                if not touch_app_client(tab_id):
                    break
                yield ": keepalive\n\n"
                time.sleep(APP_CLIENT_STREAM_PING_SECONDS)
        except GeneratorExit:
            pass
        finally:
            unregister_app_client(tab_id)

    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/api/videos", methods=["GET"])
def api_videos():
    keyword = request.args.get("q", "").strip()
    tag_query = request.args.get("tag_q", "").strip()
    status = request.args.get("status", "all").strip()

    sync_info = maybe_auto_sync()
    config = load_config()
    sort_name = normalize_sort(request.args.get("sort", "").strip() or config.get("default_sort", DEFAULT_CONFIG["default_sort"]))

    videos = merge_video_data()
    tag_source_videos = filter_videos_without_tag_query(videos, keyword, status)
    filtered = filter_videos(videos, keyword, tag_query, status)
    sorted_filtered = sort_videos(filtered, sort_name)

    return jsonify({
        "ok": True,
        "summary": get_cached_summary(),
        "count": len(sorted_filtered),
        "videos": sorted_filtered,
        "tag_entries": tag_entries(tag_source_videos),
        "sync": sync_info,
        "sort": sort_name,
    })


@app.route("/api/progress", methods=["POST"])
def api_progress():
    data = request.get_json(silent=True) or {}

    video_id = str(data.get("video_id", "")).strip()
    watched_input = data.get("watched_time_text", data.get("watched_seconds", 0))
    mark_watched = truthy(data.get("mark_watched", False))
    clear_progress = truthy(data.get("clear_progress", False))

    if not video_id:
        return jsonify({"ok": False, "error": "video_id が必要です。"}), 400

    try:
        result = update_progress(video_id, watched_input, mark_watched=mark_watched, clear_progress=clear_progress)
        return jsonify({"ok": True, "result": result})
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 404
    except Exception as error:
        return jsonify({"ok": False, "error": f"保存に失敗しました: {error}"}), 500


@app.route("/api/note", methods=["POST"])
def api_note():
    data = request.get_json(silent=True) or {}
    video_id = str(data.get("video_id", "")).strip()
    note = str(data.get("note", ""))

    if not video_id:
        return jsonify({"ok": False, "error": "video_id が必要です。"}), 400

    try:
        result = update_note(video_id, note)
        return jsonify({"ok": True, "result": result})
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 404
    except Exception as error:
        return jsonify({"ok": False, "error": f"保存に失敗しました: {error}"}), 500


@app.route("/api/video-tags", methods=["POST"])
def api_video_tags():
    data = request.get_json(silent=True) or {}
    video_id = str(data.get("video_id", "")).strip()
    manual_tags_text = str(data.get("manual_tags", ""))

    if not video_id:
        return jsonify({"ok": False, "error": "video_id が必要です。"}), 400

    try:
        result = update_video_tags(video_id, manual_tags_text)
        return jsonify({"ok": True, "result": result})
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 404
    except Exception as error:
        return jsonify({"ok": False, "error": f"タグ保存に失敗しました: {error}"}), 500


@app.route("/api/videos/bulk", methods=["POST"])
def api_videos_bulk():
    data = request.get_json(silent=True) or {}
    video_ids = data.get("video_ids", [])
    add_tags = str(data.get("add_tags", ""))
    remove_tags = str(data.get("remove_tags", ""))
    delete_videos = truthy(data.get("delete_videos", False))
    mark_watched = truthy(data.get("mark_watched", False))
    clear_progress = truthy(data.get("clear_progress", False))

    try:
        result = bulk_update_videos(
            video_ids,
            add_tags_text=add_tags,
            remove_tags_text=remove_tags,
            delete_videos=delete_videos,
            mark_watched=mark_watched,
            clear_progress=clear_progress,
        )
        videos = merge_video_data()
        return jsonify({
            "ok": True,
            "result": result,
            "summary": get_cached_summary(),
            "tag_entries": tag_entries(videos),
        })
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception as error:
        return jsonify({"ok": False, "error": f"一括操作に失敗しました: {error}"}), 500


@app.route("/api/tag-actions", methods=["POST"])
def api_tag_actions():
    data = request.get_json(silent=True) or {}
    action = str(data.get("action", "")).strip()
    target_tag = str(data.get("target_tag", "")).strip()
    new_tag = str(data.get("new_tag", "")).strip()

    try:
        if action == "rename":
            result = rename_manual_tag_across_videos(target_tag, new_tag)
        elif action == "delete":
            result = delete_manual_tag_across_videos(target_tag)
        else:
            return jsonify({"ok": False, "error": "action が不正です。"}), 400

        return jsonify({
            "ok": True,
            "result": result,
            "tag_entries": tag_entries(merge_video_data()),
        })
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception as error:
        return jsonify({"ok": False, "error": f"タグ編集に失敗しました: {error}"}), 500


@app.route("/api/manual-video", methods=["POST"])
def api_manual_video():
    is_form = request.content_type and "multipart/form-data" in request.content_type
    data = request.form if is_form else (request.get_json(silent=True) or {})
    title = str(data.get("title", ""))
    url = str(data.get("url", ""))
    duration_input = data.get("duration_text", data.get("duration_seconds", 0))
    manual_tags = str(data.get("manual_tags", ""))
    note = str(data.get("note", ""))
    watched_input = data.get("watched_time_text", data.get("watched_seconds", 0))
    mark_watched = truthy(data.get("mark_watched", False))
    thumbnail_file = request.files.get("thumbnail") if is_form else None

    try:
        result = add_manual_video(
            title,
            url,
            duration_input,
            manual_tags,
            note=note,
            watched_input=watched_input,
            mark_watched=mark_watched,
            thumbnail_file=thumbnail_file,
        )
        return jsonify({"ok": True, "result": result})
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception as error:
        return jsonify({"ok": False, "error": f"手動追加に失敗しました: {error}"}), 500


@app.route("/api/stats", methods=["GET"])
def api_stats():
    granularity = "month" if request.args.get("granularity", "day").strip() == "month" else "day"
    chart_offset = normalize_chart_offset(request.args.get("offset", 0))
    ratio_query = request.args.get("ratio_q", "").strip()
    average_query = request.args.get("average_q", "").strip()
    videos = merge_video_data()
    return jsonify({
        "ok": True,
        "stats": {
            "granularity": "month" if granularity == "month" else "day",
            "progress_chart": build_progress_chart(granularity, chart_offset),
            "tag_ratio": calculate_tag_ratio(videos, ratio_query),
            "average_duration": calculate_average_duration(videos, average_query, granularity),
        },
        "tag_entries": tag_entries(videos),
    })


@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_thumbnail(filename: str):
    safe_name = os.path.basename(filename)
    if safe_name != filename:
        return jsonify({"ok": False, "error": "ファイルが見つかりません。"}), 404
    path = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.exists(path):
        return jsonify({"ok": False, "error": "ファイルが見つかりません。"}), 404
    return send_file(path)


@app.route("/assets/<path:filename>", methods=["GET"])
def uploaded_asset(filename: str):
    path = resolve_asset_path(filename)
    if not path:
        return jsonify({"ok": False, "error": "ファイルが見つかりません。"}), 404
    return send_file(path)


@app.route("/api/thumbnail/<video_id>/download", methods=["GET"])
def api_thumbnail_download(video_id: str):
    try:
        video = get_video_row(video_id)
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 404

    thumbnail_url = video.get("thumbnail_url", "").strip()
    if not thumbnail_url:
        return jsonify({"ok": False, "error": "サムネイルがありません。"}), 404

    if thumbnail_url.startswith("/uploads/"):
        filename = os.path.basename(thumbnail_url.replace("/uploads/", "", 1))
        path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(path):
            return jsonify({"ok": False, "error": "サムネイルが見つかりません。"}), 404
        download_name = f"{slugify_filename(video.get('title', ''), video_id)}{os.path.splitext(filename)[1] or '.jpg'}"
        return send_file(path, as_attachment=True, download_name=download_name)

    request_obj = Request(thumbnail_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request_obj, timeout=20) as response:
            content = response.read()
            content_type = response.headers.get_content_type() or "image/jpeg"
    except (HTTPError, URLError) as error:
        return jsonify({"ok": False, "error": f"サムネイル取得に失敗しました: {error}"}), 502

    download_name = f"{slugify_filename(video.get('title', ''), video_id)}.jpg"
    return send_file(
        io.BytesIO(content),
        mimetype=content_type,
        as_attachment=True,
        download_name=download_name,
    )


@app.route("/api/backup", methods=["POST"])
def api_backup():
    try:
        backup_name = maybe_auto_backup(force=True) or create_backup()
        return jsonify({"ok": True, "backup_name": backup_name})
    except Exception as error:
        return jsonify({"ok": False, "error": f"バックアップ作成に失敗しました: {error}"}), 500


def run_server(host: Optional[str] = None, port: Optional[int] = None, debug: Optional[bool] = None) -> None:
    ensure_storage_ready()
    server_host = str(host).strip() if host else runtime_host()
    preferred_port = max(1, int(port)) if port is not None else runtime_port()
    server_port = choose_runtime_port(server_host, preferred_port)
    server_debug = runtime_debug() if debug is None else bool(debug)
    if server_debug:
        app.run(
            host=server_host,
            port=server_port,
            debug=True,
            threaded=True,
            use_reloader=True,
        )
        return

    reset_app_lifecycle_state()
    SERVER_STATE["shutdown_requested"] = False
    SERVER_STATE["server"] = make_server(server_host, server_port, app, threaded=True)

    monitor_thread = None
    if runtime_auto_exit():
        monitor_thread = threading.Thread(target=lifecycle_monitor_loop, daemon=True)
        monitor_thread.start()
    SERVER_STATE["monitor_thread"] = monitor_thread

    try:
        SERVER_STATE["server"].serve_forever()
    finally:
        SERVER_STATE["shutdown_requested"] = True
        server = SERVER_STATE.get("server")
        if isinstance(server, BaseWSGIServer):
            server.server_close()
        SERVER_STATE["server"] = None
        SERVER_STATE["monitor_thread"] = None
        reset_app_lifecycle_state()


def main(argv: Optional[List[str]] = None) -> int:
    args = list(argv or sys.argv[1:])
    if args:
        print("使い方: python app.py")
        return 1

    host = runtime_host()
    port = runtime_port()
    debug = runtime_debug()
    browser_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host

    print("ローカルサーバーを起動します。")
    actual_port = choose_runtime_port(host, port)
    print(f"URL: http://{browser_host}:{actual_port}")
    if host in {"0.0.0.0", "::"}:
        print(f"LAN共有: http://PCのIPアドレス:{actual_port}")
    print(f"debug: {'on' if debug else 'off'}")
    run_server(host=host, port=actual_port, debug=debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
