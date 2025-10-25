"""
Filtro ético de contenidos usando Deepseek
Valida que las moralejas sean apropiadas para niños
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class ContentFilter:
    """
    Filtro ético que valida moralejas antes de generar videos.
    Rechaza contenidos que contradicen valores básicos.
    """
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
    
    def validar_moraleja(self, moraleja_input):
        """
        Valida si una moraleja es apropiada para contenido infantil educativo.
        
        Args:
            moraleja_input (str): La moraleja a validar
            
        Returns:
            dict: {
                'es_valida': bool,
                'razon': str,
                'valores_detectados': list,
                'nivel_apropiado': str
            }
        """
        
        prompt = self._build_validation_prompt(moraleja_input)
        
        try:
            response = self._call_deepseek_api(prompt)
            resultado = json.loads(response)
            return resultado
            
        except Exception as e:
            # En caso de error, ser conservador pero permitir continuar
            print(f"Error en filtro ético: {e}")
            return {
                'es_valida': True,
                'razon': 'No se pudo validar, se permite continuar',
                'valores_detectados': [],
                'nivel_apropiado': 'desconocido'
            }
    
    def _build_validation_prompt(self, moraleja):
        """Construye el prompt para el filtro ético"""
        
        return f"""Eres un filtro ético para contenido infantil educativo.
Tu trabajo es analizar moralejas y determinar si son apropiadas para niños de 5-10 años.

RECHAZA contenidos que promuevan:
- Violencia o daño físico/emocional
- Discriminación (raza, género, religión, capacidades)
- Engaño o mentira como virtud
- Egoísmo extremo o falta de empatía
- Miedo excesivo o trauma
- Irrespeto a la autoridad legítima (padres, maestros)

ACEPTA contenidos que enseñen:
- Empatía y compasión
- Honestidad y verdad
- Respeto y tolerancia
- Responsabilidad y esfuerzo
- Amistad y colaboración
- Cuidado del medio ambiente
- Seguridad personal (ej: no hablar con extraños)

Moraleja a validar: "{moraleja}"

Responde ÚNICAMENTE con un JSON válido (sin markdown, sin explicaciones):
{{
  "es_valida": true/false,
  "razon": "explicación breve de por qué es apropiada o no",
  "valores_detectados": ["lista", "de", "valores"],
  "nivel_apropiado": "excelente/aceptable/rechazado"
}}"""
    
    def _call_deepseek_api(self, prompt):
        """Llama a la API de Deepseek"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Eres un experto en contenido educativo infantil y ética.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.3,  # Más determinístico para filtros
            'max_tokens': 500
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=data,
            timeout=int(os.getenv('DEEPSEEK_TIMEOUT', '30'))
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extraer el contenido de la respuesta
        content = result['choices'][0]['message']['content'].strip()
        
        # Limpiar posibles markdown
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '').strip()
        elif content.startswith('```'):
            content = content.replace('```', '').strip()
        
        return content
