#!/usr/bin/env python3
"""Script para generar imágenes de referencia de personajes faltantes"""

from google import genai
from pathlib import Path

API_KEY = "AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk"
client = genai.Client(api_key=API_KEY)

personajes_a_generar = {
    "carlos": {
        "nombre": "Carlos",
        "descripcion": """Hombre adulto de 40 años
- Cabello: negro corto, bien peinado
- Ojos: color café oscuro, seguros
- Ropa: camisa blanca, pantalón oscuro
- Piel: tez morena
- Expresión: confiable, seria pero amable
- Estatura: alta
- Rasgos: cara cuadrada, mandíbula definida, aspecto deportivo"""
    },
    "juan": {
        "nombre": "Juan",
        "descripcion": """Adulto mayor de 70 años
- Cabello: blanco, corto o con calvicie parcial
- Ojos: color café claro, sabios y cálidos
- Ropa: suéter marrón o camisa a cuadros, pantalón casual
- Piel: tez clara con arrugas de expresión
- Expresión: sonrisa sabia, mirada bondadosa
- Estatura: mediana, ligeramente encorvado
- Rasgos: cara arrugada con arrugas de sonrisa, aspecto abuelo cariñoso"""
    },
    "martina": {
        "nombre": "Martina",
        "descripcion": """Mujer adulta de 45 años
- Cabello: castaño con mechas grises, recogido en cola o moño profesional
- Ojos: color café, inteligentes y amables
- Ropa: bata blanca de doctora, estetoscopio al cuello
- Accesorios: gafas rectangulares modernas
- Piel: tez clara
- Expresión: profesional, confiable, sonrisa tranquilizadora
- Estatura: mediana-alta
- Rasgos: cara ovalada, aspecto competente y amigable"""
    }
}

def generar_personaje(pid, datos):
    """Genera la imagen de referencia de un personaje"""
    print(f"📸 Generando {datos['nombre']}...")
    
    prompt = f"""Genera una imagen de referencia de personaje para cuento infantil:

{datos['nombre'].upper()}
{datos['descripcion']}

IMPORTANTE:
- Vista frontal, cuerpo completo
- Fondo blanco simple
- Estilo: ilustración infantil colorida, amigable, educativa
- NO incluir texto ni diálogos
- Expresión amigable
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                output_path = Path(f"personajes/{pid}/{pid}_referencia.png")
                output_path.write_bytes(part.inline_data.data)
                print(f"   ✅ Guardado en {output_path}")
                return True
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print(f"   ❌ No se pudo generar")
    return False

if __name__ == "__main__":
    print("🎨 Generando personajes faltantes...\n")
    
    for pid, datos in personajes_a_generar.items():
        generar_personaje(pid, datos)
        print()
    
    print("✅ Proceso completado")
