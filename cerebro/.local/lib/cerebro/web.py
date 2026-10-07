"""Retrieval web sin dependencias: fuentes preferidas primero, luego web general."""
import html
import ipaddress
import json
import re
import socket
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class WebError(RuntimeError):
    pass


_SPHINX_BASES = {
    "docs.python.org": "https://docs.python.org/3/",
    "pandas.pydata.org": "https://pandas.pydata.org/pandas-docs/stable/",
}
_SPHINX_CACHE = {}


class _PageText(HTMLParser):
    _SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header"}

    def __init__(self):
        super().__init__()
        self.title = ""
        self.parts = []
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, _attrs):
        if tag in self._SKIP:
            self._skip += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            self.parts.append(data)


def _request(url, timeout):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "cerebro/1.0 (+local knowledge assistant)"},
    )
    return urllib.request.urlopen(req, timeout=timeout)


def _public_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".local"):
        return False
    try:
        return not ipaddress.ip_address(host).is_private
    except ValueError:
        return True


def _discover(query, timeout):
    url = "https://www.bing.com/search?" + urllib.parse.urlencode(
        {"q": query, "format": "rss", "setlang": "en-US"}
    )
    try:
        with _request(url, timeout) as response:
            page = response.read(1_000_000)
    except (OSError, urllib.error.URLError) as e:
        raise WebError(f"buscador web no disponible: {e}") from e
    try:
        root = ET.fromstring(page)
    except ET.ParseError as e:
        raise WebError("el buscador devolvió una respuesta inválida") from e
    out = []
    for item in root.findall("./channel/item"):
        result = {
            "url": item.findtext("link", ""),
            "title": html.unescape(" ".join(item.findtext("title", "").split())),
            "snippet": html.unescape(" ".join(item.findtext("description", "").split())),
        }
        if _public_url(result["url"]):
            out.append(result)
    return out


def _relevant(result, query):
    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_]{3,}", query)]
    terms = [t for t in terms if t not in {"site", "the", "and", "para", "como", "que"}]
    if not terms:
        return True
    haystack = f"{result['title']} {result['snippet']}".lower()
    needed = 1 if len(terms) == 1 else 2
    return sum(t in haystack for t in set(terms)) >= needed


def _sphinx_sources(domain, query, timeout):
    """Busca en índices Sphinx oficiales (Python/pandas) sin buscador externo."""
    base = _SPHINX_BASES.get(domain)
    if not base:
        return []
    try:
        index = _SPHINX_CACHE.get(base)
        if index is None:
            with _request(urllib.parse.urljoin(base, "searchindex.js"), timeout) as response:
                raw = response.read(6_000_000).decode("utf-8", errors="ignore")
            prefix = "Search.setIndex("
            if not raw.startswith(prefix) or not raw.endswith(")"):
                return []
            index = json.loads(raw[len(prefix):-1])
            _SPHINX_CACHE[base] = index
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return []

    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_]{3,}", query)]
    terms = [t for t in terms if t not in {"python", "pandas", "para", "como", "que"}]
    scored = []
    for docname, title in zip(index.get("docnames", []), index.get("titles", [])):
        plain_title = re.sub(r"<[^>]+>", "", title).lower()
        haystack = f"{docname} {plain_title}".lower()
        score = sum(t in haystack for t in set(terms))
        if score:
            scored.append((score, docname, re.sub(r"<[^>]+>", "", title)))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [
        {
            "url": urllib.parse.urljoin(base, docname + ".html"),
            "title": html.unescape(" ".join(title.split())),
            "snippet": "",
        }
        for _score, docname, title in scored[:2]
    ]


def _relevant_excerpt(text, query, max_chars):
    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_]{3,}", query)]
    terms = [t for t in terms if t not in {"python", "pandas", "javascript", "java", "rust", "para", "como", "que"}]
    positions = [text.lower().find(term) for term in terms]
    positions = [pos for pos in positions if pos >= 0]
    if not positions:
        return text[:max_chars]
    start = max(0, max(positions) - 900)
    return text[start:start + max_chars]


def _fetch(result, timeout, max_chars, query):
    try:
        with _request(result["url"], timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml"}:
                return None
            body = response.read(1_500_000)
            charset = response.headers.get_content_charset() or "utf-8"
    except (OSError, urllib.error.URLError, socket.timeout):
        return None
    parser = _PageText()
    parser.feed(body.decode(charset, errors="ignore"))
    text = " ".join(" ".join(parser.parts).split())
    if len(text) < 120:
        return None
    title = " ".join((parser.title or result["title"]).split())
    return {"url": result["url"], "title": title, "text": _relevant_excerpt(text, query, max_chars)}


def search(query, cfg):
    """Devuelve fuentes legibles, priorizando los dominios elegidos por el usuario."""
    web_cfg = cfg.get("web", {})
    domains = web_cfg.get("preferred_domains", [])
    max_sources = int(web_cfg.get("max_sources", 4))
    timeout = int(web_cfg.get("timeout_seconds", 12))
    max_chars = int(web_cfg.get("chars_per_source", 6_000))
    found = []
    seen = set()

    def collect(results, domain=None, trusted=False):
        for result in results:
            url = result["url"].rstrip("/")
            if url in seen:
                continue
            host = urllib.parse.urlsplit(url).hostname or ""
            if domain and host != domain and not host.endswith("." + domain):
                continue
            if not trusted and not _relevant(result, query):
                continue
            seen.add(url)
            page = _fetch(result, timeout, max_chars, query)
            if page:
                found.append(page)
            if len(found) >= max_sources:
                return True
        return False

    for domain in domains:
        try:
            if collect(_sphinx_sources(domain, query, timeout), domain, trusted=True):
                break
            if collect(_discover(f"site:{domain} {query}", timeout), domain):
                break
        except WebError:
            continue
    if len(found) < max_sources:
        try:
            collect(_discover(query, timeout))
        except WebError:
            pass

    return [
        {
            "path": page["url"],
            "rel": page["title"] or urllib.parse.urlsplit(page["url"]).netloc,
            "area": "web",
            "score": float(max_sources - i),
            "heading": page["title"],
            "excerpt": page["text"],
        }
        for i, page in enumerate(found)
    ]
