#!/usr/bin/env python3
"""Genera todas las imágenes de referencia de personajes y escenarios"""

import google.generativeai as genai
from pathlib import Path

genai.configure(api_key='AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk')
model = genai.GenerativeModel('gemini-2.5-flash')

# Personajes
personajes = {
    "carlos": """CARLOS - Hombre adulto de 40 años
- Cabello: negro corto, bien peinado
- Ojos: café oscuro
- Ropa: camisa blanca
- Piel: tez morena
- Expresión: confiable y amable
- Vista frontal, cuerpo completo
- Fondo blanco simple
- Estilo: ilustración infantil colorida
- NO incluir texto""",
    
    "juan": """JUAN - Adulto mayor de 70 años
- Cabello: blanco corto
- Ojos: café claro, sabios
- Ropa: suéter marrón
- Piel: tez clara con arrugas
- Expresión: bondadosa, abuelo cariñoso
- Vista frontal, cuerpo completo
- Fondo blanco simple
- Estilo: ilustración infantil colorida
- NO incluir texto""",
    
    "martina": """MARTINA - Doctora de 45 años
- Cabello: castaño recogido
- Ojos: café, inteligentes
- Ropa: bata blanca de doctora, estetoscopio
- Accesorios: gafas rectangulares
- Piel: tez clara
- Expresión: profesional y amable
- Vista frontal, cuerpo completo
- Fondo blanco simple
- Estilo: ilustración infantil colorida
- NO incluir texto"""
}

# Escenarios
escenarios = {
    "bosque": """Bosque chileno - Escenario para cuento infantil
- Árboles nativos (araucarias, arrayanes)
- Vegetación verde
- Luz natural suave
- Atmósfera mágica y acogedora
- Sin personajes
- Estilo: ilustración infantil colorida
- Perspectiva amplia para superponer personajes""",
    
    "hospital": """Hospital - Escenario para cuento infantil
- Sala de hospital limpia y amigable
- Colores claros y cálidos
- Ventanas con luz natural
- Ambiente tranquilizador
- Sin personajes
- Estilo: ilustración infantil colorida
- NO texto visible""",
    
    "plaza": """Plaza chilena - Escenario para cuento infantil
- Plaza con árboles y bancas
- Juegos infantiles al fondo
- Cielo despejado
- Ambiente alegre y seguro
- Sin personajes
- Estilo: ilustración infantil colorida
- Vista amplia""",
    
    "calle": """Calle de barrio chileno - Escenario para cuento infantil
- Calle residencial tranquila
- Casas coloridas
- Veredas limpias
- Ambiente acogedor
- Sin personajes
- Estilo: ilustración infantil colorida
- Vista de calle""",
    
    "habitacion": """Habitación infantil - Escenario para cuento infantil
- Dormitorio cálido y acogedor
- Cama, juguetes, ventana
- Colores alegres
- Ambiente seguro
- Sin personajes
- Estilo: ilustración infantil colorida
- Vista interior""",
    
    "sala_de_clases": """Sala de clases - Escenario para cuento infantil
- Aula escolar luminosa
- Pizarra, pupitres
- Decoraciones educativas
- Ambiente alegre de aprendizaje
- Sin personajes
- Estilo: ilustración infantil colorida
- Vista del salón"""
}

def generar_imagen(nombre, prompt, carpeta):
    """Genera y guarda una imagen"""
    print(f"📸 Generando {nombre}...")
    try:
        response = model.generate_content(
            f"Genera una imagen de referencia para cuento infantil:\n\n{prompt}"
        )
        
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    output_path = Path(f"{carpeta}/{nombre}_{'referencia' if 'personajes' in carpeta else 'background'}.png")
                    output_path.write_bytes(part.inline_data.data)
                    print(f"   ✅ Guardado en {output_path}")
                    return True
        print(f"   ⚠️  No se generó imagen")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

print("🎨 GENERANDO PERSONAJES\n")
for nombre, prompt in personajes.items():
    generar_imagen(nombre, prompt, f"personajes/{nombre}")
    print()

print("\n🏞️  GENERANDO ESCENARIOS\n")
for nombre, prompt in escenarios.items():
    generar_imagen(nombre, prompt, "escenarios")
    print()

print("✅ Proceso completado")
