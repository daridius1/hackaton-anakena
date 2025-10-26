#!/usr/bin/env python3
"""Genera escenarios/backgrounds con el estilo de ilustración infantil del proyecto"""

from google import genai
from PIL import Image as PILImage
from pathlib import Path

API_KEY = "AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk"
client = genai.Client(api_key=API_KEY)

# Cargar imágenes de personajes como referencia de estilo
sofia_img = PILImage.open('personajes/sofia/sofia_referencia.png')
lucas_img = PILImage.open('personajes/lucas/lucas_referencia.png')

escenarios_a_generar = {
    "bosque": {
        "nombre": "Bosque Mágico",
        "prompt": """Escenario de BOSQUE MÁGICO para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Bosque encantado con árboles altos de troncos marrones
- Hojas verdes abundantes y frondosas
- Rayos de sol dorados filtrándose entre las ramas
- Helechos y plantas al nivel del suelo
- Flores silvestres coloridas (rojas, amarillas, moradas)
- Camino de tierra serpenteante
- Mariposas y luciérnagas brillantes
- Ambiente mágico pero acogedor

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores brillantes y saturados
- Ilustración digital infantil profesional
- Perspectiva amplia del bosque
- Sin personas ni animales
- Fondo apropiado para superponer personajes
"""
    },
    "hospital": {
        "nombre": "Hospital Infantil",
        "prompt": """Escenario de HOSPITAL INFANTIL para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Interior de consultorio médico acogedor
- Paredes celestes o verde menta suave
- Camilla blanca con papel protector
- Estante con equipo médico organizado
- Ventana grande con luz natural y cortinas
- Pósters educativos alegres sobre salud
- Mesa con libros y juguetes para niños
- Plantas decorativas en macetas
- Ambiente limpio, moderno y tranquilizador

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores suaves pero vibrantes
- Ilustración digital infantil profesional
- Vista del consultorio desde la puerta
- Sin personas
- Fondo apropiado para superponer personajes
"""
    },
    "plaza": {
        "nombre": "Plaza del Pueblo",
        "prompt": """Escenario de PLAZA PÚBLICA para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Plaza colorida y alegre
- Árboles grandes con hojas verdes
- Bancas de madera pintadas de colores
- Flores en maceteros coloridos
- Pasto verde brillante
- Caminos de baldosas decorativas
- Faroles antiguos estilo parque
- Fuente pequeña con agua cristalina
- Cielo azul con nubes blancas esponjosas
- Ambiente acogedor y familiar

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores brillantes y alegres
- Ilustración digital infantil profesional
- Vista amplia de la plaza
- Sin personas
- Fondo apropiado para superponer personajes
"""
    },
    "calle": {
        "nombre": "Calle del Barrio",
        "prompt": """Escenario de CALLE URBANA para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Calle tranquila de barrio residencial
- Casas coloridas (amarilla, azul, rosada) con techos de tejas
- Veredas amplias con árboles en las aceras
- Faroles de calle modernos
- Letreros de tiendas amigables (panadería, librería)
- Macetas con flores en las ventanas
- Bicicletas apoyadas en postes
- Cielo azul con algunas nubes
- Ambiente seguro y familiar

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores vibrantes y alegres
- Ilustración digital infantil profesional
- Perspectiva de calle en ángulo
- Sin personas ni vehículos en movimiento
- Fondo apropiado para superponer personajes
"""
    },
    "habitacion": {
        "nombre": "Habitación Infantil",
        "prompt": """Escenario de HABITACIÓN INFANTIL para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Dormitorio acogedor y ordenado
- Cama con edredón colorido (estrellas o nubes)
- Ventana grande con cortinas alegres y luz natural
- Estante con libros infantiles y juguetes organizados
- Alfombra suave en el piso
- Lámpara de mesita con pantalla divertida
- Pósters educativos o de animales en las paredes
- Escritorio pequeño con crayones y papel
- Cesto con peluches
- Ambiente cálido, seguro y acogedor

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores cálidos y brillantes
- Ilustración digital infantil profesional
- Vista desde la puerta de la habitación
- Sin personas
- Fondo apropiado para superponer personajes
"""
    },
    "sala_de_clases": {
        "nombre": "Sala de Clases",
        "prompt": """Escenario de SALA DE CLASES para cuento infantil:

DESCRIPCIÓN DEL LUGAR:
- Aula escolar moderna y acogedora
- Pizarra blanca o verde al frente
- Escritorios pequeños de colores (rojos, azules, amarillos)
- Sillas proporcionales para niños
- Estantes con libros y materiales educativos
- Ventanas grandes con luz natural
- Pósters educativos alegres (números, letras, mapas)
- Mapa del mundo colorido en la pared
- Globo terráqueo en un escritorio
- Plantas decorativas
- Calendario ilustrado
- Ambiente luminoso y estimulante

ESTILO VISUAL:
- Mismo estilo de ilustración que las referencias de personajes
- Colores brillantes y educativos
- Ilustración digital infantil profesional
- Vista frontal del aula
- Sin personas
- Fondo apropiado para superponer personajes
"""
    }
}

def generar_escenario(nombre_escenario, datos):
    """Genera un escenario manteniendo el estilo de los personajes"""
    print(f"🏞️  Generando {datos['nombre']}...")
    
    prompt_completo = f"""{datos['prompt']}

REFERENCIAS DE ESTILO:
Las imágenes adjuntas muestran el estilo artístico que debes seguir exactamente.
Usa los mismos colores vibrantes, el mismo trazo y la misma técnica de ilustración digital.
"""
    
    try:
        # Pasar Sofia y Lucas como referencia de estilo artístico
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[prompt_completo, sofia_img, lucas_img]
        )
        
        # Buscar imagen en response
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    output_path = Path(f"escenarios/{nombre_escenario}_background.png")
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(part.inline_data.data)
                    print(f"   ✅ Guardado en {output_path}")
                    return True
        
        print(f"   ⚠️  No se generó imagen (solo texto)")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Generando escenarios con el estilo del proyecto...\n")
    
    generados = 0
    total = len(escenarios_a_generar)
    
    for nombre, datos in escenarios_a_generar.items():
        if generar_escenario(nombre, datos):
            generados += 1
        print()
    
    print(f"✅ {generados}/{total} escenarios generados")
