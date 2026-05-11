#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3.10 以上が必要です。"
  read -r -p "Enterで閉じる..."
  exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/build_release.py"
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
  echo
  echo "ビルドに失敗しました。"
  read -r -p "Enterで閉じる..."
fi

exit "$STATUS"
