"""
Vistas de la aplicación web de cuentos infantiles
Integra con los pipelines existentes sin modificarlos
"""
import json
import os
import uuid
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Importar los pipelines existentes (sin modificar tu código)
from pipelines import Pipeline1Guion, Pipeline2Audio, Pipeline3Imagen, Pipeline4Video


# Almacenamiento temporal del progreso (en producción usar Redis/DB)
PROGRESS_STORAGE = {}


def index(request):
    """Página principal con input y ejemplos de videos"""
    
    # Videos de ejemplo pre-generados
    ejemplos = [
        {
            'id': 'compartir',
            'titulo': 'La Importancia de Compartir',
            'descripcion': 'Aprende por qué compartir con los demás nos hace felices',
            'thumbnail': 'ejemplos/compartir_thumb.jpg',
            'video': 'ejemplos/ejemplo1.mp4',
            'duracion': '8 min',
        },
        {
            'id': 'extranos',
            'titulo': 'No Hablar con Extraños',
            'descripcion': 'Aprende a estar seguro y protegido',
            'thumbnail': 'ejemplos/extranos_thumb.jpg',
            'video': 'ejemplos/extranos.mp4',
            'duracion': '7 min',
        },
        {
            'id': 'honesto',
            'titulo': 'Ser Honesto Siempre',
            'descripcion': 'La verdad siempre es el mejor camino',
            'thumbnail': 'ejemplos/honesto_thumb.jpg',
            'video': 'ejemplos/honesto.mp4',
            'duracion': '8 min',
        },
        {
            'id': 'ambiente',
            'titulo': 'Cuidar el Medio Ambiente',
            'descripcion': 'Pequeñas acciones para un planeta mejor',
            'thumbnail': 'ejemplos/ambiente_thumb.jpg',
            'video': 'ejemplos/ambiente.mp4',
            'duracion': '9 min',
        },
    ]
    
    return render(request, 'index.html', {
        'ejemplos': ejemplos
    })


@csrf_exempt
def generar_video(request):
    """Genera un video usando los pipelines existentes"""
    
    if request.method != 'POST':
        return redirect('webapp:index')
    
    moraleja = request.POST.get('moraleja', '').strip()
    
    if not moraleja:
        return redirect('webapp:index')
    
    # Generar ID único para esta tarea
    task_id = str(uuid.uuid4())[:8]
    video_id = f"video_{task_id}"
    
    # Inicializar progreso
    PROGRESS_STORAGE[task_id] = {
        'step': 'Iniciando...',
        'progress': 0,
        'video_id': video_id,
        'moraleja': moraleja,
        'status': 'processing'
    }
    
    try:
        # PIPELINE 1: Guion
        PROGRESS_STORAGE[task_id].update({'step': 'Generando guion...', 'progress': 10})
        pipeline1 = Pipeline1Guion()
        guion_path = f"guion_{task_id}.json"
        guion = pipeline1.generar(moraleja, output_path=guion_path)
        
        # PIPELINE 2: Audio (placeholder por ahora)
        PROGRESS_STORAGE[task_id].update({'step': 'Generando voces...', 'progress': 30})
        pipeline2 = Pipeline2Audio()
        audio_files = pipeline2.generar(guion_path=guion_path)
        
        # PIPELINE 3: Imágenes (placeholder por ahora)
        PROGRESS_STORAGE[task_id].update({'step': 'Generando imágenes...', 'progress': 60})
        pipeline3 = Pipeline3Imagen()
        image_files = pipeline3.generar(guion_path=guion_path)
        
        # PIPELINE 4: Video
        PROGRESS_STORAGE[task_id].update({'step': 'Ensamblando video...', 'progress': 90})
        pipeline4 = Pipeline4Video()
        video_path = pipeline4.generar(guion_path=guion_path, output_name=f"{video_id}.mp4")
        
        # Completado
        PROGRESS_STORAGE[task_id].update({
            'step': 'Completado',
            'progress': 100,
            'status': 'completed',
            'video_path': video_path
        })
        
        # Guardar metadata del video
        metadata = {
            'moraleja': moraleja,
            'titulo': guion.get('guion', {}).get('metadata', {}).get('titulo', 'Sin título'),
            'duracion': guion.get('guion', {}).get('metadata', {}).get('duracion_estimada', 'N/A'),
            'num_escenas': len(guion.get('guion', {}).get('escenas', [])),
        }
        
        metadata_path = settings.MEDIA_ROOT / f"{video_id}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
    except Exception as e:
        PROGRESS_STORAGE[task_id].update({
            'step': 'Error',
            'progress': 0,
            'status': 'error',
            'error': str(e)
        })
        return render(request, 'error.html', {'error': str(e)})
    
    return redirect('webapp:resultado', video_id=video_id)


def resultado(request, video_id):
    """Muestra el video generado"""
    
    video_path = settings.MEDIA_ROOT / f"{video_id}.mp4"
    metadata_path = settings.MEDIA_ROOT / f"{video_id}_metadata.json"
    
    if not video_path.exists():
        return render(request, 'error.html', {
            'error': 'Video no encontrado. Puede que aún se esté generando.'
        })
    
    # Cargar metadata si existe
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    return render(request, 'result.html', {
        'video_id': video_id,
        'video_url': f'/media/{video_id}.mp4',
        'metadata': metadata
    })


def progreso_api(request, task_id):
    """API para consultar el progreso de una tarea"""
    
    progress = PROGRESS_STORAGE.get(task_id, {
        'step': 'Desconocido',
        'progress': 0,
        'status': 'not_found'
    })
    
    return JsonResponse(progress)
