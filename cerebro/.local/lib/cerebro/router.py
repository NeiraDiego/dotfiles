"""Router: Qwen3-1.7B parsea la consulta a JSON estricto via json_schema."""
import json

from . import llm, config

SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["ask", "search", "save_note", "save_snippet", "explain"]},
        "mode": {"type": "string", "enum": ["literal", "auto"]},
        "terms": {"type": "array", "items": {"type": "string", "maxLength": 40}},
        "area": {"type": ["string", "null"], "maxLength": 40},
        "lang": {"type": ["string", "null"], "maxLength": 40},
    },
    "required": ["intent", "mode", "terms", "area", "lang"],
    "additionalProperties": False,
}


def parse(raw_query, cfg=None):
    cfg = cfg or config.load()
    areas = cfg.get("areas", {}).get("known", [])
    areas_txt = ", ".join(areas)
    system = (
        "Eres el router de un asistente que busca en un vault de notas de "
        "Obsidian. Analiza la consulta del usuario y responde SOLO JSON.\n"
        "intent: una de ask (pregunta informativa), search (buscar nota), "
        "explain (explicar concepto), save_note (guardar nota rapida), "
        "save_snippet (guardar snippet de codigo).\n"
        "mode: literal si la consulta nombra una funcion, lenguaje o concepto "
        "exacto; auto si es vaga o conceptual.\n"
        "terms: 2-5 palabras clave en minuscula; incluye sinonimos en ingles "
        "si la nota puede estar en ingles (ej. reduce -> [reduce, functools, "
        "fold, acumular]).\n"
        f"area: una de estas carpetas: {areas_txt} o null.\n"
        "lang: lenguaje de programacion (python, bash, css, git...) o null.\n"
        "Usa area/lang solo si estas razonablemente seguro; si no, null."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": raw_query},
    ]
    last = None
    for tokens in (cfg["router"]["max_tokens"], 512):
        data = llm.chat(
            cfg["router"]["base_url"],
            "router",
            messages,
            max_tokens=tokens,
            temperature=0.0,
            chat_template_kwargs={"enable_thinking": False},
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "query_plan", "schema": SCHEMA, "strict": True},
            },
        )
        try:
            return json.loads(llm.extract_text(data))
        except (json.JSONDecodeError, KeyError) as e:
            last = e
    raise RuntimeError(f"router falló en producir JSON válido: {last}")