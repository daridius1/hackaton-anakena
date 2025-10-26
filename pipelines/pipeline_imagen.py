"""
Pipeline 3: Generador de Imágenes
Genera imágenes PNG para cada escena del guion usando Gemini API.

Input: guion.json
Output: assets/images/image_N.png (una por cada escena)

Implementación: Usa Gemini 2.5 Flash Image con referencias de personajes
para mantener consistencia visual.
"""
import json
import os
import unicodedata
from pathlib import Path
from typing import Dict, Any, List
from google import genai
from PIL import Image as PILImage
from .gestor_escenarios import GestorEscenarios

# ============================================================================
# CONFIGURACIÓN GEMINI
# ============================================================================

API_KEY = "AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk"

# ============================================================================
# DICCIONARIO FIJO DE PERSONAJES
# Este diccionario define las características físicas EXACTAS de cada personaje
# para mantener coherencia visual en TODAS las generaciones
# ============================================================================

PERSONAJES = {
    "sofia": {
        "nombre": "Sofia",
        "edad": "7 años",
        "descripcion_fisica_detallada": """
            - Niña de 7 años
            - Cabello: rizado castaño oscuro, largo hasta los hombros
            - Ojos: grandes, color café oscuro
            - Ropa: vestido rosa
            - Piel: tez morena clara
            - Expresión: curiosa, entusiasta
            - Estatura: promedio para su edad
            - Rasgos: cara ovalada, rizos definidos y voluminosos
        """,
        "descripcion_corta": "niña de 7 años, cabello rizado castaño oscuro hasta los hombros, vestido rosa, ojos grandes café oscuro, tez morena clara, expresión curiosa",
        "personalidad": "curiosa, entusiasta por aprender",
        "referencia": "personajes/sofia/sofia_referencia.png"
    },
    "lucas": {
        "nombre": "Lucas",
        "edad": "7 años",
        "descripcion_fisica_detallada": """
            - Niño de 7 años
            - Cabello: castaño corto, liso
            - Ojos: grandes y expresivos, color café
            - Ropa: camisa azul celeste
            - Piel: tez clara
            - Expresión: sonrisa brillante con dientes blancos
            - Estatura: promedio para su edad
            - Rasgos: cara redondeada, mejillas sonrosadas
        """,
        "descripcion_corta": "niño de 7 años, cabello castaño corto, camisa azul celeste, sonrisa brillante con dientes blancos, ojos grandes color café",
        "personalidad": "alegre, responsable, buen ejemplo",
        "referencia": "personajes/lucas/lucas_referencia.png"
    },
    "matilda": {
        "nombre": "Matilda",
        "edad": "35 años",
        "descripcion_fisica_detallada": """
            - Mujer adulta de 35 años
            - Cabello: castaño largo, lacio
            - Ojos: color café, expresivos y amables
            - Ropa: blusa celeste, pantalón casual
            - Piel: tez clara
            - Expresión: cálida, maternal, comprensiva
            - Estatura: mediana
            - Rasgos: cara ovalada, sonrisa amable, aspecto profesional
        """,
        "descripcion_corta": "mujer adulta de 35 años, cabello castaño largo lacio, blusa celeste, ojos café amables, expresión cálida y maternal",
        "personalidad": "cariñosa, responsable, protectora",
        "referencia": "personajes/matilda/matilda_referencia.png"
    },
    "carlos": {
        "nombre": "Carlos",
        "edad": "40 años",
        "descripcion_fisica_detallada": """
            - Hombre adulto de 40 años
            - Cabello: negro corto, bien peinado
            - Ojos: color café oscuro, seguros
            - Ropa: camisa blanca o polo, pantalón oscuro
            - Piel: tez morena
            - Expresión: confiable, seria pero amable
            - Estatura: alta
            - Rasgos: cara cuadrada, mandíbula definida, aspecto deportivo
        """,
        "descripcion_corta": "hombre adulto de 40 años, cabello negro corto, camisa blanca, ojos café oscuro, tez morena, expresión confiable y amable",
        "personalidad": "responsable, trabajador, paternal",
        "referencia": "personajes/carlos/carlos_referencia.png"
    },
    "don_juan": {
        "nombre": "Don Juan",
        "edad": "70 años",
        "descripcion_fisica_detallada": """
            - Adulto mayor de 70 años
            - Cabello: blanco, corto o con calvicie parcial
            - Ojos: color café claro, sabios y cálidos
            - Ropa: suéter marrón o camisa a cuadros, pantalón casual
            - Piel: tez clara con arrugas de expresión
            - Expresión: sonrisa sabia, mirada bondadosa
            - Estatura: mediana, ligeramente encorvado
            - Rasgos: cara arrugada con arrugas de sonrisa, aspecto abuelo cariñoso
        """,
        "descripcion_corta": "adulto mayor de 70 años, cabello blanco corto, suéter marrón, ojos café claro sabios, arrugas de expresión, aspecto de abuelo bondadoso",
        "personalidad": "sabio, paciente, cariñoso, contador de historias",
        "referencia": "personajes/don_juan/don_juan_referencia.png"
    },
    "doctora_martina": {
        "nombre": "Doctora Martina",
        "edad": "45 años",
        "descripcion_fisica_detallada": """
            - Mujer adulta de 45 años
            - Cabello: castaño con mechas grises, recogido en cola o moño profesional
            - Ojos: color café, inteligentes y amables
            - Ropa: bata blanca de doctora, estetoscopio al cuello
            - Accesorios: gafas rectangulares modernas
            - Piel: tez clara
            - Expresión: profesional, confiable, sonrisa tranquilizadora
            - Estatura: mediana-alta
            - Rasgos: cara ovalada, aspecto competente y amigable
        """,
        "descripcion_corta": "doctora de 45 años, cabello castaño recogido, bata blanca, gafas rectangulares, estetoscopio, expresión profesional y amable",
        "personalidad": "inteligente, empática, profesional, tranquilizadora",
        "referencia": "personajes/doctora_martina/doctora_martina_referencia.png"
    }
}


