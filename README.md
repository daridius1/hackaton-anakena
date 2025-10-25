# Generador de Cuentos Infantiles Educativos 🎨🎵🖼️🎬

Sistema de 4 pipelines + interfaz web para crear videos educativos infantiles automáticamente a partir de una moraleja.

**🚀 Demo para Hackaton: Aplicación Web Django completa**

## 🎯 Objetivo

Generar videos educativos completos (imagen + voz + sonido) para niños de 5-8 años, partiendo solo de una moraleja o lección moral.

## 🌐 Interfaz Web (NUEVO)

### Inicio Rápido - Demo Web

```bash
# 1. Activar entorno
source .venv/bin/activate

# 2. Iniciar servidor Django
python manage.py runserver

# 3. Abrir en navegador
http://localhost:8000
```

### Funcionalidades de la Web

- ✅ **Página principal** con input de moraleja
- ✅ **4 cards de videos de ejemplo** (con emojis ilustrativos)
- ✅ **Generación en tiempo real** (muestra progreso de pipelines)
- ✅ **Video player integrado** (HTML5 con controles)
- ✅ **Descarga de videos** generados
- ✅ **UI moderna** con TailwindCSS
- ✅ **Sin base de datos** (solo filesystem)

### Flujo de Usuario

```
Usuario → Escribe moraleja → Click "Generar Video"
   ↓
Pipeline 1 → Guion JSON
   ↓
Pipeline 2 → Voces MP3 (placeholder)
   ↓  
Pipeline 3 → Imágenes PNG (placeholder)
   ↓
Pipeline 4 → Video MP4 final
   ↓
Página de resultados → Ver/Descargar video
```

## 📋 Flujo de Pipelines

```
Input: "no hablar con extraños"
   ↓
Pipeline 1 (Guion) → guion.json
   ↓
Pipeline 2 (Audio) → dialogue_1.mp3 ... dialogue_8.mp3
   ↓
Pipeline 3 (Imagen) → image_1.png ... image_8.png
   ↓
Pipeline 4 (Video) → cuento_final.mp4
```

### Pipeline 1: Generador de Guion ✅ IMPLEMENTADO
- **Input:** Moraleja (texto)
- **Proceso:** API de Deepseek genera historia estructurada
- **Output:** `guion.json` con metadata, personajes y escenas
- **Personajes fijos:** Lucas, Sofia, Abuelo Sabio
- **Escenas:** 5-8 escenas con diálogos y descripciones visuales

### Pipeline 2: Generador de Audio 🚧 PLACEHOLDER
- **Input:** `guion.json`
- **Proceso:** API de TTS (Text-to-Speech) convierte diálogos a voz
- **Output:** `assets/voices/dialogue_N.mp3` (uno por escena)
- **TODO:** Implementar integración con OpenAI TTS, ElevenLabs, o similar

### Pipeline 3: Generador de Imágenes 🚧 PLACEHOLDER
- **Input:** `guion.json`
- **Proceso:** API de generación de imágenes crea ilustraciones
- **Output:** `assets/images/image_N.png` (una por escena)
- **TODO:** Implementar integración con DALL-E, Stable Diffusion, o similar

### Pipeline 4: Ensamblador de Video 🚧 PLACEHOLDER
- **Input:** guion.json + todos los assets
- **Proceso:** MoviePy combina imagen + audio + sonidos de fondo
- **Output:** `assets/outputs/cuento_final.mp4`
- **TODO:** Instalar moviepy y descomentar código

## 🚀 Instalación

### 1. Clonar y configurar entorno

```bash
cd /home/sasha/hackaton
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar credenciales

```bash
cp .env.example .env
# Editar .env y añadir tu DEEPSEEK_API_KEY
```

**⚠️ IMPORTANTE:** NUNCA subas tu `.env` a git. El `.gitignore` ya lo protege.

### 3. Obtener API key de Deepseek

1. Regístrate en https://platform.deepseek.com/
2. Genera una API key
3. Agrégala a `.env`:

```env
DEEPSEEK_API_KEY=sk-tu-key-aqui
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_TIMEOUT=60
```

## 💻 Uso

### Modo básico (solo guion)

```bash
source .venv/bin/activate
python main.py "no hablar con extraños" --guion-only
```

### Flujo completo (4 pipelines)

```bash
python main.py "compartir es importante"
```

### Opciones avanzadas

```bash
# Especificar nombre de video
python main.py "ser honesto" --output mi_cuento.mp4

# Saltar pipelines no implementados
python main.py "ayudar a los demás" --skip-audio --skip-imagen --skip-video

# Solo generar guion
python main.py "respetar a los mayores" --guion-only
```

### Ejecutar pipelines individuales

```bash
# Pipeline 1: Solo guion
python pipelines/pipeline_guion.py "cuidar el medio ambiente"

# Pipeline 2: Solo audio (requiere guion.json existente)
python pipelines/pipeline_audio.py --guion guion.json

