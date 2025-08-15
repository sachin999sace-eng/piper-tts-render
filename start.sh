#!/usr/bin/env bash
set -e

# These two must point to your chosen Piper voice files
# Example: en_US voice model (.onnx) + its config (.json)
# You will set them in Render's Environment tab.
MODEL_URL="${PIPER_MODEL_URL:-}"
CONFIG_URL="${PIPER_CONFIG_URL:-}"

mkdir -p /app/models

# Download voice model/config only if missing
if [ ! -f "$PIPER_MODEL" ]; then
  if [ -z "$MODEL_URL" ]; then
    echo "ERROR: PIPER_MODEL_URL not set. Please add it in Render → Environment."
    exit 1
  fi
  echo "Downloading model from $MODEL_URL ..."
  curl -L "$MODEL_URL" -o "$PIPER_MODEL"
fi

if [ ! -f "$PIPER_CONFIG" ]; then
  if [ -z "$CONFIG_URL" ]; then
    echo "ERROR: PIPER_CONFIG_URL not set. Please add it in Render → Environment."
    exit 1
  fi
  echo "Downloading config from $CONFIG_URL ..."
  curl -L "$CONFIG_URL" -o "$PIPER_CONFIG"
fi

echo "Starting Piper TTS API on port ${PORT:-5000} ..."
exec waitress-serve --host 0.0.0.0 --port "${PORT:-5000}" server:app
