"""STT/TTS on-demand: invoca el worker del venv 3.12 como subproceso y
mata después de inactividad para devolver la RAM a cero."""
import shlex
import subprocess
import time
from pathlib import Path

from . import config as cfgmod

_last = [0.0]


def _run(args, timeout=300):
    cfg = cfgmod.load()
    py = cfg["audio"]["venv_python"]
    worker = Path(__file__).parent / "audio_worker.py"
    t0 = time.time()
    r = subprocess.run(
        [py, str(worker), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    _last[0] = time.time()
    if r.returncode != 0:
        raise RuntimeError(f"audio_worker: {r.stderr.strip()[:400]}")
    return r.stdout.strip(), time.time() - t0


def transcribe(wav):
    return _run(["transcribe", wav])[0]


def speak(text, out=None, voice=None):
    cfg = cfgmod.load()
    out = out or str(Path(cfg["audio"]["cache_dir"]) / "tts.wav")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    voice = voice or cfg["audio"].get("tts_voice", "ef_dora")
    return _run(["speak", text, "--voice", voice, "--out", out])[0]


def play(path):
    subprocess.run(["pw-play", path], check=False)


def record(seconds, out):
    out = str(out)
    r = subprocess.run(
        ["pw-record", "--rate", "16000", out],
        timeout=seconds + 5,
        capture_output=True,
        text=True,
    )
    return out