# Pipeline 3: Solo imágenes (requiere guion.json existente)
python pipelines/pipeline_imagen.py --guion guion.json

# Pipeline 4: Solo video (requiere todos los assets)
python pipelines/pipeline_video.py --guion guion.json --output final.mp4
```

## 📁 Estructura del Proyecto

```
/hackaton
├── main.py                      # Orquestador principal
├── guion.json                   # Guion generado (Pipeline 1)
├── .env                         # Credenciales (NO versionar)
├── .env.example                 # Template de credenciales
├── requirements.txt             # Dependencias Python
├── README.md                    # Esta documentación
│
├── pipelines/                   # Módulos de pipelines
│   ├── __init__.py
│   ├── pipeline_guion.py        # Pipeline 1 ✅
│   ├── pipeline_audio.py        # Pipeline 2 🚧
│   ├── pipeline_imagen.py       # Pipeline 3 🚧
│   └── pipeline_video.py        # Pipeline 4 🚧
│
├── assets/                      # Assets generados
│   ├── voices/                  # MP3 de diálogos (Pipeline 2)
│   │   └── dialogue_N.mp3
│   ├── images/                  # PNG de escenas (Pipeline 3)
│   │   └── image_N.png
│   ├── background_sounds/       # Sonidos ambientales (manual)
│   │   └── pajaros.mp3
│   └── outputs/                 # Videos finales (Pipeline 4)
│       └── cuento_final.mp4
│
├── deepseek_client.py           # [DEPRECADO] Usar pipelines/
└── generate_guion.py            # [DEPRECADO] Usar main.py
```

## 🔧 Para Desarrolladores (Tus Colegas)

### Implementar Pipeline 2 (Audio)

Editar `pipelines/pipeline_audio.py`:

1. Elegir API de TTS (OpenAI, ElevenLabs, Google Cloud, Azure)
2. Descomentar sección TODO
3. Implementar `_call_tts_api(texto, personaje, emocion)`
4. Mapear personajes a voces específicas
5. Guardar MP3 en `assets/voices/`

### Implementar Pipeline 3 (Imágenes)

Editar `pipelines/pipeline_imagen.py`:

1. Elegir API de imágenes (DALL-E, Stable Diffusion, Midjourney)
2. Descomentar sección TODO
3. Construir prompts optimizados con `_build_image_prompt()`
4. Llamar API y guardar PNG en `assets/images/`
5. Considerar estilo consistente (ilustración infantil)

### Implementar Pipeline 4 (Video)

Editar `pipelines/pipeline_video.py`:

1. Instalar MoviePy: `pip install moviepy`
2. Descomentar código de ensamblaje
3. Ajustar FPS, resolución, códecs según necesidad
4. Implementar transiciones entre escenas
5. Mezclar audio de diálogo + fondo

## 🎨 Formato del Guion (guion.json)

```json
{
  "guion": {
    "metadata": {
      "titulo": "El Secreto del Parque Seguro",
      "leccion": "No hablar con extraños",
      "duracion_estimada": "8 minutos",
      "personajes": [...]
    },
    "escenas": [
      {
        "numero_escena": 1,
        "sonido_fondo": "Pájaros cantando",
        "imagen_descripcion": "Lucas y Sofia jugando en el parque...",
        "dialogo": {
          "personaje": "Lucas",
          "texto": "¡Qué divertido es jugar!",
          "emocion": "Feliz"
        }
      }
    ]
  }
}
```

## 🐛 Solución de Problemas

### Error: "DEEPSEEK_API_KEY no está configurada"
- Verifica que `.env` existe y contiene `DEEPSEEK_API_KEY=sk-...`
- Ejecuta `source .venv/bin/activate` antes de correr scripts

### Error: "Authentication Fails"
- Tu API key es inválida o expiró
- Genera una nueva en https://platform.deepseek.com/

### Error: "Import ... could not be resolved"
- Activa el virtualenv: `source .venv/bin/activate`
- Instala dependencias: `pip install -r requirements.txt`

## 📝 Notas de Seguridad

- ❌ **NUNCA** hagas commit de `.env` con credenciales reales
- ✅ `.gitignore` ya protege `.env`, `.venv/` y `__pycache__/`
- ✅ Si expusiste una key por error, revócala inmediatamente en Deepseek
- ✅ Usa `.env.example` como template seguro

## 🤝 Contribución

Este proyecto es para el hackathon. Para trabajar en equipo:

1. **Pipeline 1 (Guion):** Ya implementado ✅
2. **Pipeline 2 (Audio):** Asignado a [nombre del colega]
3. **Pipeline 3 (Imagen):** Asignado a [nombre del colega]
4. **Pipeline 4 (Video):** Por asignar

Usa git para versionar tus cambios:

```bash
git add pipelines/pipeline_audio.py
git commit -m "Implementar Pipeline 2 con OpenAI TTS"
```

---

**Autor:** Sasha  
**Hackathon:** Generador de Cuentos Infantiles  
**Fecha:** Octubre 2025
