#!/usr/bin/env python3
"""cerebro ui: lanzador GTK4 sin adornos (tipo quick-ask) con respuestas
inline, streaming, voz y guardado de notas/snippets."""
import threading
import time
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gdk, GLib, Gtk

from . import audio, config, llm, notes, retrieve, router, web

BG = "#1e1e2e"
FG = "#cdd6f4"
DIM = "#6c7086"
ACCENT = "#89b4fa"
BORDER = "#313244"
GREEN = "#a6e3a1"
RED = "#f38ba8"
YELLOW = "#f9e2af"

CSS = f"""
window.cerebro {{ background: {BG}; color: {FG}; border: 1px solid {BORDER}; border-radius: 14px; }}
.c-hint {{ color: {DIM}; }}
.c-status {{ color: {DIM}; font-size: 10px; }}
.c-answer {{ color: {FG}; font-family: monospace; }}
.c-src {{ color: {ACCENT}; }}
.c-tooltip {{ color: {YELLOW}; }}
"""


class CerebroWin:
    def __init__(self):
        self.cfg = config.load()
        self.answer = ""           # respuesta completa actual
        self.sources = []          # [{rel, path, score, heading}]
        self.plan = None
        self.no_notes = False
        self.busy = False
        self.cancelled = False
        self.recording = False
        self.voice_busy = False
        self.record_process = None
        self.record_path = None
        self.cloud = False

        self.win = Gtk.Window(title="cerebro")
        self.win.set_default_size(940, 620)
        self.win.set_decorated(False)
        self.win.add_css_class("cerebro")
        self.win.set_name("cerebro")

        self._build()
        self._apply_css()
        self._keys()

        self.win.set_default_size(940, 620)

        self.win.connect("close-request", self._on_close)
        self.set_status("¿Qué necesitas?  Ctrl+I=web  Ctrl+C=copiar  Ctrl+K=snippet  Ctrl+S=nota  Ctrl+L=voz  Ctrl+P=nube")

    def _build(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.set_margin_top(10)
        root.set_margin_bottom(12)
        root.set_margin_start(14)
        root.set_margin_end(14)
        self.win.set_child(root)

        self.hint = Gtk.Label(label="", xalign=0, wrap=True)
        self.hint.add_css_class("c-hint")
        self.hint.set_margin_bottom(4)
        root.append(self.hint)

        sw = Gtk.ScrolledWindow(vexpand=True)
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.outbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        sw.set_child(self.outbox)
        root.append(sw)

        self.answer_lbl = Gtk.Label(label="", xalign=0, wrap=True, selectable=True, vexpand=True)
        self.answer_lbl.add_css_class("c-answer")
        self.sources_lbl = Gtk.Label(label="", xalign=0, wrap=True)
        self.sources_lbl.add_css_class("c-src")
        self.outbox.append(self.answer_lbl)
        self.outbox.append(self.sources_lbl)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.set_margin_top(6)
        self.entry = Gtk.Entry(hexpand=True, placeholder_text="Pregunta o busca en tus notas…")
        self.entry.connect("activate", self.on_enter)
        self.entry.set_size_request(-1, 36)
        row.append(self.entry)

        self.btn_knowledge = Gtk.Button(label="LLM")
        self.btn_knowledge.set_tooltip_text(
            "Responder con conocimiento general del modelo (Ctrl+Enter)"
        )
        self.btn_knowledge.set_sensitive(False)
        self.btn_knowledge.connect("clicked", lambda *_: self.knowledge_flow())
        row.append(self.btn_knowledge)

        self.btn_web = Gtk.Button(label="WEB")
        self.btn_web.set_tooltip_text("Buscar en Internet con fuentes (Ctrl+I)")
        self.btn_web.connect("clicked", lambda *_: self.web_flow())
        row.append(self.btn_web)

        self.btn_mic = Gtk.Button(label="🎙")
        self.btn_mic.set_tooltip_text("Preguntar por voz (Ctrl+L)")
        self.btn_mic.connect("clicked", lambda *_: self.toggle_voice())
        row.append(self.btn_mic)

        self.btn_cloud = Gtk.Button(label="☁", tooltip_text="Alternar modelo en la nube (Ctrl+P)")
        self.btn_cloud.connect("clicked", lambda *_: self.toggle_cloud())
        row.append(self.btn_cloud)
        root.append(row)

        self.status_lbl = Gtk.Label(label="", xalign=0)
        self.status_lbl.add_css_class("c-status")
        self.status_lbl.set_margin_top(3)
        root.append(self.status_lbl)

    def _apply_css(self):
        css = CSS.replace("{ACcentB}", ACCENT)
        p = Gtk.CssProvider()
        p.load_from_string(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), p, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _keys(self):
        ctrl = Gdk.ModifierType.CONTROL_MASK
        key = Gtk.EventControllerKey()
        # El Entry consume algunos Ctrl+<tecla>; capturar en la ventana hace que
        # los atajos del lanzador funcionen aunque el campo tenga el foco.
        key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key.connect("key-pressed", self._on_key)
        self.win.add_controller(key)
        self._keymap = {
            (ctrl, Gdk.KEY_c): self.copy_answer,
            (ctrl, Gdk.KEY_k): self.snippet_flow,
            (ctrl, Gdk.KEY_s): self.note_flow,
            (ctrl, Gdk.KEY_l): self.toggle_voice,
            (ctrl, Gdk.KEY_p): self.toggle_cloud,
            (ctrl, Gdk.KEY_i): self.web_flow,
            (ctrl, Gdk.KEY_Return): self.knowledge_flow,
            (ctrl, Gdk.KEY_KP_Enter): self.knowledge_flow,
        }

    def _on_key(self, _c, keyval, _code, state):
        # Ignorar Caps/Num Lock y conservar solo modificadores relevantes.
        mods = state & (
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.ALT_MASK
            | Gdk.ModifierType.SUPER_MASK
            | Gdk.ModifierType.SHIFT_MASK
        )
        for (m, k), fn in self._keymap.items():
            if (m, k) == (mods, keyval):
                if self.busy and fn not in (self.copy_answer, self.toggle_cloud):
                    return True
                fn()
                return True
        if self.busy:
            if keyval == Gdk.KEY_Escape:
                self.cancelled = True
            return True
        if keyval == Gdk.KEY_Escape:
            self.win.close()
            return True
        return False

    # ---- utilidades ----
    def toast(self, msg, color=YELLOW):
        def _set():
            self.status_lbl.set_text(msg)
            self.status_lbl.remove_css_class("c-status")
            self.status_lbl.add_css_class("c-tooltip")
        def _clear():
            self.status_lbl.set_text("")
            self.status_lbl.add_css_class("c-status")
        GLib.idle_add(_set)
        GLib.timeout_add(4000, _clear)
        return False

    def set_status(self, msg, color=DIM):
        self.status_lbl.set_text(msg)
        self.status_lbl.add_css_class("c-status")

    def _run(self, fn):
        t = threading.Thread(target=fn, daemon=True)
        t.start()

    def _set_entry(self, text):
        self.entry.set_text(text)

    def _idle(self, fn, *args):
        """Ejecuta una actualización GTK desde un hilo de trabajo."""
        GLib.idle_add(fn, *args)

    # ---- nube / voz ----
    @property
    def cloud_url(self):
        return self.cfg.get("cloud", {}).get("base_url") or "http://127.0.0.1:11434/v1"

    def cloud_is_alive(self):
        return llm.health(self.cloud_url, timeout=2)

    def toggle_cloud(self):
        self.cloud = not self.cloud
        self.btn_cloud.set_label("☁✓" if self.cloud else "☁")
        self.toast("Modo nube ON (Big Pickle / Zen)" if self.cloud else "Modo local ON", ACCENT)

    def toggle_voice(self):
        if self.voice_busy and not self.recording:
            self.toast("Transcribiendo…", YELLOW)
            return
        if self.recording:
            self.recording = False
            self.btn_mic.set_label("…")
            self.hint.set_text("Transcribiendo…")
            self._run(self._stop_and_ask)
            return
        out = str(Path(self.cfg["audio"]["cache_dir"]) / f"query-{time.time_ns()}.wav")
        try:
            self.record_process = audio.record_start(out)
        except Exception as e:
            self.toast(f"No pude iniciar el micrófono: {e}", RED)
            return
        self.record_path = out
        self.recording = True
        self.voice_busy = True
        self.btn_mic.set_label("⏹")
        self.hint.set_text("Escuchando… Ctrl+L o botón para terminar.")
        GLib.timeout_add_seconds(45, self._voice_timeout)

    def _voice_timeout(self):
        if self.recording:
            self.toggle_voice()
        return False

    def _stop_and_ask(self):
        try:
            audio.record_stop(self.record_process)
            if not self.record_path or not Path(self.record_path).is_file() or Path(self.record_path).stat().st_size < 1024:
                raise RuntimeError("no se capturó audio")
            text = audio.transcribe(self.record_path)
            if not text:
                raise RuntimeError("no se detectó voz")
        except Exception as e:
            self.toast(f"STT falló: {e}", RED)
        else:
            self._idle(self._goto_query, text)
        finally:
            self.record_process = None
            self.recording = False
            self.voice_busy = False
            self._idle(self._voice_finished)

    def _voice_finished(self):
        self.btn_mic.set_label("🎙")
        if self.hint.get_text() == "Transcribiendo…":
            self.hint.set_text("")

    def _goto_query(self, text):
        self.hint.set_text("")
        self._set_entry(text)
        self.on_enter()

    # ---- flujo principal ----
    def on_enter(self, *_):
        self.query = self.entry.get_text().strip()
        self.answer = ""
        self.sources = []
        self.plan = None
        self.no_notes = False
        self.btn_knowledge.set_sensitive(False)
        self.btn_web.set_sensitive(True)
        self.cancelled = False
        if not self.query:
            return
        # web quick-ask 2.0: prefijo "!" → buscador en Brave
        if self.query.startswith("!"):
            self._web_query()
            return
        self._run(self._ask_flow)

    def _web_query(self):
        q = self.query[1:].strip()
        import urllib.parse
        url = "https://duckduckgo.com/?q=" + urllib.parse.quote(q)
        self._open_url(url)

    def _open_url(self, url):
        def _do():
            try:
                import subprocess
                subprocess.Popen(["xdg-open", url])
            except Exception as e:
                self.toast(f"xdg-open: {e}", RED)
        self._run(_do)
        self._idle(lambda: self._set_entry(""))

    def _ask_flow(self):
        self._idle(self._block_ui)
        try:
            plan = router.parse(self.query, self.cfg)
        except Exception as e:
            self._idle(self._unblock_ui)
            self.toast(f"router: {e}", RED)
            return
        self.plan = plan
        terms = plan.get("terms") or [self.query]
        results = retrieve.search(" ".join(terms), self.cfg)
        if plan.get("area"):
            results = [r for r in results if r["area"] == plan["area"]] or results
        results = results[:5]
        self.sources = results

        if not results:
            self._idle(self._show_answer, None, "No está en mis notas.", [])
            return
        # modo búsqueda (search/explain con pocas fuentes sin responder) → lista
        if plan.get("intent") in ("search",) :
            self._idle(self._show_answer, None, None, results)
            return

        system = (
            "Respondé EXCLUSIVAMENTE con la información del CONTEXTO entregado. "
            "Si la información no está en el contexto, respondé exactamente: "
            "«No está en mis notas.» No completes con conocimiento propio. "
            "Citá al final de cada afirmación el path de la nota (el texto del "
            "encabezado ###) del que salió."
        )
        ctx = self._build_context(results)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"CONTEXTO:\n{ctx}\n\nCONSULTA: {self.query}"},
        ]

        if self.cloud:
            if not self.cloud_is_alive():
                self._idle(self._unblock_ui)
                self.toast("Endpoint de nube caído; reejecutá con ☁ desactivado.", RED)
                return
            base, model = self.cloud_url, self.cfg["chat"]["model"]
        else:
            base, model = self.cfg["chat"]["base_url"], self.cfg["chat"]["model"]
        try:
            chunks = []
            for tok in llm.stream_chat(
                base, model, messages,
                max_tokens=self.cfg["chat"]["max_tokens"],
                temperature=self.cfg["chat"]["temperature"],
            ):
                if self.cancelled:
                    self._idle(self._unblock_ui)
                    return
                chunks.append(tok)
                self._idle(self._stream_render, "".join(chunks))
            answer = "".join(chunks)
        except Exception as e:
            self._idle(self._unblock_ui)
            self.toast(f"LLM: {e}", RED)
            return
        self.answer = answer or ""
        self._idle(self._finish_answer)

    def _build_context(self, results):
        context = []
        for result in results:
            source = f"### {result['rel']}"
            if result["area"] == "web":
                source += f"\nURL: {result['path']}"
            context.append(f"{source}\n{result['excerpt']}")
        return "\n\n".join(context)

    def _block_ui(self):
        self.busy = True
        self.cancelled = False
        self.entry.set_sensitive(False)
        self.btn_knowledge.set_sensitive(False)
        self.btn_web.set_sensitive(False)
        self.set_status(f"Consultando…")

    def _unblock_ui(self):
        self.busy = False
        self.entry.set_sensitive(True)
        self.btn_web.set_sensitive(True)
        if self.answer:
            self.set_status("Enter=abrir nota · Ctrl+C=copiar · Ctrl+K=snippet · Ctrl+S=nota")

    def _stream_render(self, text):
        self.answer_lbl.set_text(text)

    def _show_answer(self, _no, answer, results):
        self.busy = False
        self.entry.set_sensitive(True)
        self.btn_web.set_sensitive(True)
        if answer is not None:
            self.answer = answer or ""
            self.answer_lbl.set_text(self.answer or "")
        self.sources = results
        self.render_sources()
        self.no_notes = answer == "No está en mis notas." and not results
        if self.no_notes:
            self.btn_knowledge.set_sensitive(True)
            self.set_status("No hay fuentes. Ctrl+Enter o LLM=respuesta con conocimiento general.")
        else:
            self.set_status("Enter=abrir nota · Ctrl+C=copiar · Ctrl+K=snippet · Ctrl+S=nota")

    def _finish_answer(self):
        self.busy = False
        self.entry.set_sensitive(True)
        self.btn_web.set_sensitive(True)
        self.render_sources()
        self.set_status("Enter=abrir nota · Ctrl+C=copiar · Ctrl+K=snippet · Ctrl+S=nota")

    def knowledge_flow(self):
        """Consulta deliberadamente sin grounding cuando el vault no tiene respuesta."""
        if self.busy:
            return
        query = self.entry.get_text().strip() or getattr(self, "query", "")
        if not query:
            self.toast("Escribí primero una consulta.", RED)
            return
        self.query = query
        self._run(self._knowledge_flow)

    def _knowledge_flow(self):
        self._idle(self._block_ui)
        self.sources = []
        system = (
            "Respondé en español con conocimiento general. Esta respuesta NO proviene "
            "del vault del usuario: no inventes citas ni digas que fue encontrada en sus notas."
        )
        if self.cloud:
            if not self.cloud_is_alive():
                self._idle(self._unblock_ui)
                self.toast("Endpoint de nube caído; desactivá ☁ para usar el modelo local.", RED)
                return
            base, model = self.cloud_url, self.cfg["chat"]["model"]
        else:
            base, model = self.cfg["chat"]["base_url"], self.cfg["chat"]["model"]
        try:
            chunks = []
            for tok in llm.stream_chat(
                base,
                model,
                [{"role": "system", "content": system}, {"role": "user", "content": self.query}],
                max_tokens=self.cfg["chat"]["max_tokens"],
                temperature=self.cfg["chat"]["temperature"],
            ):
                if self.cancelled:
                    self._idle(self._unblock_ui)
                    return
                chunks.append(tok)
                self._idle(self._stream_render, "".join(chunks))
            self.answer = "".join(chunks)
        except Exception as e:
            self._idle(self._unblock_ui)
            self.toast(f"LLM: {e}", RED)
            return
        self._idle(self._finish_knowledge)

    def _finish_knowledge(self):
        self.busy = False
        self.no_notes = False
        self.entry.set_sensitive(True)
        self.btn_knowledge.set_sensitive(False)
        self.btn_web.set_sensitive(True)
        self.sources_lbl.set_text("\n[Respuesta de conocimiento general del LLM: sin fuentes en tus notas]")
        self.set_status("Ctrl+C=copiar · Ctrl+K=snippet · Ctrl+S=nota")

    def web_flow(self):
        """Busca primero fuentes preferidas y responde solo con su contenido."""
        if self.busy:
            return
        query = self.entry.get_text().strip() or getattr(self, "query", "")
        if not query:
            self.toast("Escribí primero una consulta.", RED)
            return
        self.query = query
        self.answer = ""
        self.sources = []
        self.no_notes = False
        self._run(self._web_flow)

    def _web_flow(self):
        self._idle(self._block_ui)
        self._idle(self.set_status, "Buscando primero en tus fuentes web preferidas…")
        try:
            sources = web.search(self.query, self.cfg)
        except Exception as e:
            self._idle(self._web_error, f"No pude consultar Internet: {e}")
            return
        if not sources:
            self._idle(self._web_error, "No encontré fuentes web relevantes para esa consulta.")
            return

        self.sources = sources
        system = (
            "Respondé EXCLUSIVAMENTE usando el CONTEXTO WEB entregado. "
            "Si las fuentes no contienen la respuesta, decilo claramente. "
            "No uses conocimiento propio ni inventes hechos. Citá la URL exacta "
            "al final de cada afirmación factual."
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"CONTEXTO WEB:\n{self._build_context(sources)}\n\nCONSULTA: {self.query}"},
        ]
        if self.cloud:
            if not self.cloud_is_alive():
                self._idle(self._unblock_ui)
                self.toast("Endpoint de nube caído; desactivá ☁ para usar el modelo local.", RED)
                return
            base, model = self.cloud_url, self.cfg["chat"]["model"]
        else:
            base, model = self.cfg["chat"]["base_url"], self.cfg["chat"]["model"]
        try:
            chunks = []
            for tok in llm.stream_chat(
                base,
                model,
                messages,
                max_tokens=self.cfg["chat"]["max_tokens"],
                temperature=self.cfg["chat"]["temperature"],
            ):
                if self.cancelled:
                    self._idle(self._unblock_ui)
                    return
                chunks.append(tok)
                self._idle(self._stream_render, "".join(chunks))
            self.answer = "".join(chunks)
        except Exception as e:
            self._idle(self._unblock_ui)
            self.toast(f"LLM: {e}", RED)
            return
        self._idle(self._finish_web)

    def _web_error(self, message):
        self.busy = False
        self.entry.set_sensitive(True)
        self.btn_web.set_sensitive(True)
        self.answer = message
        self.answer_lbl.set_text(message)
        self.sources_lbl.set_text("")
        self.set_status("Probá reformular o agregá una fuente preferida en config.toml.")

    def _finish_web(self):
        self.busy = False
        self.entry.set_sensitive(True)
        self.btn_web.set_sensitive(True)
        self.render_sources()
        self.set_status("Respuesta grounded en web · Ctrl+C=copiar · Ctrl+K=snippet · Ctrl+S=nota")

    def render_sources(self):
        if not self.sources:
            self.sources_lbl.set_text("")
            return
        web_sources = all(r["area"] == "web" for r in self.sources)
        lines = ["\n[Fuentes web]" if web_sources else "\n[Fuentes]"]
        for r in self.sources[:3]:
            if r["area"] == "web":
                lines.append(f"  {r['rel']}\n    {r['path']}")
            else:
                lines.append(f"  {r['rel']} ({r['score']})")
        self.sources_lbl.set_text("\n".join(lines))

    # ---- acciones ----
    def open_top_source(self):
        if not self.sources:
            return
        self._open_url(self.sources[0]["path"])

    def copy_answer(self):
        if not self.answer:
            self.toast("No hay respuesta que copiar.", RED)
            return
        content = self.answer
        if self.sources:
            content += "\n\nFuentes:\n" + "\n".join(f"- {r['rel']}" for r in self.sources)
        self.win.get_clipboard().set_text(content)
        self.toast("Copiado ✓", GREEN)

    def snippet_flow(self):
        if not self.answer:
            return
        if self.busy:
            self.toast("Esperá a que termine.", RED)
            return
        # clic directo: genera título y guarda con pegado copiado
        lang = (self.plan or {}).get("lang") or ""
        title = self._auto_title()
        self._save_snippet(title, self.answer, lang, (self.plan or {}).get("terms") or ())

    def note_flow(self):
        if not self.answer:
            return
        if self.busy:
            self.toast("Espera a que termine.", RED)
            return
        area = ((self.plan or {}).get("area") or "Crecimiento_personal").replace(" ", "_")
        self._save_note(self._auto_title(), self.answer, area, (self.plan or {}).get("terms") or ())

    def _auto_title(self):
        words = []
        import re
        for w in re.split(r"\s+", self.query):
            w = re.sub(r"[^0-9A-Za-zÁ-Úá-ú_/-]+", "", w)
            if w:
                words.append(w[:24])
        base = " ".join(words[:4]).title()
        return base or time.strftime("%Y-%m-%d %H:%M")

    def _save_snippet(self, title, body, lang, keywords):
        try:
            dest = notes.snippet(
                title, body, lang, self.cfg, area="Programacion", keywords=keywords, unique=True
            )
        except Exception as e:
            self.toast(f"snippet: {e}", RED)
            return
        clip = self.win.get_clipboard()
        clip.set_text(body)
        self.toast(f"Snippet guardado: {dest}", GREEN)

    def _save_note(self, title, body, area, keywords):
        try:
            dest = notes.note(
                title,
                body,
                self.cfg,
                area=area,
                lang=(self.plan or {}).get("lang") or "",
                keywords=keywords,
                unique=True,
            )
        except Exception as e:
            self.toast(f"nota: {e}", RED)
            return
        self.toast(f"Nota guardada: {dest}", GREEN)

    def _on_close(self, *_):
        self.cancelled = True
        audio.record_cancel(self.record_process)
        return False  # propagar cerrar


def main():
    app = Gtk.Application(application_id="ar.cl.cerebro")

    def on_activate(_app):
        w = CerebroWin()
        w.win.set_application(_app)
        w.win.present()

    app.connect("activate", on_activate)
    app.run(None)


if __name__ == "__main__":
    main()
