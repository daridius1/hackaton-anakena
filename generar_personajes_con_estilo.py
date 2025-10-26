#!/usr/bin/env python3
"""Genera personajes faltantes usando el estilo de los existentes"""

from google import genai
from PIL import Image as PILImage
from pathlib import Path

API_KEY = "AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk"
client = genai.Client(api_key=API_KEY)

# Cargar imágenes de referencia de estilo (Sofia y Lucas)
sofia_img = PILImage.open('personajes/sofia/sofia_referencia.png')
lucas_img = PILImage.open('personajes/lucas/lucas_referencia.png')

personajes_a_generar = {
    "carlos": {
        "nombre": "Carlos",
        "descripcion": """Hombre adulto de 40 años
- Cabello: negro corto, bien peinado
- Ojos: café oscuro, seguros
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
- Ojos: café claro, sabios y cálidos
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
- Ojos: café, inteligentes y amables
- Ropa: bata blanca de doctora, estetoscopio al cuello
- Accesorios: gafas rectangulares modernas
- Piel: tez clara
- Expresión: profesional, confiable, sonrisa tranquilizadora
- Estatura: mediana-alta
- Rasgos: cara ovalada, aspecto competente y amigable"""
    }
}

def generar_personaje(pid, datos):
    """Genera personaje manteniendo el estilo de Sofia y Lucas"""
    print(f"📸 Generando {datos['nombre']}...")
    
    prompt = f"""Genera una imagen de personaje para cuento infantil siguiendo EXACTAMENTE el mismo estilo artístico de las imágenes de referencia:

{datos['nombre'].upper()}
{datos['descripcion']}

IMPORTANTE - MANTENER EL MISMO ESTILO:
- Usar el mismo estilo de ilustración que las referencias
- Mismo tipo de líneas, colores y sombreado
- Misma proporción de cuerpo y cabeza
- Vista frontal, cuerpo completo
- Fondo blanco simple
- Estilo: ilustración infantil colorida, IGUAL que las referencias
- NO incluir texto ni diálogos
- Expresión amigable y accesible
"""
    
    try:
        # Pasar las imágenes de Sofia y Lucas como referencia de estilo
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[prompt, sofia_img, lucas_img]
        )
        
        # Buscar imagen en response.parts
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    output_path = Path(f"personajes/{pid}/{pid}_referencia.png")
                    output_path.write_bytes(part.inline_data.data)
                    print(f"   ✅ Guardado en {output_path}")
                    return True
        
        # Buscar en candidates
        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            output_path = Path(f"personajes/{pid}/{pid}_referencia.png")
                            output_path.write_bytes(part.inline_data.data)
                            print(f"   ✅ Guardado en {output_path}")
                            return True
        
        print(f"   ⚠️  No se generó imagen (solo texto)")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Generando personajes con el estilo de Sofia y Lucas...\n")
    
    for pid, datos in personajes_a_generar.items():
        generar_personaje(pid, datos)
        print()
    
    print("✅ Proceso completado")