class Pipeline3Imagen:
    """Pipeline 3: Generador de imágenes para escenas usando Gemini API"""
    
    def __init__(self, output_dir: str = "assets/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = genai.Client(api_key=API_KEY)
        self.gestor_escenarios = GestorEscenarios()  # Sistema de coherencia de escenarios
    
    def _mapear_nombre_a_id(self, nombre: str) -> str:
        """Convierte nombre de personaje a ID (maneja acentos)"""
        nombre_norm = unicodedata.normalize('NFD', nombre)
        nombre_norm = ''.join(c for c in nombre_norm if unicodedata.category(c) != 'Mn')
        return nombre_norm.lower().replace(" ", "_").replace(".", "")
    
    def _obtener_personajes_del_cuento(self, escenas: List[Dict]) -> List[str]:
        """Identifica qué personajes aparecen en el cuento"""
        personajes = set()
        for escena in escenas:
            nombre = escena.get("dialogo", {}).get("personaje", "")
            pid = self._mapear_nombre_a_id(nombre)
            if pid in PERSONAJES:
                personajes.add(pid)
        return list(personajes)
    
    def _generar_imagen_con_gemini(self, descripcion: str, personajes_ids: List[str], escenario_ref: str = None) -> bytes:
        """Genera una imagen usando Gemini con referencias de personajes y escenario"""
        
        # Descripciones detalladas de personajes
        desc_personajes = "\n".join([
            f"- {PERSONAJES[p]['nombre']} ({PERSONAJES[p]['edad']}): {PERSONAJES[p]['descripcion_corta']}"
            for p in personajes_ids if p in PERSONAJES
        ])
        
        # Cargar imágenes de referencia de PERSONAJES
        referencias = []
        for pid in personajes_ids:
            if pid in PERSONAJES:
                ref_path = PERSONAJES[pid]["referencia"]
                # Buscar la ruta relativa al directorio del proyecto principal
                base_path = Path(__file__).parent.parent.parent / ref_path
                if base_path.exists():
                    referencias.append(PILImage.open(base_path))
        
        # Cargar imagen de referencia de ESCENARIO si existe
        if escenario_ref and Path(escenario_ref).exists():
            referencias.append(PILImage.open(escenario_ref))
            print(f"      🏞️  Usando referencia de escenario")
        
        # Construir prompt
        nombres_personajes = [PERSONAJES[p]['nombre'] for p in personajes_ids if p in PERSONAJES]
        
        prompt = f"""PERSONAJES QUE DEBEN APARECER EN LA IMAGEN:
{desc_personajes}

IMPORTANTE: La imagen DEBE incluir a TODOS estos personajes: {', '.join(nombres_personajes)}

ESCENA:
{descripcion}

INSTRUCCIONES CRÍTICAS:
- INCLUYE a {', '.join(nombres_personajes)} en la imagen
- MANTÉN las características EXACTAS de cada personaje según las referencias visuales
- Si hay referencia de escenario/background, MANTÉN el mismo estilo visual del lugar
- NO cambies ropa, colores, peinados ni rasgos faciales de los personajes
- NO incluir texto, diálogos ni viñetas en la imagen
- Estilo: ilustración infantil colorida, amigable, educativa
- Colores brillantes y alegres
- Composición: personajes en primer plano, escenario de fondo
"""
        
        # Generar imagen
        contenido = [prompt] + referencias
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp-image",
                contents=contenido
            )
            
            # Extraer imagen
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return part.inline_data.data
            
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                return part.inline_data.data
        except Exception as e:
            print(f"   ⚠️  Error generando imagen: {str(e)}")
            return None
        
        return None
    
    def generar(self, guion_path: str = "guion.json") -> List[str]:
        """
        Genera imágenes PNG para cada escena del guion.
        
        Args:
            guion_path: Ruta al archivo guion.json generado por Pipeline 1
            
        Returns:
            Lista de rutas a las imágenes generadas
        """
        print(f"🖼️  PIPELINE 3: Generando imágenes desde: {guion_path}...")
        
        # Leer guion
        with open(guion_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        guion = data.get("guion", {})
        escenas = guion.get("escenas", [])
        metadata = guion.get("metadata", {})
        titulo = metadata.get("titulo", "Cuento sin título")
        
        if not escenas:
            print("⚠️  No hay escenas en el guion")
            return []
        
        print(f"   📖 Título: {titulo}")
        print(f"   🎬 Escenas: {len(escenas)}")
        
        # Identificar personajes del cuento
        personajes_cuento = self._obtener_personajes_del_cuento(escenas)
        print(f"   👥 Personajes detectados: {', '.join([PERSONAJES[p]['nombre'] for p in personajes_cuento if p in PERSONAJES])}")
        
        # Analizar escenarios del cuento
        escenarios_cuento = self.gestor_escenarios.analizar_cuento(escenas)
        print(f"   🏞️  Escenarios detectados: {list(escenarios_cuento.keys())}")
        
        # Generar o cargar referencias de escenarios
        refs_escenarios = {}
        for nombre_escenario, nums_escena in escenarios_cuento.items():
            print(f"   📍 Escenario '{nombre_escenario}' aparece en escenas: {nums_escena}")
            # Obtener primera descripción como ejemplo
            ejemplo_desc = next(
                (e.get("imagen_descripcion") for e in escenas if e.get("numero_escena") in nums_escena),
                None
            )
            ruta_ref = self.gestor_escenarios.obtener_o_crear_escenario(nombre_escenario, ejemplo_desc)
            if ruta_ref:
                refs_escenarios[nombre_escenario] = ruta_ref
        
        print(f"   ⚠️  NOTA: Personajes se incluirán como referencia en TODAS las escenas")
        print(f"   ⚠️  NOTA: Escenarios se reutilizarán para mantener coherencia visual")
        print()
        
        archivos_generados = []
        
        for escena in escenas:
            num_escena = escena.get("numero_escena")
            descripcion = escena.get("imagen_descripcion")
            
            output_file = self.output_dir / f"image_{num_escena}.png"
            
            # Detectar qué escenario usar para esta escena
            escenario_ref = None
            tipo_escenario = self.gestor_escenarios.detectar_escenario(descripcion)
            if tipo_escenario and tipo_escenario in refs_escenarios:
                escenario_ref = refs_escenarios[tipo_escenario]
            
            print(f"   🎬 Escena {num_escena}...")
            print(f"      {descripcion[:80]}...")
            print(f"      � Con: {', '.join([PERSONAJES[p]['nombre'] for p in personajes_cuento if p in PERSONAJES])}")
            if escenario_ref:
                print(f"      🏞️  Escenario: {tipo_escenario}")
            
            # Generar imagen con Gemini (personajes + escenario)
            imagen_bytes = self._generar_imagen_con_gemini(descripcion, personajes_cuento, escenario_ref)
            
            if imagen_bytes:
                # Guardar imagen
                with open(output_file, "wb") as f:
                    f.write(imagen_bytes)
                
                archivos_generados.append(str(output_file))
                print(f"      ✅ Guardada: {output_file}")
            else:
                print(f"      ❌ Error en escena {num_escena}")
        
        print()
        print(f"✅ {len(archivos_generados)}/{len(escenas)} imágenes generadas en: {self.output_dir}")
        
        return archivos_generados


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 3: Generar imágenes de escenas")
    parser.add_argument("--guion", "-g", default="guion.json", help="Archivo guion.json")
    parser.add_argument("--output-dir", "-o", default="assets/images", help="Directorio de salida")
    args = parser.parse_args()
    
    pipeline = Pipeline3Imagen(output_dir=args.output_dir)
    pipeline.generar(guion_path=args.guion)
