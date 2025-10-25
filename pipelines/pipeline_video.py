"""
Pipeline 4: Ensamblador de Video
Combina imágenes, audio de diálogos y sonidos de fondo en un video MP4 final.

Input: 
  - guion.json
  - assets/voices/dialogue_N.mp3
  - assets/images/image_N.png
  - assets/background_sounds/*.mp3
  
Output: assets/outputs/cuento_final.mp4

Usa MoviePy para ensamblar el video escena por escena.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List

# TODO: Descomentar cuando se instale moviepy
# from moviepy.editor import (
#     ImageClip, AudioFileClip, CompositeAudioClip, 
#     concatenate_videoclips, CompositeVideoClip
# )


class Pipeline4Video:
    """Pipeline 4: Ensamblador de video final"""
    
    def __init__(
        self, 
        output_dir: str = "assets/outputs",
        voices_dir: str = "assets/voices",
        images_dir: str = "assets/images",
        sounds_dir: str = "assets/background_sounds"
    ):
        self.output_dir = Path(output_dir)
        self.voices_dir = Path(voices_dir)
        self.images_dir = Path(images_dir)
        self.sounds_dir = Path(sounds_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generar(self, guion_path: str = "guion.json", output_name: str = "cuento_final.mp4") -> str:
        """
        Ensambla el video final combinando todos los assets.
        
        Args:
            guion_path: Ruta al archivo guion.json
            output_name: Nombre del video de salida
            
        Returns:
            Ruta al video generado
        """
        print(f"🎬 PIPELINE 4: Ensamblando video desde: {guion_path}...")
        
        # Leer guion
        with open(guion_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        guion = data.get("guion", {})
        metadata = guion.get("metadata", {})
        escenas = guion.get("escenas", [])
        
        output_path = self.output_dir / output_name
        
        print(f"   Título: {metadata.get('titulo')}")
        print(f"   Total escenas: {len(escenas)}")
        
        # TODO: IMPLEMENTAR ENSAMBLAJE CON MOVIEPY
        # clips_escenas = []
        # 
        # for escena in escenas:
        #     num = escena["numero_escena"]
        #     
        #     # Cargar imagen
        #     image_path = self.images_dir / f"image_{num}.png"
        #     
        #     # Cargar audio del diálogo
        #     dialogue_path = self.voices_dir / f"dialogue_{num}.mp3"
        #     dialogue_audio = AudioFileClip(str(dialogue_path))
        #     
        #     # Crear clip de video con la imagen (duración = duración del audio)
        #     image_clip = ImageClip(str(image_path), duration=dialogue_audio.duration)
        #     
        #     # Buscar y cargar sonido de fondo
        #     bg_sound = self._get_background_sound(escena["sonido_fondo"])
        #     if bg_sound:
        #         bg_audio = AudioFileClip(bg_sound).volumex(0.3)  # Volumen más bajo
        #         bg_audio = bg_audio.subclip(0, dialogue_audio.duration)
        #         # Mezclar audio del diálogo con fondo
        #         final_audio = CompositeAudioClip([dialogue_audio, bg_audio])
        #     else:
        #         final_audio = dialogue_audio
        #     
        #     # Añadir audio al clip de imagen
        #     image_clip = image_clip.set_audio(final_audio)
        #     clips_escenas.append(image_clip)
        # 
        # # Concatenar todas las escenas
        # video_final = concatenate_videoclips(clips_escenas, method="compose")
        # 
        # # Exportar video
        # video_final.write_videofile(
        #     str(output_path),
        #     fps=24,
        #     codec='libx264',
        #     audio_codec='aac'
        # )
        
        # Por ahora, crear archivo placeholder
        output_path.touch()
        
        print(f"✅ Video generado en: {output_path}")
        print(f"⚠️  NOTA: Pipeline 4 es un PLACEHOLDER. Instalar moviepy y descomentar código.")
        
        return str(output_path)
    
    def _get_background_sound(self, descripcion: str) -> str | None:
        """
        Busca el archivo de sonido de fondo apropiado según la descripción.
        
        Args:
            descripcion: Descripción del sonido de fondo del guion (ej: "Pájaros cantando")
            
        Returns:
            Ruta al archivo de audio o None si no se encuentra
        """
        # Mapeo simple de descripciones a archivos
        # TODO: Mejorar con fuzzy matching o búsqueda más inteligente
        mapeo = {
            "pajaros": "pajaros.mp3",
            "parque": "parque.mp3",
            "casa": "casa.mp3",
            "escuela": "escuela.mp3",
            "naturaleza": "naturaleza.mp3",
            "viento": "viento.mp3",
            "silencio": "silencio.mp3",
        }
        
        descripcion_lower = descripcion.lower()
        
        for keyword, filename in mapeo.items():
            if keyword in descripcion_lower:
                filepath = self.sounds_dir / filename
                if filepath.exists():
                    return str(filepath)
        
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 4: Ensamblar video final")
    parser.add_argument("--guion", "-g", default="guion.json", help="Archivo guion.json")
    parser.add_argument("--output", "-o", default="cuento_final.mp4", help="Nombre del video")
    args = parser.parse_args()
    
    pipeline = Pipeline4Video()
    pipeline.generar(guion_path=args.guion, output_name=args.output)
