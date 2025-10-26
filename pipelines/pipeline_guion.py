"""
Pipeline 1: Generador de Guion
Genera un guion infantil estructurado en JSON a partir de una moraleja.

Input: moraleja (string)
Output: guion.json

Usa la API de Deepseek para generar historias educativas con:
- Personajes fijos: Lucas, Sofia, Abuelo Sabio
- 5-8 escenas con diálogos y descripciones visuales
- Estructura narrativa coherente
"""
import os
import json
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()


class Pipeline1Guion:
    """Pipeline 1: Generador de guiones infantiles usando Deepseek API"""
    
    def __init__(self, api_key: str | None = None, api_url: str | None = None, timeout: int | None = None, perfil_usuario=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.api_url = api_url or os.getenv("DEEPSEEK_API_URL")
        timeout_env = timeout or os.getenv("DEEPSEEK_TIMEOUT")
        self.timeout = int(timeout_env) if timeout_env is not None else 60
        self.perfil_usuario = perfil_usuario  # 🆕 Perfil para personalización

        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY no está configurada. Revisa tu archivo .env")
        if not self.api_url:
            raise RuntimeError("DEEPSEEK_API_URL no está configurada. Revisa tu archivo .env")

    def _build_prompt(self, moraleja: str) -> str:
        """Construye el prompt para Deepseek con el esquema JSON y reglas"""
        prompt_base = (
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
            "- Usar SOLO estos personajes: Lucas (niño curioso, 7 años), Sofia (niña inteligente, 7 años), Carlos (abuelo sabio, 70 años), Juan (adulto amable, 40 años), Martina (mujer adulta, 35 años).\n"
            "- NO crear personajes adicionales a los mencionados previamente\n"
            "- Generar entre 5-8 escenas (pocas escenas, historia concisa).\n"
            "- Estructura sugerida: inicio (presentación), desarrollo (aprendizaje), cierre (moraleja).\n"
            "- Cada escena tiene 1 diálogo y descripción visual.\n"
            "- Título relacionado con la moraleja.\n"
            "- Diálogos simples para niños 5-8 años, en español.\n"
            "- Para las escenas puedes elegir solamente entre estos escenarios: parque, habitación, bosque, hospital, colegio, calle.
            "- Emociones variadas: curioso, feliz, sorprendido, etc.\n"
            "Moraleja: \"" + moraleja + "\"\n"
            "Devuelve únicamente el JSON, sin texto adicional."
        )
        
        # 🆕 Aplicar personalización si hay perfil
        if self.perfil_usuario:
            from agents.story_adapter import StoryAdapter
            adapter = StoryAdapter()
            prompt_base = adapter.adaptar_prompt_guion(prompt_base, self.perfil_usuario)
        
        return prompt_base

    def _call_deepseek_api(self, prompt: str) -> Dict[str, Any]:
        """Llama a la API de Deepseek con el prompt"""
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
            raise RuntimeError(f"Error en Deepseek API {resp.status_code}: {resp.text}")

        # Extraer contenido de la respuesta de chat completion
        try:
            response_data = resp.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                raise RuntimeError("Formato de respuesta inesperado de Deepseek API")
        except json.JSONDecodeError as exc:
            raise RuntimeError("No se pudo parsear la respuesta JSON de Deepseek") from exc

    def generar(self, moraleja: str, output_path: str = "guion.json") -> Dict[str, Any]:
        """
        Genera un guion a partir de una moraleja y lo guarda en JSON.
        
        Args:
            moraleja: La moraleja de la historia (ej: "no hablar con extraños")
            output_path: Ruta donde guardar el guion.json (default: "guion.json")
            
        Returns:
            El guion generado como diccionario Python
        """
        if not moraleja or not moraleja.strip():
            raise ValueError("La moraleja debe ser un texto no vacío")

        print(f"🎨 PIPELINE 1: Generando guion para moraleja: '{moraleja}'...")
        
        prompt = self._build_prompt(moraleja.strip())
        guion = self._call_deepseek_api(prompt)
        
        # Guardar guion en archivo JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(guion, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Guion generado y guardado en: {output_path}")
        
        # Mostrar resumen
        if "guion" in guion and "metadata" in guion["guion"]:
            metadata = guion["guion"]["metadata"]
            num_escenas = len(guion["guion"].get("escenas", []))
            print(f"   Título: {metadata.get('titulo', 'N/A')}")
            print(f"   Escenas: {num_escenas}")
            print(f"   Duración estimada: {metadata.get('duracion_estimada', 'N/A')}")
        
        return guion


if __name__ == "__main__":
    # Test rápido del pipeline
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 1: Generar guion desde moraleja")
    parser.add_argument("moraleja", help="La moraleja de la historia")
    parser.add_argument("--output", "-o", default="guion.json", help="Archivo de salida")
    args = parser.parse_args()
    
    pipeline = Pipeline1Guion()
    pipeline.generar(args.moraleja, args.output)
