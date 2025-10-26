"""
Pipeline 3: Generador de Imágenes
Genera imágenes PNG para cada escena del guion usando Gemini API.

Input: guion.json
Output: assets/images/image_N.png (una por cada escena)

Usa gemini-2.0-flash-preview-image-generation para generar imágenes consistentes
basadas en las descripciones de characters.json
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class Pipeline3Imagen:
    """Pipeline 3: Generador de imágenes para escenas usando Gemini"""
    
    def __init__(self, output_dir: str = "assets/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar cliente Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY no está configurada. Revisa tu archivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.0-flash-preview-image-generation'
        
        # Cargar descripciones de personajes
        self.characters = self._load_characters()
        self.animation_style = self.characters.get('animation_style', {})
        self.scene_guidelines = self.characters.get('scene_guidelines', {})
    
    def _load_characters(self) -> Dict[str, Any]:
        """Carga las descripciones de personajes desde characters.json"""
        characters_path = Path("config/characters.json")
        if not characters_path.exists():
            print("⚠️  Advertencia: config/characters.json no encontrado")
            return {}
        
        with open(characters_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _build_character_description(self, character_name: str) -> str:
        """Construye descripción detallada de un personaje para el prompt"""
        characters_data = self.characters.get('characters', {})
        char_data = characters_data.get(character_name, {})
        
        if not char_data:
            return f"{character_name}"
        
        basic_info = char_data.get('basic_info', {})
        physical = char_data.get('physical_description', {})
        clothing = char_data.get('clothing', {})
        
        # Construir descripción completa
        description_parts = []
        
        # Información básica
        age = basic_info.get('age', '')
        personality = basic_info.get('personality', '')
        if age:
            description_parts.append(f"{character_name}, {age}")
        
        # Descripción física
        if physical:
            desc_items = []
            if physical.get('skin_tone'):
                desc_items.append(physical['skin_tone'])
            if physical.get('hair'):
                desc_items.append(physical['hair'])
            if physical.get('eyes'):
                desc_items.append(physical['eyes'])
            if physical.get('build'):
                desc_items.append(physical['build'])
            
            if desc_items:
                description_parts.append(", ".join(desc_items))
        
        # Vestimenta
        if clothing:
            clothing_items = []
            for key, value in clothing.items():
                if isinstance(value, dict):
                    # Extraer colores y tipos principales
                    if 'color' in value:
                        clothing_items.append(f"{value.get('color', '')} {key}")
                    elif 'main_color' in value:
                        clothing_items.append(f"{value.get('main_color', '')} {key}")
            
            if clothing_items:
                description_parts.append("wearing " + ", ".join(clothing_items))
        
        return "; ".join(description_parts)
    
    def _build_image_prompt(self, escena: Dict[str, Any]) -> str:
        """Construye el prompt para generar la imagen de una escena"""
        descripcion = escena.get("imagen_descripcion", "")
        dialogo = escena.get("dialogo", {})
        personaje_hablando = dialogo.get("personaje", "")
        sonido_fondo = escena.get("sonido_fondo", "")
        
        # Estilo de animación base
        style_desc = self.animation_style.get('description', '')
        art_chars = self.animation_style.get('art_characteristics', [])
        
        # Construir prompt
        prompt_parts = []
        
        # Estilo artístico
        prompt_parts.append(f"Style: {style_desc}")
        if art_chars:
            prompt_parts.append("Art style: " + "; ".join(art_chars[:3]))
        
        # Escena principal
        prompt_parts.append(f"Scene: {descripcion}")
        
        # Personajes (extraer de la descripción o del diálogo)
        # Intentar identificar personajes mencionados
        characters_in_scene = []
        all_char_names = list(self.characters.get('characters', {}).keys())
        
        text_to_search = (descripcion + " " + personaje_hablando).lower()
        for char_name in all_char_names:
            if char_name.lower() in text_to_search:
                characters_in_scene.append(char_name)
        
        # Agregar descripciones de personajes
        if characters_in_scene:
            prompt_parts.append("Characters in scene:")
            for char in characters_in_scene:
                char_desc = self._build_character_description(char)
                prompt_parts.append(f"- {char_desc}")
        
        # Ambiente basado en sonido de fondo
        if sonido_fondo:
            location_map = {
                'park': 'outdoor park setting',
                'parque': 'outdoor park setting',
                'forest': 'forest setting with trees',
                'bosque': 'forest setting with trees',
                'hospital': 'hospital or medical setting',
                'school': 'school or classroom setting',
                'colegio': 'school or classroom setting',
                'street': 'street or urban setting',
                'calle': 'street or urban setting'
            }
            
            for key, desc in location_map.items():
                if key in sonido_fondo.lower():
                    prompt_parts.append(f"Setting: {desc}")
                    break
        
        # Guidelines de escena
        lighting = self.scene_guidelines.get('lighting', '')
        color_palette = self.scene_guidelines.get('color_palette', '')
        
        if lighting:
            prompt_parts.append(f"Lighting: {lighting}")
        if color_palette:
            prompt_parts.append(f"Colors: {color_palette}")
        
        # Importante: para niños
        prompt_parts.append("Child-friendly, educational, safe for ages 5-8")
        
        return ". ".join(prompt_parts)
    
    def _generate_image(self, prompt: str) -> bytes:
        """Genera una imagen usando Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],  # CRÍTICO: ambas modalidades
                )
            )
            
            # Extraer imagen de la respuesta
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    return part.inline_data.data
            
            print("      ⚠️  No se encontró imagen en la respuesta")
            return None
            
        except Exception as e:
            print(f"      ❌ Error generando imagen: {str(e)}")
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
        titulo = metadata.get("titulo", "Sin título")
        
        print(f"   📖 Título: {titulo}")
        print(f"   🎬 Total escenas: {len(escenas)}")
        
        archivos_generados = []
        exitos = 0
        
        for escena in escenas:
            num_escena = escena.get("numero_escena")
            descripcion = escena.get("imagen_descripcion", "")
            
            output_file = self.output_dir / f"image_{num_escena}.png"
            
            print(f"\n   🎬 Escena {num_escena}...")
            print(f"      {descripcion[:80]}...")
            
            # Construir prompt
            prompt = self._build_image_prompt(escena)
            
            # Generar imagen
            image_data = self._generate_image(prompt)
            
            if image_data:
                # Guardar imagen
                try:
                    image = Image.open(BytesIO(image_data))
                    image.save(output_file)
                    archivos_generados.append(str(output_file))
                    exitos += 1
                    print(f"      ✅ Imagen guardada: {output_file.name}")
                except Exception as e:
                    print(f"      ❌ Error guardando imagen: {str(e)}")
            else:
                # Crear placeholder si falla
                output_file.touch()
                archivos_generados.append(str(output_file))
                print(f"      ⚠️  Placeholder creado")
        
        print(f"\n✅ {exitos}/{len(escenas)} imágenes generadas exitosamente en: {self.output_dir}")
        
        return archivos_generados


if __name__ == "__main__":
    # Test rápido del pipeline
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 3: Generar imágenes desde guion")
    parser.add_argument("guion", nargs="?", default="guion.json", help="Archivo guion.json")
    parser.add_argument("--output", "-o", default="assets/images", help="Directorio de salida")
    args = parser.parse_args()
    
    pipeline = Pipeline3Imagen(output_dir=args.output)
    pipeline.generar(args.guion)

