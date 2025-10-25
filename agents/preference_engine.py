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
        """Construye el prompt para generar sugerencias"""
        
        # Obtener valores ya cubiertos
        valores_vistos = set()
        moralejas_vistas = []
        moralejas_seleccionadas = []
        moralejas_rechazadas = []
        
        for interaccion in historial[:20]:  # Últimas 20 interacciones
            valores_vistos.update(interaccion.valores_cubiertos)
            moralejas_vistas.append(interaccion.moraleja_sugerida)
            
            # Analizar qué fue seleccionado vs rechazado
            if interaccion.fue_seleccionada or interaccion.video_generado:
                moralejas_seleccionadas.append({
                    'moraleja': interaccion.moraleja_sugerida,
                    'valores': interaccion.valores_cubiertos
                })
            else:
                moralejas_rechazadas.append(interaccion.moraleja_sugerida)
        
        # Valores pendientes
        valores_prioritarios = set(perfil.valores_prioritarios)
        valores_pendientes = valores_prioritarios - valores_vistos
        
        # Detectar patrones: ¿Qué valores se seleccionan más?
        valores_populares = []
        if moralejas_seleccionadas:
            contador_valores = {}
            for item in moralejas_seleccionadas:
                for valor in item['valores']:
                    contador_valores[valor] = contador_valores.get(valor, 0) + 1
            valores_populares = sorted(contador_valores.items(), key=lambda x: x[1], reverse=True)[:3]
            valores_populares = [v[0] for v in valores_populares]
        
        return f"""Eres un agente educativo experto en crear contenido personalizado para niños.
Tu trabajo es sugerir moralejas educativas basándote en el perfil del usuario Y SU HISTORIAL.

PERFIL DEL USUARIO:
- Edad del niño: {perfil.edad_nino} años
- Nivel de complejidad: {perfil.nivel_complejidad}
- Estilo narrativo preferido: {perfil.estilo_narrativo}
- Temas favoritos: {', '.join(perfil.temas_favoritos) if perfil.temas_favoritos else 'ninguno especificado'}
- Valores prioritarios: {', '.join(perfil.valores_prioritarios) if perfil.valores_prioritarios else 'ninguno especificado'}

ANÁLISIS DEL HISTORIAL:
- Total de sugerencias mostradas: {len(moralejas_vistas)}
- Moralejas que SÍ seleccionó ({len(moralejas_seleccionadas)}): {', '.join([m['moraleja'] for m in moralejas_seleccionadas[:5]]) if moralejas_seleccionadas else 'ninguna aún'}
- Moralejas que NO seleccionó (rechazadas): {', '.join(moralejas_rechazadas[:5]) if moralejas_rechazadas else 'ninguna'}
- Valores más populares (los que más elige): {', '.join(valores_populares) if valores_populares else 'sin datos'}
- Valores ya cubiertos: {', '.join(valores_vistos) if valores_vistos else 'ninguno'}
- Valores pendientes (PRIORIDAD ALTA): {', '.join(valores_pendientes) if valores_pendientes else 'todos cubiertos'}

PATRÓN DETECTADO:
{self._describir_patron(moralejas_seleccionadas, valores_populares, perfil)}

INSTRUCCIONES:
Genera {n} sugerencias de moralejas que:
1. **PRIORIDAD MÁXIMA:** Cubrir valores pendientes que aún no ha visto
2. **APRENDER DEL HISTORIAL:** Evitar temas similares a los rechazados
3. **REFORZAR PATRONES:** Si le gustan ciertos valores, incluir más de esos
4. Se adapten a la edad ({perfil.edad_nino} años) y nivel ({perfil.nivel_complejidad})
5. Incorporen los temas favoritos: {', '.join(perfil.temas_favoritos) if perfil.temas_favoritos else 'general'}
6. Tengan un enfoque {perfil.estilo_narrativo}
7. **NO REPETIR** moralejas ya vistas

Responde ÚNICAMENTE con un JSON válido (sin markdown):
{{
  "sugerencias": [
    {{
      "moraleja": "texto corto de la moraleja (máx 60 caracteres)",
      "razon": "por qué se sugiere BASADO EN SU HISTORIAL",
      "valores": ["lista", "de", "valores"],
      "prioridad": 1-5
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
    
    def _describir_patron(self, moralejas_seleccionadas, valores_populares, perfil):
        """Describe el patrón de comportamiento del usuario"""
        if not moralejas_seleccionadas:
            return f"Usuario nuevo, sin historial. Usar valores prioritarios: {', '.join(perfil.valores_prioritarios)}"
        
        if valores_populares:
            return f"Este usuario prefiere historias sobre: {', '.join(valores_populares)}. Sugerir más de estos temas."
        
        return "Historial limitado, explorar diferentes valores."
    
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
