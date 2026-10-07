#!/usr/bin/env python3
"""cerebro: asistente over tus notas de Obsidian. CLI + lanzador GUI."""
import argparse
import json
import sys
from pathlib import Path

from . import config, retrieve, router, notes, llm, audio, web


def _cfg():
    return config.load()


def _areas_cli(cfg):
    areas, known = retrieve.list_areas(cfg["brain"]["vault"], cfg)
    new = [a for a in areas if a not in known]
    print("Areas indexadas:")
    for a in areas:
        flag = "" if a in known else "  [NUEVA: pedir incluirla]"
        print(f"  - {a}{flag}")
    if new:
        print("-> Agrega las nuevas en [areas] del config.toml para indexarlas.")


def _build_context(results):
    ctx = []
    for r in results:
        ctx.append(f"### {r['rel']}\n{r['excerpt']}")
    return "\n\n".join(ctx)


def ask_cmd(args, cfg):
    plan = router.parse(args.query, cfg)
    if args.debug:
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr)

    terms = plan.get("terms") or [args.query]

    results = retrieve.search(" ".join(terms), cfg)
    if plan.get("area"):
        results = [r for r in results if r["area"] == plan["area"]] or results
    results = results[:5]

    if not results:
        answer = "No está en mis notas."
        print(answer)
        if getattr(args, "voice", False):
            audio.speak(answer, out=str(Path(cfg["audio"]["cache_dir"]) / "ans.wav"))
        return

    if args.no_llm:
        for r in results:
            print(f"[{r['score']}] {r['rel']}\n    {r['heading']}")
        return

    system = (
        "Respondé EXCLUSIVAMENTE con la información del CONTEXTO entregado. "
        "Si la información no está en el contexto, respondé exactamente: "
        "«No está en mis notas.» No completes con conocimiento propio. "
        "Citá al final de cada afirmación el path de la nota (el texto del "
        "encabezado ###) del que salió."
    )
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": f"CONTEXTO:\n{_build_context(results)}\n\n"
            f"CONSULTA: {args.query}",
        },
    ]
    data = llm.chat(
        cfg["chat"]["base_url"],
        args.model or cfg["chat"]["model"],
        messages,
        max_tokens=cfg["chat"]["max_tokens"],
        temperature=cfg["chat"]["temperature"],
    )
    answer = llm.extract_text(data)
    print(answer)
    print("\n[Fuentes]", file=sys.stderr)
    for r in results[:3]:
        print(f"  {r['rel']} ({r['score']})", file=sys.stderr)

    if getattr(args, "voice", False):
        audio.speak(answer, out=str(Path(cfg["audio"]["cache_dir"]) / "ans.wav"))


def search_cmd(args, cfg):
    for r in retrieve.search(args.query, cfg):
        print(f"[{r['score']}] {r['rel']}\n    {r['heading']}")


def web_cmd(args, cfg):
    results = web.search(args.query, cfg)
    if not results:
        print("No encontré fuentes web relevantes.")
        return 1
    for r in results:
        print(f"[{r['score']}] {r['rel']}\n    {r['path']}")


def note_cmd(args, cfg):
    if not args.body and sys.stdin.isatty():
        print("Body via stdin (Ctrl-D para terminar):", file=sys.stderr)
        args.body = sys.stdin.read().strip()
    dest = notes.note(args.title, args.body or "", cfg, args.area, args.lang, args.tags)
    print(f"Nota guardada: {dest}")


def snippet_cmd(args, cfg):
    if not args.code and sys.stdin.isatty():
        print("Código via stdin (Ctrl-D para terminar):", file=sys.stderr)
        args.code = sys.stdin.read().strip()
    dest = notes.snippet(args.title, args.code or "", args.lang, cfg, args.area, args.tags)
    print(f"Snippet guardado: {dest}")


def health_cmd(args, cfg):
    ok = True
    for name, url in (("router", cfg["router"]["base_url"]), ("chat", cfg["chat"]["base_url"])):
        status = "OK" if llm.health(url) else "DOWN"
        if status == "DOWN":
            ok = False
        print(f"  {name:8s} {url:35s} {status}")
    tid = Path(cfg["audio"]["venv_python"]).name
    print(f"  audio    {cfg['audio']['venv_python']}  {'OK' if Path(cfg['audio']['venv_python']).exists() else 'FALTA'}")
    vault_ok = Path(cfg["brain"]["vault"]).is_dir()
    print(f"  vault    {cfg['brain']['vault']}  {'OK' if vault_ok else 'FALTA'}")
    return 0 if ok else 1


