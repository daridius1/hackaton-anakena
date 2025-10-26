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
    
    def generar(
        self, 
        guion_path: str = "guion.json", 
        output_name: str = "cuento_final.mp4",
        fade_duration: float = 0.5,
        dialog_delay: float = 0.8,
        bg_volume: float = 0.3,
        music_volume: float = 0.15
    ) -> str:
        """
        Ensambla el video final combinando todos los assets.
        
        Args:
            guion_path: Ruta al archivo guion.json
            output_name: Nombre del video de salida
            fade_duration: Duración del fade in/out en segundos
            dialog_delay: Tiempo de silencio antes del diálogo en segundos
            bg_volume: Volumen del audio de fondo ambiental (0.0-1.0)
            music_volume: Volumen de la música de fondo general (0.0-1.0)
            
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
        titulo = metadata.get("titulo", "Sin título")
        
        output_path = self.output_dir / output_name
        
        print(f"   Título: {titulo}")
        print(f"   Total escenas: {len(escenas)}")
        print(f"   Configuración: fade={fade_duration}s, delay={dialog_delay}s, bg_vol={bg_volume}, music_vol={music_volume}")
        
        clips_escenas = []
        duracion_total = 0
        
        for escena in escenas:
            num = escena["numero_escena"]
            print(f"\n   🎬 Procesando Escena {num}...")
            
            # Rutas de archivos
            image_path = self.images_dir / f"image_{num}.png"
            dialogue_path = self.voices_dir / f"dialogue_{num}.mp3"
            
            # Verificar que existan los archivos necesarios
            if not image_path.exists():
                print(f"      ⚠️  Imagen no encontrada: {image_path}")
                continue
            
            if not dialogue_path.exists():
                print(f"      ⚠️  Audio de diálogo no encontrado: {dialogue_path}")
                continue
            
            # Cargar audio de voz para obtener duración
            voice_audio = AudioFileClip(str(dialogue_path))
            # Duración total: delay + voz + fade out
            duration = dialog_delay + voice_audio.duration + fade_duration
            
            # Crear clip de imagen con esa duración
            image_clip = ImageClip(str(image_path), duration=duration)
            
            # Aplicar fade in al inicio y fade out al final
            image_clip = image_clip.with_effects([vfx.FadeIn(fade_duration), vfx.FadeOut(fade_duration)])
            
            # Buscar y cargar sonido de fondo AMBIENTAL basado en el ESCENARIO
            imagen_descripcion = escena.get("imagen_descripcion", "")
            bg_sound_path = self._get_background_sound(imagen_descripcion)
            
            if bg_sound_path and Path(bg_sound_path).exists():
                print(f"      🎵 Sonido ambiental: {Path(bg_sound_path).name} (escenario: {imagen_descripcion[:40]}...)")
                # Cargar audio de fondo ambiental
                bg_audio = AudioFileClip(bg_sound_path).with_volume_scaled(bg_volume)
                # El fondo empieza desde el inicio y dura toda la escena
                bg_audio_clip = bg_audio.subclipped(0, min(bg_audio.duration, duration))
                # Aplicar fade in/out al audio de fondo
                bg_audio_clip = bg_audio_clip.with_effects([
                    afx.AudioFadeIn(fade_duration), 
                    afx.AudioFadeOut(fade_duration)
                ])
                
                # El diálogo empieza después del delay
                voice_audio_delayed = voice_audio.with_start(dialog_delay)
                
                # Mezclar voz (con delay) + fondo ambiental (con fade)
                final_audio = CompositeAudioClip([bg_audio_clip, voice_audio_delayed])
            else:
                print(f"      🔇 Sin sonido ambiental para: {imagen_descripcion[:40]}...")
                # Solo voz con delay
                voice_audio_delayed = voice_audio.with_start(dialog_delay)
                final_audio = voice_audio_delayed
            
            # Asignar audio al clip
            image_clip = image_clip.with_audio(final_audio)
            clips_escenas.append(image_clip)
            
            duracion_total += duration
            print(f"      ✅ Escena {num} procesada ({duration:.2f}s)")
        
        if not clips_escenas:
            raise RuntimeError("No se pudo procesar ninguna escena. Verifica que existan las imágenes y audios.")
        
        # Concatenar todas las escenas
        print(f"\n   📦 Concatenando {len(clips_escenas)} escenas...")
        video_final = concatenate_videoclips(clips_escenas, method="compose")
        
        # 🎵 AGREGAR MÚSICA DE FONDO A TODO EL VIDEO
        song_path = self.sounds_dir / "song.mp3"
        if song_path.exists():
            print(f"   🎶 Agregando música de fondo a todo el video: {song_path.name}")
            music_audio = AudioFileClip(str(song_path)).with_volume_scaled(music_volume)
            
            # Hacer loop de la música si el video es más largo
            if music_audio.duration < duracion_total:
                # Repetir la música en loop
                num_loops = int(duracion_total / music_audio.duration) + 1
                music_audio = music_audio.with_effects([afx.AudioLoop(duration=duracion_total)])
                print(f"      🔁 Música en loop para cubrir {duracion_total:.2f}s")
            else:
                # Cortar la música a la duración del video
                music_audio = music_audio.subclipped(0, duracion_total)
            
            # Aplicar fade in/out a la música
            music_audio = music_audio.with_effects([
                afx.AudioFadeIn(1.0),
                afx.AudioFadeOut(2.0)
            ])
            
            # Combinar el audio existente del video con la música de fondo
            final_audio_with_music = CompositeAudioClip([video_final.audio, music_audio])
            video_final = video_final.with_audio(final_audio_with_music)
            print(f"      ✅ Música de fondo agregada (volumen: {music_volume})")
        else:
            print(f"   ⚠️  No se encontró song.mp3, video sin música de fondo")
        
        # Exportar video
        print(f"\n   💾 Exportando video a: {output_path}")
        video_final.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='medium'
        )
        
        print(f"\n✅ Video generado exitosamente: {output_path}")
        print(f"   📊 Duración total: {duracion_total:.2f} segundos ({duracion_total/60:.1f} minutos)")
        print(f"   🎬 Escenas procesadas: {len(clips_escenas)}/{len(escenas)}")
        
        return str(output_path)
    
    def _get_background_sound(self, imagen_descripcion: str) -> str | None:
        """
        Busca el archivo de sonido de fondo apropiado según la descripción de la imagen/escena.
        
        Args:
            imagen_descripcion: Descripción de la imagen (escenario) del guion
            
        Returns:
            Ruta al archivo de audio o None si no se encuentra
        """
        # Mapeo de palabras clave de ESCENARIOS a archivos de sonido disponibles
        # Basado en los archivos en assets/background_sounds/
        mapeo_escenarios = {
            # Parque
            "parque": "park.mp3",
            "park": "park.mp3",
            "columpio": "park.mp3",
            "plaza": "park.mp3",
            
            # Bosque/Naturaleza
            "bosque": "forest.mp3",
            "forest": "forest.mp3",
            "árbol": "forest.mp3",
            "árboles": "forest.mp3",
            "naturaleza": "forest.mp3",
            
            # Hospital
            "hospital": "hospital.mp3",
            "médico": "hospital.mp3",
            "doctor": "hospital.mp3",
            "clínica": "hospital.mp3",
            
            # Escuela/Colegio
            "escuela": "school.mp3",
            "school": "school.mp3",
            "colegio": "school.mp3",
            "clase": "school.mp3",
            "aula": "school.mp3",
            "salón": "school.mp3",
            
            # Calle
            "calle": "street.mp3",
            "street": "street.mp3",
            "ciudad": "street.mp3",
            "vereda": "street.mp3",
            "acera": "street.mp3",
        }
        
        if not imagen_descripcion:
            return None
        
        descripcion_lower = imagen_descripcion.lower()
        
        # Buscar coincidencia con las palabras clave de escenarios
        for keyword, filename in mapeo_escenarios.items():
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
