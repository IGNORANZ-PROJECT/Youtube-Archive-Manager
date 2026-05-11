#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

for APP_BIN in \
  "$SCRIPT_DIR/dist/YAM/YAM" \
  "$SCRIPT_DIR/release/YAM/YAM" \
  "$SCRIPT_DIR/YAM"; do
  if [ -x "$APP_BIN" ]; then
    "$APP_BIN"
    exit $?
  fi
done

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3.10 以上が必要です。"
  read -r -p "Enterで閉じる..."
  exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/launch_yam.py"
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
  echo
  echo "起動に失敗しました。"
  read -r -p "Enterで閉じる..."
fi

exit "$STATUS"
