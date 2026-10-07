"""Retrieval sin índice: el vault son ~215 notas / 0.3 MB, se lee en <20 ms.
ranking = título(×3) + encabezado(×2) + cuerpo(×1); path→excerpt con heading."""
import bisect
import re
from pathlib import Path

from . import config as cfgmod


def _excludes(cfg):
    ex = set(cfg.get("brain", {}).get("excludes", []))
    return ex


def walk_files(vault, cfg):
    root = Path(vault)
    ex = _excludes(cfg)
    out = []
    for p in root.rglob("*.md"):
        parts = p.relative_to(root).parts
        if any(s in parts for s in ex):
            continue
        if p.is_relative_to(root / ".git") or p.is_relative_to(root / ".obsidian"):
            continue
        out.append(p)
    return out


def list_areas(vault, cfg):
    root = Path(vault)
    known = set(cfg.get("areas", {}).get("known", []))
    ex = _excludes(cfg)
    areas = []
    for p in sorted(root.iterdir()):
        if not p.is_dir() or p.name in ex:
            continue
        areas.append(p.name)
    return areas, known


def _score(rel_lower, text_lower, terms):
    score = 0.0
    for t in terms:
        if not t:
            continue
        c_path = rel_lower.count(t)
        c_head = sum(
            1 for ln in text_lower.splitlines() if ln.startswith("#") and t in ln
        )
        c_body = text_lower.count(t)
        score += c_path * 3.0 + c_head * 2.0 + min(c_body, 50)
    return score


def _excerpt(text, terms, radius=4):
    lines = text.splitlines()
    first = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if any(t in low for t in terms if t):
            first = i
            break
    if first is None:
        return ""
    start = max(0, first - radius)
    end = min(len(lines), first + radius + 1)
    return "\n".join(lines[start:end])


def _heading_ctx(text, hit_line):
    for ln in reversed(text.splitlines()[: hit_line + 1]):
        if ln.startswith("#"):
            return ln
    return ""


def search(query, cfg=None):
    cfg = cfg or cfgmod.load()
    vault = cfg["brain"]["vault"]
    root = Path(vault)
    terms = [t.strip().lower() for t in re.split(r"\s+", query) if t.strip()]
    if not terms:
        return []

    results = []
    for p in walk_files(vault, cfg):
        rel = str(p.relative_to(root)).lower()
        text = p.read_text(errors="ignore")
        s = _score(rel, text.lower(), terms)
        if s > 0:
            results.append((s, p, rel, text))

    results.sort(key=lambda r: (-r[0], r[1]))

    out = []
    for s, p, rel, text in results[:20]:
        lines = text.splitlines()
        hit = next((i for i, ln in enumerate(lines) if any(t in ln.lower() for t in terms)), 0)
        heading = _heading_ctx(text, hit)
        out.append(
            {
                "path": str(p),
                "rel": rel,
                "area": rel.split("/")[0],
                "score": round(s, 1),
                "heading": heading,
                "excerpt": _excerpt(text, terms),
            }
        )
    return out