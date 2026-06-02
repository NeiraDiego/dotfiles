#!/bin/bash

OLLAMA_HOST="192.168.30.110:11434"
OLLAMA_TIMEOUT=2
ENV_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/quick-ask/env"

OLLAMA_MODEL_MINI="llama3.2:1b"
OLLAMA_MODEL_PRO="qwen2.5:7b"
OPENAI_MODEL_MINI="gpt-4o-mini"
OPENAI_MODEL_PRO="gpt-4o"

MODEL_TYPE="${1:-mini}"
MODE_LABEL=$( [ "$MODEL_TYPE" = "pro" ] && echo "pro" || echo "mini" )

QUESTION=$(wofi --show dmenu -p "Pregunta ($MODE_LABEL)" 2>/dev/null) || exit 0
[ -z "$QUESTION" ] && exit 0

QUESTION_JSON=$(printf '%s' "$QUESTION" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

if curl -s --connect-timeout "$OLLAMA_TIMEOUT" "http://$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
    MODEL=$([ "$MODEL_TYPE" = "pro" ] && echo "$OLLAMA_MODEL_PRO" || echo "$OLLAMA_MODEL_MINI")
    BACKEND="Ollama ($MODEL)"
    RESPONSE=$(curl -s "http://$OLLAMA_HOST/api/generate" \
        -d "{\"model\":\"$MODEL\",\"prompt\":$QUESTION_JSON,\"stream\":false}" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('response',''))")
else
    [ -f "$ENV_FILE" ] && source "$ENV_FILE"
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "Error: Ollama caído y no hay OPENAI_API_KEY en $ENV_FILE" | \
            wofi --show dmenu -p "Error" 2>/dev/null
        exit 1
    fi

    MODEL=$([ "$MODEL_TYPE" = "pro" ] && echo "$OPENAI_MODEL_PRO" || echo "$OPENAI_MODEL_MINI")
    BACKEND="OpenAI ($MODEL)"
    RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":$QUESTION_JSON}]}" | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
try:
    print(data['choices'][0]['message']['content'])
except (KeyError, IndexError):
    print('Error: ' + json.dumps(data))
")
fi

[ -n "$RESPONSE" ] && {
    printf '%s\n' " [$BACKEND]" "" "$RESPONSE" | \
        wofi --show dmenu -p "Respuesta:" -W 800 -H 400 2>/dev/null
}
