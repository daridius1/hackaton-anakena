"""
Motor de preferencias que genera sugerencias personalizadas
Usa Deepseek para analizar perfil y historial del usuario
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class PreferenceEngine:
    """
    Motor que genera sugerencias de moralejas personalizadas
    basadas en el perfil del usuario y su historial.
    """
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
    
    def generar_sugerencias(self, perfil_usuario, historial_interacciones, n=5):
        """
        Genera sugerencias personalizadas de moralejas.
        
        Args:
            perfil_usuario: Instancia de PerfilUsuario
            historial_interacciones: QuerySet de InteraccionSugerencia
            n: Número de sugerencias a generar
            
        Returns:
            list: Lista de diccionarios con sugerencias
        """
        
        prompt = self._build_suggestion_prompt(perfil_usuario, historial_interacciones, n)
        
        try:
            response = self._call_deepseek_api(prompt)
            resultado = json.loads(response)
            return resultado.get('sugerencias', [])
            
        except Exception as e:
            print(f"Error generando sugerencias: {e}")
            return self._get_sugerencias_default()
    
    def _build_suggestion_prompt(self, perfil, historial, n):
        """Construye el prompt para generar sugerencias basadas solo en valores pendientes"""
        
        # Obtener valores ya cubiertos del historial
        valores_trabajados = set()
        moralejas_vistas = []
        
        for interaccion in historial[:20]:  # Últimas 20 interacciones
            valores_trabajados.update(interaccion.valores_cubiertos)
            moralejas_vistas.append(interaccion.moraleja_sugerida)
        
        # Valores pendientes (los que el usuario quiere pero no ha trabajado)
        valores_prioritarios = set(perfil.valores_prioritarios) if perfil.valores_prioritarios else set()
        valores_pendientes = valores_prioritarios - valores_trabajados
        
        # Si no hay valores pendientes, usar todos los valores prioritarios
        if not valores_pendientes:
            valores_pendientes = valores_prioritarios
        
        # Si no hay valores prioritarios definidos, usar valores educativos generales
        if not valores_pendientes:
            valores_pendientes = {'empatía', 'honestidad', 'responsabilidad', 'respeto', 'solidaridad'}
        
        return f"""Eres un agente educativo experto en crear contenido infantil educativo.
Tu trabajo es sugerir moralejas que enseñen valores que el usuario AÚN NO ha trabajado.

VALORES PRIORITARIOS DEL USUARIO: {', '.join(valores_prioritarios) if valores_prioritarios else 'no especificados'}
VALORES YA TRABAJADOS: {', '.join(valores_trabajados) if valores_trabajados else 'ninguno'}
VALORES PENDIENTES (PRIORIDAD MÁXIMA): {', '.join(valores_pendientes)}

MORALEJAS YA VISTAS (evitar repetir): {', '.join(moralejas_vistas[:10]) if moralejas_vistas else 'ninguna'}

INSTRUCCIONES:
Genera {n} sugerencias de moralejas educativas que:
1. **PRIORIDAD:** Cubrir los valores pendientes
2. Sean apropiadas para niños de 5-10 años
3. **NO REPETIR** moralejas ya vistas
4. Sean simples y claras (máximo 60 caracteres)

Responde ÚNICAMENTE con un JSON válido (sin markdown):
{{
  "sugerencias": [
    {{
      "moraleja": "texto corto de la moraleja (ej: 'respetar a los mayores')",
      "razon": "por qué se sugiere (qué valor cubre que falta)",
      "valores": ["lista", "de", "valores", "que", "enseña"],
      "prioridad": 5
    }}
  ]
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
                    'content': 'Eres un experto en pedagogía infantil y contenido educativo personalizado.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,  # Más creativo para sugerencias
            'max_tokens': 1000
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
    
    def _get_sugerencias_default(self):
        """Sugerencias por defecto en caso de error"""
        return [
            {
                'moraleja': 'compartir con los demás',
                'razon': 'Enseña generosidad y empatía',
                'valores': ['empatía', 'generosidad'],
                'prioridad': 5
            },
            {
                'moraleja': 'ser honesto siempre',
                'razon': 'Refuerza la importancia de la verdad',
                'valores': ['honestidad', 'integridad'],
                'prioridad': 5
            },
            {
                'moraleja': 'cuidar la naturaleza',
                'razon': 'Conciencia ambiental desde temprana edad',
                'valores': ['responsabilidad', 'respeto'],
                'prioridad': 4
            },
            {
                'moraleja': 'ayudar a quien lo necesita',
                'razon': 'Desarrolla empatía y solidaridad',
                'valores': ['empatía', 'solidaridad'],
                'prioridad': 4
            },
            {
                'moraleja': 'ser valiente ante los miedos',
                'razon': 'Desarrolla resiliencia y confianza',
                'valores': ['valentía', 'confianza'],
                'prioridad': 3
            }
        ]
