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

from moviepy import (
    ImageClip, AudioFileClip, CompositeAudioClip, 
    concatenate_videoclips, vfx, afx
)


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

    def generar_test(self, output_name: str = "sample_final.mp4", fade_duration: float = 0.5, dialog_delay: float = 0.8) -> str:
        """
        Genera un video de prueba de 2 escenas usando los archivos sample.
        
        Escena 1: sample_1.jpeg + sample_1.mp3 (voz) + sample_1.mp3 (fondo)
        Escena 2: sample_2.jpeg + sample_2.mp3 (voz) + sample_2.mp3 (fondo)
        
        Con transiciones fade out/in entre escenas y delay antes del diálogo.
        
        Args:
            output_name: Nombre del video de salida (default: sample_final.mp4)
            fade_duration: Duración del fade in/out en segundos (default: 0.5)
            dialog_delay: Tiempo de silencio antes del diálogo en segundos (default: 0.8)
            
        Returns:
            Ruta al video generado
        """
        print(f"🎬 PIPELINE 4 TEST: Generando video de prueba con samples...")
        print(f"   Fade duration: {fade_duration}s | Dialog delay: {dialog_delay}s")
        
        output_path = self.output_dir / output_name
        clips_escenas = []
        
        # Escena 1
        print("   Procesando Escena 1 (sample_1)...")
        image1 = self.images_dir / "sample_1.jpeg"
        voice1 = self.voices_dir / "sample_1.mp3"
        bg1 = self.sounds_dir / "sample_1.mp3"
        
        if not all([image1.exists(), voice1.exists(), bg1.exists()]):
            raise FileNotFoundError(
                f"Faltan archivos sample_1. Verifica:\n"
                f"  - {image1}\n"
                f"  - {voice1}\n"
                f"  - {bg1}"
            )
        
        # Cargar audio de voz para obtener duración
        voice_audio1 = AudioFileClip(str(voice1))
        # Duración total: delay + voz + fade out
        duration1 = dialog_delay + voice_audio1.duration + fade_duration
        
        # Crear clip de imagen con esa duración
        image_clip1 = ImageClip(str(image1), duration=duration1)
        
        # Aplicar fade in al inicio y fade out al final
        image_clip1 = image_clip1.with_effects([vfx.FadeIn(fade_duration), vfx.FadeOut(fade_duration)])
        
        # Cargar audio de fondo
        bg_audio1 = AudioFileClip(str(bg1)).with_volume_scaled(0.3)
        # El fondo empieza desde el inicio y dura toda la escena
        bg_audio1_clip = bg_audio1.subclipped(0, min(bg_audio1.duration, duration1))
        # Aplicar fade in/out al audio de fondo
        bg_audio1_clip = bg_audio1_clip.with_effects([afx.AudioFadeIn(fade_duration), afx.AudioFadeOut(fade_duration)])
        
        # El diálogo empieza después del delay
        voice_audio1_delayed = voice_audio1.with_start(dialog_delay)
        
        # Mezclar voz (con delay) + fondo (con fade)
        final_audio1 = CompositeAudioClip([bg_audio1_clip, voice_audio1_delayed])
        
        # Asignar audio al clip
        image_clip1 = image_clip1.with_audio(final_audio1)
        clips_escenas.append(image_clip1)
        
        # Escena 2
        print("   Procesando Escena 2 (sample_2)...")
        image2 = self.images_dir / "sample_2.jpeg"
        voice2 = self.voices_dir / "sample_2.mp3"
        bg2 = self.sounds_dir / "sample_2.mp3"
        
        if not all([image2.exists(), voice2.exists(), bg2.exists()]):
            raise FileNotFoundError(
                f"Faltan archivos sample_2. Verifica:\n"
                f"  - {image2}\n"
                f"  - {voice2}\n"
                f"  - {bg2}"
            )
        
        # Cargar audio de voz para obtener duración
        voice_audio2 = AudioFileClip(str(voice2))
        # Duración total: delay + voz + fade out
        duration2 = dialog_delay + voice_audio2.duration + fade_duration
        
        # Crear clip de imagen con esa duración
        image_clip2 = ImageClip(str(image2), duration=duration2)
        
        # Aplicar fade in al inicio y fade out al final
        image_clip2 = image_clip2.with_effects([vfx.FadeIn(fade_duration), vfx.FadeOut(fade_duration)])
        
        # Cargar audio de fondo
        bg_audio2 = AudioFileClip(str(bg2)).with_volume_scaled(0.3)
        # El fondo empieza desde el inicio y dura toda la escena
        bg_audio2_clip = bg_audio2.subclipped(0, min(bg_audio2.duration, duration2))
        # Aplicar fade in/out al audio de fondo
        bg_audio2_clip = bg_audio2_clip.with_effects([afx.AudioFadeIn(fade_duration), afx.AudioFadeOut(fade_duration)])
        
        # El diálogo empieza después del delay
        voice_audio2_delayed = voice_audio2.with_start(dialog_delay)
        
        # Mezclar voz (con delay) + fondo (con fade)
        final_audio2 = CompositeAudioClip([bg_audio2_clip, voice_audio2_delayed])
        
        # Asignar audio al clip
        image_clip2 = image_clip2.with_audio(final_audio2)
        clips_escenas.append(image_clip2)
        
        # Concatenar ambas escenas
        print("   Concatenando escenas...")
        video_final = concatenate_videoclips(clips_escenas, method="compose")
        
        # Exportar video
        print(f"   Exportando video a: {output_path}")
        video_final.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='medium'
        )
        
        print(f"✅ Video de prueba generado: {output_path}")
        print(f"   Duración total: {duration1 + duration2:.2f} segundos")
        print(f"   Escena 1: {duration1:.2f}s | Escena 2: {duration2:.2f}s")
        print(f"   (Cada escena: {fade_duration}s fade in + {dialog_delay}s delay + voz + {fade_duration}s fade out)")
        
        return str(output_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 4: Ensamblar video final")
    parser.add_argument("--guion", "-g", default="guion.json", help="Archivo guion.json")
    parser.add_argument("--output", "-o", default="cuento_final.mp4", help="Nombre del video")
    parser.add_argument("--test", action="store_true", help="Modo TEST: genera video con archivos sample")
    args = parser.parse_args()
    
    pipeline = Pipeline4Video()
    
    if args.test:
        pipeline.generar_test(output_name="sample_final.mp4")
    else:
        pipeline.generar(guion_path=args.guion, output_name=args.output)
