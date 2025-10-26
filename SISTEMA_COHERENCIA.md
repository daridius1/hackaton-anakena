# 🎯 SISTEMA DE COHERENCIA VISUAL - RESUMEN

## 📋 ¿Cómo funciona?

### Flujo completo:

```
1. USUARIO ingresa moraleja
   ↓
   "la importancia de compartir"

2. DEEPSEEK genera historia
   ↓
   {
     "escenas": [
       {
         "numero_escena": 1,
         "imagen_descripcion": "Sofia y Lucas en un parque con árboles...",
         "dialogo": {"personaje": "Sofia", ...}
       },
       {
         "numero_escena": 2,
         "imagen_descripcion": "Sofia y Lucas en el mismo parque...",
         "dialogo": {"personaje": "Lucas", ...}
       },
       ...
     ]
   }

3. SISTEMA DETECTA AUTOMÁTICAMENTE
   ↓
   Personajes: [Sofia, Lucas]
   Escenarios: [parque] en escenas [1, 2, 3]

4. GESTOR DE ESCENARIOS
   ↓
   ¿Existe "parque" en DB?
   → SÍ: Reutiliza imagen existente
   → NO: Genera nuevo background sin personajes

5. PIPELINE DE IMAGEN genera cada escena
   ↓
   Escena 1: [ref_sofia] + [ref_lucas] + [ref_parque] → Imagen 1
   Escena 2: [ref_sofia] + [ref_lucas] + [ref_parque] → Imagen 2
   Escena 3: [ref_sofia] + [ref_lucas] + [ref_parque] → Imagen 3
                              ↑
                   MISMO PARQUE EN TODAS!

6. RESULTADO
   ↓
   ✅ Personajes consistentes (misma ropa, rasgos)
   ✅ Escenario consistente (mismo parque visual)
   ✅ Coherencia total en el cuento
```

---

## 🔧 Componentes del Sistema

### 1. **Diccionario de Personajes** (`PERSONAJES`)
- Definiciones físicas EXACTAS de cada personaje
- Sofia, Lucas, Dr. Muelitas, Abuelo Sabio
- Incluye: edad, descripción detallada, ruta de referencia

### 2. **Gestor de Escenarios** (`gestor_escenarios.py`)
- Detecta escenarios mencionados (parque, bosque, playa, etc.)
- Mantiene base de datos JSON de escenarios generados
- Reutiliza escenarios existentes automáticamente
- Genera nuevos backgrounds cuando es necesario

### 3. **Pipeline de Imágenes** (`pipeline_imagen.py`)
- Analiza el guion completo ANTES de generar
- Identifica personajes y escenarios
- Genera/carga referencias necesarias
- Crea cada imagen con referencias múltiples:
  * Referencias de personajes (siempre)
  * Referencia de escenario (si aplica)

### 4. **Prompt Mejorado de DeepSeek** (`pipeline_guion.py`)
- Instruye a DeepSeek para especificar escenarios
- Pide coherencia en descripciones de escenas
- Menciona escenarios comunes predefinidos

---

## 🎨 Ventajas del Sistema

### ✅ Coherencia Visual Total
- Los personajes se ven IGUALES en todas las escenas
- Los escenarios se ven IGUALES cuando se repiten
- No hay inconsistencias visuales

### ✅ Eficiencia
- Escenarios se generan UNA VEZ y se reutilizan
- Base de datos crece con el tiempo
- Menos llamadas a API de generación

### ✅ Consultas Encapsuladas
- Cada generación incluye TODAS las referencias necesarias
- Gemini recibe: descripción + refs_personajes + ref_escenario
- Una sola llamada por escena con contexto completo

### ✅ Automatización Completa
- Detección automática de personajes
- Detección automática de escenarios
- Gestión automática de reutilización
- Usuario solo pone la moraleja

---

## 📊 Ejemplo Real

### Input del usuario:
```
"la importancia de compartir"
```

### DeepSeek genera:
```json
{
  "escenas": [
    {
      "numero_escena": 1,
      "imagen_descripcion": "Sofia y Lucas en un parque con columpios...",
      "dialogo": {"personaje": "Sofia", "texto": "¡Mira cuántos juguetes!"}
    },
    {
      "numero_escena": 2,
      "imagen_descripcion": "Sofia y Lucas en el parque, compartiendo...",
      "dialogo": {"personaje": "Lucas", "texto": "Compartamos juntos"}
    }
  ]
}
```

### Sistema detecta:
```
Personajes: Sofia, Lucas
Escenarios: parque (escenas 1, 2)
```

### Sistema prepara referencias:
```
1. personajes/sofia/sofia_referencia.png (existente)
2. personajes/lucas/lucas_referencia.png (existente)
3. escenarios/parque_background.png (genera o reutiliza)
```

### Generación de imágenes:
```
Escena 1:
  Input a Gemini:
    - Descripción: "Sofia y Lucas en un parque..."
    - Ref 1: sofia_referencia.png
    - Ref 2: lucas_referencia.png
    - Ref 3: parque_background.png
  Output: image_1.png
  
Escena 2:
  Input a Gemini:
    - Descripción: "Sofia y Lucas en el parque..."
    - Ref 1: sofia_referencia.png
    - Ref 2: lucas_referencia.png
    - Ref 3: parque_background.png ← MISMO PARQUE!
  Output: image_2.png
```

### Resultado:
- ✅ Sofia se ve igual en ambas escenas
- ✅ Lucas se ve igual en ambas escenas
- ✅ El parque se ve igual en ambas escenas
- ✅ Coherencia visual perfecta

---

## 🗂️ Archivos Clave

```
hackaton-anakena/
├── pipelines/
│   ├── pipeline_guion.py         # DeepSeek - genera historia
│   ├── pipeline_imagen.py        # Gemini - genera imágenes
│   └── gestor_escenarios.py      # Sistema de escenarios
├── personajes/                    # Referencias de personajes
│   ├── sofia/sofia_referencia.png
│   ├── lucas/lucas_referencia.png
│   ├── dr_muelitas/dr_muelitas_referencia.png
│   └── abuelo_sabio/abuelo_referencia.png
├── escenarios/                    # Base de datos de escenarios
│   ├── escenarios.json           # Metadata
│   ├── parque_background.png     # Escenarios generados
│   ├── bosque_background.png
│   └── ...
└── assets/images/                 # Imágenes finales del cuento
    ├── image_1.png
    ├── image_2.png
    └── ...
```

---

## 🚀 ¿Qué sigue?

1. **Probar el sistema** con una moraleja
2. **Verificar** que se detecten personajes correctamente
3. **Verificar** que se generen/reutilicen escenarios
4. **Ajustar** prompts si es necesario
5. **Expandir** escenarios predefinidos si quieres más tipos

---

## 💡 Tips

- Los escenarios se generan **sin personajes** (solo el lugar)
- Los personajes se **superponen** sobre el escenario
- DeepSeek debe **especificar el escenario** en cada descripción
- El sistema **reutiliza automáticamente** escenarios existentes
- Puedes **pre-generar** escenarios comunes para tener una biblioteca
