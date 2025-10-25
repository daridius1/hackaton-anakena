# Generador de guiones infantiles (Deepseek) — Scaffold

Este pequeño proyecto prepara un cliente y un CLI para enviar una "moraleja" a la API de Deepseek y recibir un guion en JSON con el formato estricto que requiere el pipeline de vídeo.

IMPORTANTE: Nunca pongas tu API key directamente en el repositorio. Usa variables de entorno o un gestor de secretos.

Archivos creados:

- `deepseek_client.py` — cliente mínimo que lee `DEEPSEEK_API_KEY` y `DEEPSEEK_API_URL` desde el entorno y hace la llamada.
- `generate_guion.py` — CLI para generar el guion a partir de la moraleja.
- `.env.example` — ejemplo de variables de entorno.
- `requirements.txt` — dependencias.

Rápido inicio (Linux / bash):

1. Copia `.env.example` a `.env` y edítalo (NO subir `.env` a git):

```bash
cp .env.example .env
# Edita .env y pega tu API key en DEEPSEEK_API_KEY
export DEEPSEEK_API_KEY="sk-..."
export DEEPSEEK_API_URL="https://api.deepseek.example/v1/generate"
```

2. Instala dependencias (recomendado en virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Ejecuta el generador:

```bash
python generate_guion.py "no hablar con extraños"
```

Salida: el CLI imprimirá el JSON estricto que tu pipeline de vídeo espera.

Notas y adaptación:

- El cliente asume que la API de Deepseek acepta POST JSON con un campo `input` y autentica con `Authorization: Bearer <key>`.
  Si tu API utiliza otra forma (por ejemplo `prompt` o un endpoint con otra ruta), ajusta `deepseek_client.py`.
- Si quieres probar sin llamar a la API real, modifica `deepseek_client.py` para devolver un mock JSON siguiendo el esquema.

Seguridad:

- No compartas ni publiques tu API key. Si la pegaste por error en algún commit, respínnea y revoca la clave lo antes posible.
