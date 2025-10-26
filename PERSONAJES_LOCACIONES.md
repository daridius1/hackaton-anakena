# 📋 PERSONAJES Y LOCACIONES - CONFIGURACIÓN ACTUALIZADA

## 👥 PERSONAJES (6 disponibles)

### Niños (2)
1. **Sofia** - Niña 7 años
   - Cabello rizado castaño oscuro hasta los hombros
   - Vestido rosa
   - Tez morena clara
   - Personalidad: curiosa, entusiasta por aprender

2. **Lucas** - Niño 7 años
   - Cabello castaño corto liso
   - Camisa azul celeste
   - Tez clara
   - Personalidad: alegre, responsable, buen ejemplo

### Adultos (3)
3. **Matilda** - Adulta 35 años
   - Cabello castaño largo lacio
   - Blusa celeste
   - Tez clara
   - Personalidad: cariñosa, responsable, protectora

4. **Carlos** - Adulto 40 años
   - Cabello negro corto
   - Camisa blanca/polo
   - Tez morena
   - Personalidad: responsable, trabajador, paternal

5. **Doctora Martina** - Doctora 45 años
   - Cabello castaño recogido (mechas grises)
   - Bata blanca, estetoscopio, gafas rectangulares
   - Tez clara
   - Personalidad: inteligente, empática, profesional

### Adultos Mayores (1)
6. **Don Juan** - Adulto mayor 70 años
   - Cabello blanco corto
   - Suéter marrón
   - Tez clara con arrugas
   - Personalidad: sabio, paciente, cariñoso

---

## 🏞️ LOCACIONES (6 disponibles)

### 1. **Bosque**
- Árboles altos, hojas verdes
- Rayos de sol filtrándose
- Helechos, flores silvestres
- Camino de tierra
- Ambiente mágico y acogedor

### 2. **Hospital**
- Paredes celestes/verde menta
- Camilla blanca
- Equipo médico básico
- Pósters educativos
- Ambiente limpio y tranquilizador

### 3. **Plaza**
- Árboles grandes
- Bancas verdes
- Flores en maceteros
- Pasto verde brillante
- Caminos de baldosas
- Ambiente familiar

### 4. **Calle**
- Casas coloridas
- Veredas amplias
- Árboles en aceras
- Faroles, letreros de tiendas
- Ambiente urbano seguro

### 5. **Habitación**
- Cama con edredón colorido
- Ventana con cortinas
- Estantes con libros/juguetes
- Alfombra suave
- Pósters en paredes
- Ambiente cálido

### 6. **Sala de Clases**
- Pizarra blanca/verde
- Escritorios de colores
- Estantes con materiales
- Ventanas grandes
- Pósters educativos
- Mapas, números, letras

---

## 🔧 ARCHIVOS ACTUALIZADOS

```
✅ personajes_config.py           - Diccionario centralizado
✅ pipeline_guion.py              - Prompt con nuevos personajes/locaciones
✅ pipeline_imagen.py             - Personajes actualizados
✅ gestor_escenarios.py           - Locaciones actualizadas
✅ generar_imagen_con_gemini.py   - CLI actualizado
```

---

## 📝 PALABRAS CLAVE DE DETECCIÓN

### Personajes:
- `sofia` / `sofía`
- `lucas`
- `matilda`
- `carlos`
- `don_juan` / `don juan` / `juan`
- `doctora_martina` / `doctora` / `dra` / `martina`

### Locaciones:
- `bosque` / `árboles` / `naturaleza` / `selva`
- `hospital` / `clínica` / `consultorio médico`
- `plaza` / `parque` / `área pública`
- `calle` / `avenida` / `vereda` / `ciudad`
- `habitacion` / `dormitorio` / `cuarto` / `pieza`
- `sala_de_clases` / `aula` / `salón` / `escuela`

---

## 🎯 EJEMPLO DE USO

### Usuario ingresa moraleja:
```
"la importancia de cuidar la salud"
```

### DeepSeek genera:
```json
{
  "escenas": [
    {
      "numero_escena": 1,
      "imagen_descripcion": "Sofia y Doctora Martina en un hospital moderno...",
      "dialogo": {"personaje": "Sofia", "texto": "Doctora, me duele la garganta"}
    },
    {
      "numero_escena": 2,
      "imagen_descripcion": "Sofia y Doctora Martina en el mismo hospital...",
      "dialogo": {"personaje": "Doctora Martina", "texto": "Vamos a revisarte..."}
    }
  ]
}
```

### Sistema detecta:
```
Personajes: Sofia, Doctora Martina
Locaciones: hospital (escenas 1, 2)
```

### Sistema genera:
```
Escena 1: [sofia_ref] + [doctora_martina_ref] + [hospital_background] → imagen_1.png
Escena 2: [sofia_ref] + [doctora_martina_ref] + [hospital_background] → imagen_2.png
                                                      ↑
                                             MISMO HOSPITAL!
```

---

## ⚠️ PRÓXIMOS PASOS

1. **Crear imágenes de referencia** para los nuevos personajes:
   - `personajes/matilda/matilda_referencia.png`
   - `personajes/carlos/carlos_referencia.png`
   - `personajes/don_juan/don_juan_referencia.png`
   - `personajes/doctora_martina/doctora_martina_referencia.png`

2. **Probar el sistema** con una moraleja que use los nuevos personajes

3. **Verificar** que se generen las locaciones automáticamente

---

## 💡 NOTAS

- Los personajes anteriores (Dr. Muelitas, Abuelo Sabio) fueron reemplazados
- Don Juan reemplaza al Abuelo Sabio (mismo concepto, nuevo nombre)
- Doctora Martina reemplaza al Dr. Muelitas (concepto similar)
- Las locaciones son más específicas y adaptadas al contexto chileno
- El sistema sigue manteniendo coherencia visual total