def tier_cmd(args, cfg):
    import subprocess

    has_cuda = False
    try:
        r = subprocess.run(["nvidia-smi"], capture_output=True, timeout=5)
        has_cuda = r.returncode == 0
    except FileNotFoundError:
        pass
    cur = args.model or cfg["chat"]["model"]
    print(f"eGPU (CUDA) presente: {has_cuda}")
    print(f"modelo actual de chat: {cur}")


def selftest_cmd(args, cfg):
    failures = []

    def check(name, fn):
        try:
            fn()
            print(f"  [OK] {name}")
        except Exception as e:
            failures.append(name)
            print(f"  [FAIL] {name}: {e}")

    def test_search():
        r = retrieve.search("reduce python", cfg)
        assert any("reduce" in x["rel"].lower() for x in r), f"no encontró reduce: {r[:2]}"

    def test_router_json():
        plan = router.parse("¿qué hace reduce en python?", cfg)
        assert plan["intent"], plan
        assert isinstance(plan["terms"], list), plan

    def test_negative():
        r = retrieve.search("zzzzquimera_jamas_existe", cfg)
        assert not r, f"debería ser vacío: {r[:1]}"

    def test_ask_grounded():
        import io
        import contextlib
        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            ask_cmd(argparse.Namespace(query="¿qué hace reduce en python?", no_llm=False,
                                        voice=False, debug=False, model=None), cfg)
            out = sys.stdout.getvalue()
            assert "No está en mis notas." not in out, out
        finally:
            sys.stdout = old

    check("search literal (reduce python)", test_search)
    check("router produce JSON válido", test_router_json)
    check("test negativo (consulta inexistente)", test_negative)
    check("ask con cita real (usa chat 8080)", test_ask_grounded)

    print(f"\n{len(failures)} fallos" if failures else "\nTodo OK")
    return 1 if failures else 0


def _ui_cmd(cfg):
    from . import ui

    ui.main()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cerebro", description="Asistente sobre tus notas Obsidian")
    ap.add_argument("--debug", action="store_true", help="imprime el plan del router")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ask", help="pregunta con grounding en tus notas")
    p.add_argument("query")
    p.add_argument("--model", default=None, choices=["qwen3-14b", "qwen3-14b-cpu"])
    p.add_argument("--no-llm", action="store_true", help="solo devuelve las fuentes")
    p.add_argument("--voice", action="store_true", help="leer la respuesta en voz alta")
    p.set_defaults(fn=ask_cmd)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.set_defaults(fn=search_cmd)

    p = sub.add_parser("web", help="busca fuentes web (preferidas primero)")
    p.add_argument("query")
    p.set_defaults(fn=web_cmd)

    p = sub.add_parser("note", help="nota rápida -> -Borradores/")
    p.add_argument("title")
    p.add_argument("--body", default="")
    p.add_argument("--area", default=None)
    p.add_argument("--lang", default="")
    p.add_argument("--tags", default="", help="comma-separated")
    p.set_defaults(fn=note_cmd)

    p = sub.add_parser("snippet", help="guarda snippet -> Programacion/<lang>/")
    p.add_argument("title")
    p.add_argument("--code", default="")
    p.add_argument("--lang", required=True)
    p.add_argument("--area", default="Programacion")
    p.add_argument("--tags", default="")
    p.set_defaults(fn=snippet_cmd)

    p = sub.add_parser("areas")
    p.set_defaults(fn=lambda a, c: _areas_cli(c))

    p = sub.add_parser("health")
    p.set_defaults(fn=health_cmd)

    p = sub.add_parser("tier")
    p.add_argument("--model", default=None, choices=["qwen3-14b", "qwen3-14b-cpu"])
    p.set_defaults(fn=tier_cmd)

    p = sub.add_parser("selftest")
    p.set_defaults(fn=selftest_cmd)

    p = sub.add_parser("ui", help="lanzador GTK4 (quick-ask 2.0)")
    p.set_defaults(fn=lambda a, c: _ui_cmd(c))

    args = ap.parse_args(argv)
    cfg = _cfg()
    return args.fn(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
