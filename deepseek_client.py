"""
Minimal Deepseek API client wrapper.

Behavior / contract (small):
- Inputs: a short `moraleja` string (user-provided).
- Output: JSON returned by the remote Deepseek API (as Python dict).
- Error modes: raises RuntimeError on HTTP errors or missing config.

This module reads `DEEPSEEK_API_KEY` and `DEEPSEEK_API_URL` from the environment.
Do NOT hardcode your API key in source. Use environment variables or a secrets manager.
"""
import os
import json
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


class DeepseekClient:
    def __init__(self, api_key: str | None = None, api_url: str | None = None, timeout: int | None = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.api_url = api_url or os.getenv("DEEPSEEK_API_URL")
        timeout_env = timeout or os.getenv("DEEPSEEK_TIMEOUT")
        self.timeout = int(timeout_env) if timeout_env is not None else 15

        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set. Set it in the environment or pass it to DeepseekClient.")
        if not self.api_url:
            raise RuntimeError("DEEPSEEK_API_URL is not set. Set it in the environment or pass it to DeepseekClient.")

    def _build_prompt(self, moraleja: str) -> str:
        """Construct the prompt to send to Deepseek. We keep the instruction strict and include the JSON schema.

        The remote model should return a JSON object that matches the required strict format for the video pipeline.
        """
        # Keep the schema text concise but exact to improve chance of valid output.
        prompt = (
            "Genera UN SOLO JSON que cumpla con este esquema:\n"
            "Esquema: {\n"
            "  \"guion\":{\n"
            "    \"metadata\":{\n"
            "      \"titulo\":\"string\",\n"
            "      \"leccion\":\"string\",\n"
            "      \"duracion_estimada\":\"string\",\n"
            "      \"personajes\":[{\n"
            "        \"nombre\":\"string\",\n"
            "        \"tipo_voz\":\"string\",\n"
            "        \"edad_aproximada\":\"string\",\n"
            "        \"caracteristicas\":\"string\"\n"
            "      }]\n"
            "    },\n"
            "    \"escenas\":[{\n"
            "      \"numero_escena\":number,\n"
            "      \"sonido_fondo\":\"string\",\n"
            "      \"imagen_descripcion\":\"string\",\n"
            "      \"dialogo\":{\n"
            "        \"personaje\":\"string\",\n"
            "        \"texto\":\"string\",\n"
            "        \"emocion\":\"string\"\n"
            "      }\n"
            "    }]\n"
            "  }\n"
            "}\n"
            "Reglas:\n"
            "- Usar los personajes: Lucas (niño curioso, 7 años), Sofia (niña inteligente, 7 años), Abuelo Sabio (adulto sabio, 70 años).\n"
            "- Generar entre 5-8 escenas (pocas escenas, historia concisa).\n"
            "- Estructura sugerida: inicio (presentación), desarrollo (aprendizaje), cierre (moraleja).\n"
            "- Cada escena tiene 1 diálogo y descripción visual.\n"
            "- Título relacionado con la moraleja.\n"
            "- Diálogos simples para niños 5-8 años, en español.\n"
            "- Escenarios comunes: parque, casa, escuela, naturaleza.\n"
            "- Emociones variadas: curioso, feliz, sorprendido, etc.\n"
            "Moraleja: \"" + moraleja + "\"\n"
            "Devuelve únicamente el JSON, sin texto adicional."
        )

        return prompt

    def generate_guion(self, moraleja: str) -> Dict[str, Any]:
        """Call the Deepseek API to generate a guion JSON for the given moraleja.

        Returns the parsed JSON as a Python dict. Raises RuntimeError on non-2xx or parse error.
        """
        if not moraleja or not moraleja.strip():
            raise ValueError("moraleja must be a non-empty string")

        prompt = self._build_prompt(moraleja.strip())

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }

        resp = requests.post(self.api_url, headers=headers, json=payload, timeout=self.timeout)
        if not resp.ok:
            raise RuntimeError(f"Deepseek API error {resp.status_code}: {resp.text}")

        # The API returns a chat completion format
        try:
            response_data = resp.json()
            # Extract the content from the chat completion response
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                # Parse the JSON content
                return json.loads(content)
            else:
                raise RuntimeError("Unexpected response format from Deepseek API")
        except json.JSONDecodeError:
            # If the API returns raw text containing JSON, try to parse from text.
            text = resp.text.strip()
            try:
                return json.loads(text)
            except Exception as exc:
                raise RuntimeError("Failed to parse Deepseek response as JSON") from exc


if __name__ == "__main__":
    # quick local demo (will raise if env not configured)
    import argparse

    parser = argparse.ArgumentParser(description="Test Deepseek client locally")
    parser.add_argument("moraleja", help="La moraleja (texto corto)")
    args = parser.parse_args()

    client = DeepseekClient()
    result = client.generate_guion(args.moraleja)
    print(json.dumps(result, indent=2, ensure_ascii=False))
