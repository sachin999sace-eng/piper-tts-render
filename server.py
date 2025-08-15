import io
import os
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

PIPER_BIN = "piper"
MODEL = os.environ.get("PIPER_MODEL", "/app/models/model.onnx")
CONFIG = os.environ.get("PIPER_CONFIG", "/app/models/model.onnx.json")

def synth_to_wav(text: str) -> bytes:
    # Piper reads text from stdin and writes WAV to file with -f
    out_path = "/tmp/out.wav"
    # Clean previous output if any
    try:
        os.remove(out_path)
    except FileNotFoundError:
        pass

    proc = subprocess.run(
        [PIPER_BIN, "-m", MODEL, "-c", CONFIG, "-f", out_path],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if proc.returncode != 0 or not os.path.exists(out_path):
        raise RuntimeError(f"Piper failed: {proc.stderr.decode('utf-8', errors='ignore')}")
    with open(out_path, "rb") as f:
        return f.read()

@app.get("/health")
def health():
    ok = os.path.exists(MODEL) and os.path.exists(CONFIG)
    return jsonify({"ok": ok})

@app.get("/tts")
def tts_get():
    text = request.args.get("text", "").strip()
    if not text:
        return jsonify({"error": "missing ?text=..."}), 400
    audio = synth_to_wav(text)
    return send_file(io.BytesIO(audio), mimetype="audio/wav", as_attachment=True, download_name="speech.wav")

@app.post("/tts")
def tts_post():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "missing JSON field: text"}), 400
    audio = synth_to_wav(text)
    return send_file(io.BytesIO(audio), mimetype="audio/wav", as_attachment=True, download_name="speech.wav")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
