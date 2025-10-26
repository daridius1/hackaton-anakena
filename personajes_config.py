""""""

Configuración centralizada de personajes del proyecto.Configuración centralizada de personajes del proyecto.

Este archivo contiene el diccionario FIJO de todos los personajesEste archivo contiene el diccionario FIJO de todos los personajes

con sus características físicas EXACTAS para mantener coherencia visual.con sus características físicas EXACTAS para mantener coherencia visual.



Uso:Uso:

    from personajes_config import PERSONAJES    from personajes_config import PERSONAJES

""""""



# ============================================================================# ============================================================================

# DICCIONARIO FIJO DE PERSONAJES# DICCIONARIO FIJO DE PERSONAJES

# Este diccionario define las características físicas EXACTAS de cada personaje# Este diccionario define las características físicas EXACTAS de cada personaje

# para mantener coherencia visual en TODAS las generaciones# para mantener coherencia visual en TODAS las generaciones

# ============================================================================# ============================================================================



PERSONAJES = {PERSONAJES = {

    "sofia": {    "sofia": {

        "nombre": "Sofia",        "nombre": "Sofia",

        "edad": "7 años",        "edad": "7 años",

        "tipo": "niña",        "tipo": "niña",

        "descripcion_fisica_detallada": """        "descripcion_fisica_detallada": """

            - Niña de 7 años            - Niña de 7 años

            - Cabello: rizado castaño oscuro, largo hasta los hombros            - Cabello: rizado castaño oscuro, largo hasta los hombros

            - Ojos: grandes, color café oscuro            - Ojos: grandes, color café oscuro

            - Ropa: vestido rosa            - Ropa: vestido rosa

            - Piel: tez morena clara            - Piel: tez morena clara

            - Expresión: curiosa, entusiasta            - Expresión: curiosa, entusiasta

            - Estatura: promedio para su edad            - Estatura: promedio para su edad

            - Rasgos: cara ovalada, rizos definidos y voluminosos            - Rasgos: cara ovalada, rizos definidos y voluminosos

        """,        """,

        "descripcion_corta": "niña de 7 años, cabello rizado castaño oscuro hasta los hombros, vestido rosa, ojos grandes café oscuro, tez morena clara, expresión curiosa",        "descripcion_corta": "niña de 7 años, cabello rizado castaño oscuro hasta los hombros, vestido rosa, ojos grandes café oscuro, tez morena clara, expresión curiosa",

        "personalidad": "curiosa, entusiasta por aprender",        "personalidad": "curiosa, entusiasta por aprender",

        "ruta": "personajes/sofia/sofia_referencia.png"        "ruta": "personajes/sofia/sofia_referencia.png"

    },    },

    "lucas": {    "lucas": {

        "nombre": "Lucas",        "nombre": "Lucas",

        "edad": "7 años",        "edad": "7 años",

        "tipo": "niño",        "tipo": "niño",

        "descripcion_fisica_detallada": """        "descripcion_fisica_detallada": """

            - Niño de 7 años            - Niño de 7 años

            - Cabello: castaño corto, liso            - Cabello: castaño corto, liso

            - Ojos: grandes y expresivos, color café            - Ojos: grandes y expresivos, color café

            - Ropa: camisa azul celeste            - Ropa: camisa azul celeste

            - Piel: tez clara            - Piel: tez clara

            - Expresión: sonrisa brillante con dientes blancos            - Expresión: sonrisa brillante con dientes blancos

            - Estatura: promedio para su edad            - Estatura: promedio para su edad

            - Rasgos: cara redondeada, mejillas sonrosadas            - Rasgos: cara redondeada, mejillas sonrosadas

        """,        """,

        "descripcion_corta": "niño de 7 años, cabello castaño corto, camisa azul celeste, sonrisa brillante con dientes blancos, ojos grandes color café",        "descripcion_corta": "niño de 7 años, cabello castaño corto, camisa azul celeste, sonrisa brillante con dientes blancos, ojos grandes color café",

        "personalidad": "alegre, responsable, buen ejemplo",        "personalidad": "alegre, responsable, buen ejemplo",

        "ruta": "personajes/lucas/lucas_referencia.png"        "ruta": "personajes/lucas/lucas_referencia.png"

    },    },

    "carlos": {    "carlos": {

        "nombre": "Carlos",        "nombre": "Carlos",

        "edad": "40 años",        "edad": "40 años",

        "tipo": "adulto",        "tipo": "adulto",

        "descripcion_fisica_detallada": """        "descripcion_fisica_detallada": """

            - Hombre adulto de 40 años            - Hombre adulto de 40 años

            - Cabello: negro corto, bien peinado            - Cabello: negro corto, bien peinado

            - Ojos: color café oscuro, seguros            - Ojos: color café oscuro, seguros

            - Ropa: camisa blanca o polo, pantalón oscuro            - Ropa: camisa blanca o polo, pantalón oscuro

            - Piel: tez morena            - Piel: tez morena

            - Expresión: confiable, seria pero amable            - Expresión: confiable, seria pero amable

            - Estatura: alta            - Estatura: alta

            - Rasgos: cara cuadrada, mandíbula definida, aspecto deportivo            - Rasgos: cara cuadrada, mandíbula definida, aspecto deportivo

        """,        """,

        "descripcion_corta": "hombre adulto de 40 años, cabello negro corto, camisa blanca, ojos café oscuro, tez morena, expresión confiable y amable",        "descripcion_corta": "hombre adulto de 40 años, cabello negro corto, camisa blanca, ojos café oscuro, tez morena, expresión confiable y amable",

        "personalidad": "responsable, trabajador, paternal",        "personalidad": "responsable, trabajador, paternal",

        "ruta": "personajes/carlos/carlos_referencia.png"        "ruta": "personajes/carlos/carlos_referencia.png"

    },    },

    "juan": {    "juan": {

        "nombre": "Juan",    "carlos": {

        "edad": "70 años",        "nombre": "Carlos",

        "tipo": "adulto mayor",        "edad": "40 años",

        "descripcion_fisica_detallada": """        "tipo": "adulto",

            - Adulto mayor de 70 años        "descripcion_fisica_detallada": """

            - Cabello: blanco, corto o con calvicie parcial            - Hombre adulto de 40 años

            - Ojos: color café claro, sabios y cálidos            - Cabello: negro corto, bien peinado

            - Ropa: suéter marrón o camisa a cuadros, pantalón casual            - Ojos: color café oscuro, seguros

            - Piel: tez clara con arrugas de expresión            - Ropa: camisa blanca o polo, pantalón oscuro

            - Expresión: sonrisa sabia, mirada bondadosa            - Piel: tez morena

            - Estatura: mediana, ligeramente encorvado            - Expresión: confiable, seria pero amable

            - Rasgos: cara arrugada con arrugas de sonrisa, aspecto abuelo cariñoso            - Estatura: alta

        """,            - Rasgos: cara cuadrada, mandíbula definida, aspecto deportivo

        "descripcion_corta": "adulto mayor de 70 años, cabello blanco corto, suéter marrón, ojos café claro sabios, arrugas de expresión, aspecto de abuelo bondadoso",        """,

        "personalidad": "sabio, paciente, cariñoso, contador de historias",        "descripcion_corta": "hombre adulto de 40 años, cabello negro corto, camisa blanca, ojos café oscuro, tez morena, expresión confiable y amable",

        "ruta": "personajes/juan/juan_referencia.png"        "personalidad": "responsable, trabajador, paternal",

    },        "ruta": "personajes/carlos/carlos_referencia.png"

    "martina": {    },

        "nombre": "Martina",    "juan": {

        "edad": "45 años",        "nombre": "Juan",

        "tipo": "adulta profesional",        "edad": "70 años",

        "descripcion_fisica_detallada": """        "tipo": "adulto mayor",

            - Mujer adulta de 45 años        "descripcion_fisica_detallada": """

            - Cabello: castaño con mechas grises, recogido en cola o moño profesional            - Adulto mayor de 70 años

            - Ojos: color café, inteligentes y amables            - Cabello: blanco, corto o con calvicie parcial

            - Ropa: bata blanca de doctora, estetoscopio al cuello            - Ojos: color café claro, sabios y cálidos

            - Accesorios: gafas rectangulares modernas            - Ropa: suéter marrón o camisa a cuadros, pantalón casual

            - Piel: tez clara            - Piel: tez clara con arrugas de expresión

            - Expresión: profesional, confiable, sonrisa tranquilizadora            - Expresión: sonrisa sabia, mirada bondadosa

            - Estatura: mediana-alta            - Estatura: mediana, ligeramente encorvado

            - Rasgos: cara ovalada, aspecto competente y amigable            - Rasgos: cara arrugada con arrugas de sonrisa, aspecto abuelo cariñoso

        """,        """,

        "descripcion_corta": "doctora de 45 años, cabello castaño recogido, bata blanca, gafas rectangulares, estetoscopio, expresión profesional y amable",        "descripcion_corta": "adulto mayor de 70 años, cabello blanco corto, suéter marrón, ojos café claro sabios, arrugas de expresión, aspecto de abuelo bondadoso",

        "personalidad": "inteligente, empática, profesional, tranquilizadora",        "personalidad": "sabio, paciente, cariñoso, contador de historias",

        "ruta": "personajes/martina/martina_referencia.png"        "ruta": "personajes/juan/juan_referencia.png"

    }    },

}    "martina": {

        "nombre": "Martina",

# Mapeo de IDs alternativos (para compatibilidad)        "edad": "45 años",

ALIAS_PERSONAJES = {        "tipo": "adulta profesional",

    "don_juan": "juan",        "descripcion_fisica_detallada": """

    "don juan": "juan",            - Mujer adulta de 45 años

    "doctora": "martina",            - Cabello: castaño con mechas grises, recogido en cola o moño profesional

    "dra": "martina",            - Ojos: color café, inteligentes y amables

    "dra_martina": "martina",            - Ropa: bata blanca de doctora, estetoscopio al cuello

    "doctora_martina": "martina",            - Accesorios: gafas rectangulares modernas

}            - Piel: tez clara

            - Expresión: profesional, confiable, sonrisa tranquilizadora

def obtener_personaje(nombre_o_id):            - Estatura: mediana-alta

    """            - Rasgos: cara ovalada, aspecto competente y amigable

    Obtiene la información de un personaje por nombre o ID.        """,

            "descripcion_corta": "doctora de 45 años, cabello castaño recogido, bata blanca, gafas rectangulares, estetoscopio, expresión profesional y amable",

    Args:        "personalidad": "inteligente, empática, profesional, tranquilizadora",

        nombre_o_id: Nombre, ID o alias del personaje        "ruta": "personajes/martina/martina_referencia.png"

            }

    Returns:}

        dict: Datos del personaje o None si no existe

    """# Mapeo de IDs alternativos (para compatibilidad)

    nombre_normalizado = nombre_o_id.lower().strip()ALIAS_PERSONAJES = {

        "don_juan": "juan",

    # Buscar directamente en PERSONAJES    "don juan": "juan",

    if nombre_normalizado in PERSONAJES:    "doctora": "martina",

        return PERSONAJES[nombre_normalizado]    "dra": "martina",

        "dra_martina": "martina",

    # Buscar en alias    "doctora_martina": "martina",

    if nombre_normalizado in ALIAS_PERSONAJES:}

        id_real = ALIAS_PERSONAJES[nombre_normalizado]

        return PERSONAJES.get(id_real)def obtener_personaje(nombre_o_id):

        """

    # Buscar por nombre completo    Obtiene la información de un personaje por nombre o ID.

    for pid, datos in PERSONAJES.items():    

        if datos["nombre"].lower() == nombre_normalizado:    Args:

            return datos        nombre_o_id: Nombre, ID o alias del personaje

            

    return None    Returns:

        dict: Datos del personaje o None si no existe

def listar_personajes():    """

    """Imprime la lista de todos los personajes disponibles"""    nombre_normalizado = nombre_o_id.lower().strip()

    print("\n" + "=" * 70)    

    print("PERSONAJES DISPONIBLES")    # Buscar directamente en PERSONAJES

    print("=" * 70)    if nombre_normalizado in PERSONAJES:

    for pid, datos in PERSONAJES.items():        return PERSONAJES[nombre_normalizado]

        print(f"\n🎭 {datos['nombre']} (ID: {pid})")    

        print(f"   Edad: {datos['edad']}")    # Buscar en alias

        print(f"   Personalidad: {datos['personalidad']}")    if nombre_normalizado in ALIAS_PERSONAJES:

        print(f"   📝 {datos['descripcion_corta']}")        id_real = ALIAS_PERSONAJES[nombre_normalizado]

    print("\n" + "=" * 70)        return PERSONAJES.get(id_real)

    
    # Buscar por nombre completo
    for pid, datos in PERSONAJES.items():
        if datos["nombre"].lower() == nombre_normalizado:
            return datos
    
    return None

def listar_personajes():
    """Imprime la lista de todos los personajes disponibles"""
    print("\n" + "=" * 70)
    print("PERSONAJES DISPONIBLES")
    print("=" * 70)
    for pid, datos in PERSONAJES.items():
        print(f"\n🎭 {datos['nombre']} (ID: {pid})")
        print(f"   Edad: {datos['edad']}")
        print(f"   Personalidad: {datos['personalidad']}")
        print(f"   📝 {datos['descripcion_corta']}")
    print("\n" + "=" * 70)
