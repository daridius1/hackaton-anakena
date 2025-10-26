"""
Vistas de la aplicación web de cuentos infantiles
Integra con los pipelines existentes sin modificarlos
"""

import json
import uuid
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Importar los pipelines existentes (sin modificar tu código)
from pipelines import Pipeline1Guion, Pipeline2Audio, Pipeline3Imagen, Pipeline4Video

# Importar el agente educativo
from agents import EduAgent
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
    
    # Generar sugerencias personalizadas si el usuario está logueado (OPCIONAL - comentado)
    # sugerencias = []
    # if request.user.is_authenticated and hasattr(request.user, 'perfil'):
    #     agent = EduAgent(request.user.perfil)
    #     sugerencias = agent.obtener_sugerencias(n=5)
    #     
    #     # Registrar que se mostraron estas sugerencias
    #     for sug in sugerencias:
    #         agent.registrar_interaccion(
    #             moraleja=sug['moraleja'],
    #             razon=sug['razon'],
    #             valores=sug['valores'],
    #             seleccionada=False
    #         )
    # else:
    #     # Sugerencias genéricas para usuarios no logueados
    #     agent = EduAgent()
    #     sugerencias = agent.obtener_sugerencias(n=5)
    
    sugerencias = []  # Deshabilitado temporalmente
    
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
        'ejemplos': ejemplos,
        'sugerencias': sugerencias
    })


@csrf_exempt
def generar_video(request):
    """Genera un video usando los pipelines existentes"""
    
    if request.method != 'POST':
        return redirect('webapp:index')
    
    moraleja = request.POST.get('moraleja', '').strip()
    
    if not moraleja:
        return redirect('webapp:index')
    
    # 🆕 VALIDACIÓN ÉTICA con el agente (OPCIONAL - comentado por ahora)
    # agent = EduAgent(request.user.perfil if request.user.is_authenticated and hasattr(request.user, 'perfil') else None)
    # validacion = agent.validar_moraleja(moraleja)
    # 
    # if not validacion.get('es_valida', False):
    #     return render(request, 'error.html', {
    #         'error_title': 'Contenido No Apropiado',
    #         'error_message': validacion.get('razon', 'Esta moraleja no es apropiada para contenido infantil.'),
    #         'error_type': 'filtro_etico',
    #         'valores_detectados': validacion.get('valores_detectados', []),
    #         'nivel': validacion.get('nivel_apropiado', 'rechazado')
    #     })
    
    # Registrar que el usuario seleccionó esta moraleja (OPCIONAL - comentado)
    # if request.user.is_authenticated and hasattr(request.user, 'perfil'):
    #     agent.marcar_video_generado(moraleja)
    
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
        # 🆕 Obtener perfil del usuario si está logueado
        perfil = None
        if request.user.is_authenticated and hasattr(request.user, 'perfil'):
            perfil = request.user.perfil
        
        # PIPELINE 1: Guion (con personalización)
        PROGRESS_STORAGE[task_id].update({'step': 'Generando guion personalizado...', 'progress': 20})
        pipeline1 = Pipeline1Guion(perfil_usuario=perfil)  # 🆕 Pasar perfil
        guion_path = f"guion_{task_id}.json"
        guion = pipeline1.generar(moraleja, output_path=guion_path)
        
        # PIPELINE 2: Audio ✅ HABILITADO
        PROGRESS_STORAGE[task_id].update({'step': 'Generando voces...', 'progress': 30})
        pipeline2 = Pipeline2Audio()
        audio_files = pipeline2.generar(guion_path=guion_path)
        
        # PIPELINE 3: Imágenes ✅ IMPLEMENTADO
        PROGRESS_STORAGE[task_id].update({'step': 'Generando imágenes con Gemini...', 'progress': 50})
        pipeline3 = Pipeline3Imagen()
        image_files = pipeline3.generar(guion_path=guion_path)
        
        # PIPELINE 4: Video ✅ HABILITADO
        PROGRESS_STORAGE[task_id].update({'step': 'Ensamblando video...', 'progress': 90})
        pipeline4 = Pipeline4Video()
        video_path = pipeline4.generar(guion_path=guion_path, output_name=f"{video_id}.mp4")        # Completado
        PROGRESS_STORAGE[task_id].update({
            'step': 'Completado - Video generado',
            'progress': 100,
            'status': 'completed',
            'guion_path': guion_path,
            'image_files': image_files,
            'audio_files': audio_files,
            'video_path': video_path
        })
        
        # Guardar metadata del video
        metadata = {
            'moraleja': moraleja,
            'titulo': guion.get('guion', {}).get('metadata', {}).get('titulo', 'Sin título'),
            'duracion': guion.get('guion', {}).get('metadata', {}).get('duracion_estimada', 'N/A'),
            'num_escenas': len(guion.get('guion', {}).get('escenas', [])),
            'imagenes_generadas': len(image_files),
            'audios_generados': len(audio_files),
            'video_generado': True,
            'video_path': str(video_path)
        }
        
        metadata_path = settings.MEDIA_ROOT / f"{video_id}_metadata.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
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
    """Muestra las imágenes y guion generados"""
    
    metadata_path = settings.MEDIA_ROOT / f"{video_id}_metadata.json"
    
    if not metadata_path.exists():
        return render(request, 'error.html', {
            'error': 'Contenido no encontrado. Puede que aún se esté generando.'
        })
    
    # Cargar metadata
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Buscar imágenes generadas
    imagenes_dir = Path('assets/images')
    imagenes = []
    if imagenes_dir.exists():
        for img in sorted(imagenes_dir.glob('image_*.png')):
            imagenes.append({
                'path': str(img),
                'nombre': img.name
            })
    
    # Verificar si existe el video
    tiene_video = metadata.get('video_generado', False)
    video_url = f"/media/{video_id}.mp4" if tiene_video else None
    
    return render(request, 'result.html', {
        'video_id': video_id,
        'metadata': metadata,
        'imagenes': imagenes,
        'tiene_video': tiene_video,
        'video_url': video_url
    })


def progreso_api(request, task_id):
    """API para consultar el progreso de una tarea"""
    
    progress = PROGRESS_STORAGE.get(task_id, {
        'step': 'Desconocido',
        'progress': 0,
        'status': 'not_found'
    })
    
    return JsonResponse(progress)
