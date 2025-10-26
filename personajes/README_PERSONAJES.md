# 👥 Personajes del Proyecto

## Personajes Principales (5 personajes fijos)

### 1. Lucas
- **Edad**: 7 años
- **Características físicas**: 
  - Cabello castaño corto
  - Sonrisa brillante con dientes blancos
  - Usa camisa azul
  - Ojos grandes y expresivos color café
  - Estatura promedio para su edad
- **Personalidad**: Alegre, responsable, buen ejemplo para otros niños
- **Tipo de voz**: Voz infantil alegre y clara
- **Archivo de referencia**: `personajes/lucas/lucas_referencia.png`

### 2. Sofia
- **Edad**: 7 años
- **Características físicas**:
  - Cabello rizado castaño oscuro, largo hasta los hombros
  - Vestido rosa
  - Ojos grandes color café oscuro
  - Tez morena clara
  - Expresión curiosa
- **Personalidad**: Curiosa, entusiasta por aprender, hace muchas preguntas
- **Tipo de voz**: Voz infantil curiosa y dulce
- **Archivo de referencia**: `personajes/sofia/sofia_referencia.png`

### 3. Dr. Muelitas
- **Edad**: 40 años
- **Características físicas**:
  - Cabello negro con algunas canas en las sienes
  - Bigote bien cuidado
  - Bata blanca de dentista
  - Gafas redondas
  - Sonrisa amplia y amable
  - Estatura alta
- **Personalidad**: Amable, paciente, educador nato
- **Tipo de voz**: Voz adulta cálida y amable
- **Archivo de referencia**: `personajes/dr_muelitas/dr_muelitas_referencia.png`

### 4. [Personaje 4 - Por definir]
- **Edad**: 
- **Características físicas**:
- **Personalidad**: 
- **Tipo de voz**: 
- **Archivo de referencia**: `personajes/personaje4/personaje4_referencia.png`

### 5. [Personaje 5 - Por definir]
- **Edad**: 
- **Características físicas**:
- **Personalidad**: 
- **Tipo de voz**: 
- **Archivo de referencia**: `personajes/personaje5/personaje5_referencia.png`

---

## 📁 Estructura de Carpetas

```
personajes/
├── lucas/
│   ├── lucas_referencia.png          # Imagen oficial de referencia
│   └── lucas_descripcion.txt          # Descripción detallada en texto
├── sofia/
│   ├── sofia_referencia.png
│   └── sofia_descripcion.txt
├── dr_muelitas/
│   ├── dr_muelitas_referencia.png
│   └── dr_muelitas_descripcion.txt
├── personaje4/
│   └── ...
└── personaje5/
    └── ...
```

---

## 🎯 Uso en los Scripts

Los scripts de generación de cuentos SIEMPRE usarán estas imágenes de referencia para mantener coherencia visual en TODOS los cuentos.

### Ejemplo de uso:
```python
# Cargar referencia de Lucas
imagen_lucas = "personajes/lucas/lucas_referencia.png"

# Generar nueva escena con Lucas
generar_imagen(descripcion="Lucas jugando en el parque", 
               imagen_referencia=imagen_lucas)
```

---

## ✅ Ventajas de este Sistema

1. **Coherencia total**: Los personajes se ven IGUALES en todos los cuentos
2. **Reutilizable**: No hay que redefinir personajes cada vez
3. **Escalable**: Fácil agregar más personajes
4. **Mantenible**: Si quieres cambiar un personaje, solo cambias su referencia
5. **Doble backup**: Imagen + texto descriptivo por si la imagen falla

---

## 📝 Notas Importantes

- Las imágenes de referencia deben ser **PNG de alta calidad**
- Mantener el mismo **estilo de ilustración** en todos los personajes
- Los archivos `.txt` contienen la descripción exacta por si se necesita regenerar
- **NUNCA** modificar las imágenes de referencia una vez establecidas
