"""STT/TTS on-demand: invoca el worker del venv 3.12 como subproceso y
mata después de inactividad para devolver la RAM a cero."""
import signal
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


def record_start(out):
    """Inicia pw-record y devuelve un proceso que puede detenerse con record_stop."""
    cfg = cfgmod.load()
    out = str(out)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    # El driver ACP del Framework distorsiona la fuente interna al forzar 16 kHz.
    # faster-whisper remuestrea el WAV nativo (48 kHz) sin problema.
    command = ["pw-record", out]
    return subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def record_stop(process, timeout=5):
    """Pide a pw-record cerrar el WAV correctamente y espera a que termine."""
    if process and process.poll() is None:
        try:
            process.send_signal(signal.SIGINT)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=timeout)


def record_cancel(process):
    """Detiene una grabación sin bloquear el cierre de la UI."""
    if process and process.poll() is None:
        try:
            process.send_signal(signal.SIGINT)
        except ProcessLookupError:
            pass


def record(seconds, out):
    """Compatibilidad para llamadas no interactivas con duración fija."""
    process = record_start(out)
    try:
        process.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        record_stop(process)
    return out
