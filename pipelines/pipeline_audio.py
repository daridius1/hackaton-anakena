"""
Pipeline 2: Generador de Audio (Voces)
Genera archivos MP3 con las voces de los diálogos de cada escena usando ElevenLabs.

Input: guion.json
Output: assets/voices/dialogue_N.mp3 (uno por cada escena)
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()


class Pipeline2Audio:
    """Pipeline 2: Generador de audio para diálogos usando ElevenLabs"""
    
    def __init__(self, output_dir: str = "assets/voices", config_path: str = "config/voices.json"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        
        # Load voice configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def generar(self, guion_path: str = "guion.json") -> List[str]:
        """
        Genera archivos de audio MP3 para cada diálogo del guion.
        
        Args:
            guion_path: Ruta al archivo guion.json generado por Pipeline 1
            
        Returns:
            Lista de rutas a los archivos de audio generados
        """
        print(f"🎵 PIPELINE 2: Generando audio desde: {guion_path}...")
        
        # Leer guion
        with open(guion_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        guion = data.get("guion", {})
        escenas = guion.get("escenas", [])
        
        archivos_generados = []
        
        for escena in escenas:
            num_escena = escena.get("numero_escena")
            dialogo = escena.get("dialogo", {})
            personaje = dialogo.get("personaje")
            texto = dialogo.get("texto")
            emocion = dialogo.get("emocion")
            
            print(f"   Escena {num_escena}: {personaje} dice '{texto[:50]}...'")
            
            # Generate audio for this dialogue
            try:
                output_file = self._generate_audio_for_dialogue(
                    personaje, texto, emocion, num_escena
                )
                archivos_generados.append(str(output_file))
                print(f"   ✅ Audio generado: {output_file.name}")
            except Exception as e:
                print(f"   ❌ Error generando audio para escena {num_escena}: {str(e)}")
                # Create placeholder file to continue pipeline
                output_file = self.output_dir / f"dialogue_{num_escena}.mp3"
                output_file.touch()
                archivos_generados.append(str(output_file))
        
        print(f"✅ {len(archivos_generados)} archivos de audio generados en: {self.output_dir}")
        
        return archivos_generados
    
    def _generate_audio_for_dialogue(self, personaje: str, texto: str, emocion: str, num_escena: int) -> Path:
        """
        Genera audio para un diálogo específico usando ElevenLabs.
        
        Args:
            personaje: Nombre del personaje
            texto: Texto del diálogo
            emocion: Emoción del personaje
            num_escena: Número de escena
            
        Returns:
            Path al archivo de audio generado
        """
        # Get voice configuration for character
        if personaje not in self.config["characters"]:
            raise ValueError(f"Personaje '{personaje}' no encontrado en la configuración de voces")
        voice_config = self.config["characters"][personaje]
        default_settings = self.config["default_settings"]
        
        # Add emotion tag if present
        if emocion:
            texto = f"[{emocion}] {texto}"
        
        # Generate audio using ElevenLabs
        audio = self.client.text_to_speech.convert(
            text=texto,
            voice_id=voice_config["voice_id"],
            model_id=default_settings["model"],
            output_format=default_settings["output_format"],
            voice_settings={
                "speed": default_settings["speed"],
                "language": "es",
                "accent": "standard"
            }
        )
        
        # Save audio file
        output_file = self.output_dir / f"dialogue_{num_escena}.mp3"
        with open(output_file, "wb") as f:
            f.write(b"".join(audio))
        
        return output_file


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline 2: Generar audio de diálogos")
    parser.add_argument("--guion", "-g", default="guion.json", help="Archivo guion.json")
    parser.add_argument("--output-dir", "-o", default="assets/voices", help="Directorio de salida")
    args = parser.parse_args()
    
    pipeline = Pipeline2Audio(output_dir=args.output_dir)
    pipeline.generar(guion_path=args.guion)
