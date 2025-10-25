"""
Pipelines para generación de cuentos infantiles

Pipeline 1: Guion (texto) - deepseek_client.py -> guion.json
Pipeline 2: Audio (voces) - TTS API -> dialogue_N.mp3
Pipeline 3: Imagen (visual) - Image API -> image_N.png
Pipeline 4: Video (ensamblaje) - MoviePy -> cuento_final.mp4
"""

from .pipeline_guion import Pipeline1Guion
from .pipeline_audio import Pipeline2Audio
from .pipeline_imagen import Pipeline3Imagen
from .pipeline_video import Pipeline4Video

__all__ = [
    "Pipeline1Guion",
    "Pipeline2Audio",
    "Pipeline3Imagen",
    "Pipeline4Video",
]
