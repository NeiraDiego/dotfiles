"""Worker de audio para cerebro. Corre DENTRO del venv 3.12 (kokoro exige <3.13).

Uso:
  audio_worker.py transcribe <ruta.wav>
  audio_worker.py speak <texto> --voice ef_dora --out /ruta/out.wav
"""
import argparse
import sys
import time


def transcribe(wav):
    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(wav, language="es", vad_filter=True)
    return " ".join(s.text.strip() for s in segments).strip()


def speak(text, voice, out):
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    kp = KPipeline(lang_code="e")
    chunks = []
    for _g, _ph, audio in kp(text, voice=voice, speed=1.0):
        chunks.append(audio)
    if not chunks:
        raise RuntimeError("kokoro no generó audio")
    audio = np.concatenate(chunks)
    sf.write(out, audio, 24000)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="op", required=True)

    p_t = sub.add_parser("transcribe")
    p_t.add_argument("wav")

    p_s = sub.add_parser("speak")
    p_s.add_argument("text")
    p_s.add_argument("--voice", default="ef_dora")
    p_s.add_argument("--out", required=True)

    args = ap.parse_args()

    t0 = time.time()
    if args.op == "transcribe":
        print(transcribe(args.wav), flush=True)
    else:
        speak(args.text, args.voice, args.out)
        print(args.out, flush=True)
    sys.stderr.write(f"[audio_worker] {args.op} {time.time()-t0:.2f}s\n")


if __name__ == "__main__":
    main()