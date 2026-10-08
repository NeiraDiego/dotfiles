"""Escritura segura de notas y snippets con frontmatter YAML para Obsidian.
Nunca hace git commit/push: el vault está bajo obsidian-git."""
import re
import datetime
import unicodedata
from pathlib import Path

from . import config as cfgmod


_STOPWORDS = {
    "a", "al", "como", "con", "cual", "de", "del", "el", "en", "es",
    "esta", "este", "explica", "hacer", "hace", "la", "las", "los", "mi",
    "para", "por", "que", "se", "sobre", "un", "una", "y",
}


def _part(value):
    """Normaliza un componente del nombre de archivo a ASCII con guiones bajos."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = value.lower().replace("c++", "cpp").replace("c#", "csharp")
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def _filename(title, lang="", keywords=()):
    """`python_reduce_lista.md`: lenguaje y hasta tres keywords significativas."""
    language = _part(lang)
    raw = list(keywords) + [title]
    words = []
    for value in raw:
        for word in _part(str(value)).split("_"):
            if not word or word in _STOPWORDS or word == language or word in words:
                continue
            words.append(word)
            if len(words) == 3:
                break
        if len(words) == 3:
            break
    parts = ([language] if language else []) + words
    return "_".join(parts) or "nota"


def _quick_filename(title):
    """Nombre literal de una nota rápida: el título con espacios como `_`."""
    safe = re.sub(r"[\\/:\x00]", "", title.strip())
    return re.sub(r"\s+", "_", safe).strip("._") or "nota"


def _fm(title, area, lang, tags, kind, source="cerebro"):
    today = datetime.date.today().isoformat()
    tags_txt = ", ".join(f'"{t.strip().lstrip("#")}"' for t in tags if t.strip())
    fm = ["---", f'title: "{title}"', f"area: {area}", f"lang: {lang.strip().lower() or ''}", f"kind: {kind}", f"created: {today}", f"source: {source}"]
    if tags_txt:
        fm.append(f"tags: [{tags_txt}]")
    fm.append("---")
    return "\n".join(fm) + "\n"


def _vault(cfg):
    return Path(cfg["brain"]["vault"])


def note(title, body, cfg=None, area=None, lang="", tags=(), keywords=(), unique=False):
    """Nota rápida → -Borradores/<slug>.md con frontmatter."""
    cfg = cfg or cfgmod.load()
    root = _vault(cfg)
    dest = _destination(root / cfg["notas"]["inbox"], _filename(title, lang, keywords), unique)
    text = _fm(title, area or cfg["notas"]["inbox"], lang, tags, "note") + "\n" + body.strip() + "\n"
    if dest.exists() and not unique:
        raise FileExistsError(f"{dest} ya existe")
    _write(dest, text)
    return dest


def quick_note(markdown, cfg=None):
    """Guarda Markdown sin frontmatter; la primera línea `# Título` nombra el archivo."""
    cfg = cfg or cfgmod.load()
    lines = markdown.splitlines()
    if not lines or not re.match(r"^#\s+\S", lines[0]):
        raise ValueError("la primera línea debe ser un título Markdown: # Título")
    title = lines[0][1:].strip()
    dest = _destination(_vault(cfg) / cfg["notas"]["inbox"], _quick_filename(title), True)
    _write(dest, markdown.rstrip() + "\n")
    return dest


def snippet(title, code, lang, cfg=None, area="Programacion", tags=(), keywords=(), unique=False):
    """Snippet → Programacion/<Lang>/<slug>.md con bloque de código."""
    cfg = cfg or cfgmod.load()
    root = _vault(cfg)
    lang_dir = lang.strip().lower() or "Other"
    dest = _destination(root / area / lang_dir, _filename(title, lang, keywords), unique)
    text = _fm(title, area, lang, tags, "snippet") + "\n```" + lang + "\n" + code.strip() + "\n```\n"
    if dest.exists() and not unique:
        raise FileExistsError(f"{dest} ya existe")
    _write(dest, text)
    return dest


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _destination(directory, filename, unique):
    path = directory / f"{filename}.md"
    if not unique or not path.exists():
        return path
    n = 2
    while True:
        candidate = directory / f"{filename}_{n}.md"
        if not candidate.exists():
            return candidate
        n += 1
