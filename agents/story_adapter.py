"""
Adaptador de prompts según perfil del usuario
Personaliza la generación de guiones basado en edad, nivel y estilo
"""


class StoryAdapter:
    """
    Adapta los prompts de generación según el perfil del usuario
    """
    
    def adaptar_prompt_guion(self, prompt_base, perfil_usuario):
        """
        Modifica el prompt de Pipeline1Guion según preferencias del usuario.
        
        Args:
            prompt_base (str): Prompt original del pipeline
            perfil_usuario: Instancia de PerfilUsuario
            
        Returns:
            str: Prompt adaptado
        """
        
        # Obtener parámetros del perfil
        edad = perfil_usuario.edad_nino
        nivel = perfil_usuario.nivel_complejidad
        estilo = perfil_usuario.estilo_narrativo
        temas = perfil_usuario.temas_favoritos
        
        # Construir adaptaciones
        adaptaciones = self._build_adaptaciones(edad, nivel, estilo, temas)
        
        # Insertar adaptaciones en el prompt
        prompt_adaptado = f"""{prompt_base}

PERSONALIZACIONES OPCIONALES (solo aplicar si es compatible con la moraleja principal):
{adaptaciones}

⚠️ IMPORTANTE: La moraleja especificada arriba es PRIORITARIA sobre las personalizaciones.
Si hay conflicto entre la moraleja y estas sugerencias de estilo, la moraleja SIEMPRE gana."""
        
        return prompt_adaptado
    
    def _build_adaptaciones(self, edad, nivel, estilo, temas):
        """Construye las instrucciones de adaptación"""
        
        adaptaciones = []
        
        # 1. Adaptación por EDAD
        adaptaciones.append(self._adaptar_por_edad(edad))
        
        # 2. Adaptación por NIVEL DE COMPLEJIDAD
        adaptaciones.append(self._adaptar_por_nivel(nivel, edad))
        
        # 3. Adaptación por ESTILO NARRATIVO
        adaptaciones.append(self._adaptar_por_estilo(estilo))
        
        # 4. Adaptación por TEMAS FAVORITOS
        if temas:
            adaptaciones.append(self._adaptar_por_temas(temas))
        
        return '\n'.join(adaptaciones)
    
    def _adaptar_por_edad(self, edad):
        """Adaptación según la edad del niño"""
        if edad <= 5:
            return f"""
📅 EDAD: {edad} años (Preescolar)
- Vocabulario: MUY SIMPLE (máximo 80 palabras diferentes)
- Número de escenas: 5-6 (corto, mantiene atención)
- Duración total: 5-6 minutos
- Conceptos: CONCRETOS (no abstractos)
- Frases: CORTAS (máximo 10 palabras)
- Repetición: USAR frases repetitivas para reforzar
"""
        elif edad <= 7:
            return f"""
📅 EDAD: {edad} años (Inicial)
- Vocabulario: SIMPLE (100-120 palabras diferentes)
- Número de escenas: 6-7
- Duración total: 7-8 minutos
- Conceptos: SIMPLES con ejemplos concretos
- Frases: MODERADAS (10-15 palabras)
"""
        elif edad <= 9:
            return f"""
📅 EDAD: {edad} años (Primaria)
- Vocabulario: INTERMEDIO (150-200 palabras)
- Número de escenas: 7-8
- Duración total: 8-9 minutos
- Conceptos: COMBINACIÓN de concreto y abstracto
- Frases: VARIADAS (hasta 20 palabras)
"""
        else:
            return f"""
📅 EDAD: {edad} años (Avanzado)
- Vocabulario: RICO (200+ palabras diferentes)
- Número de escenas: 8-10
- Duración total: 9-10 minutos
- Conceptos: ABSTRACTOS permitidos
- Frases: COMPLEJAS (estructuras variadas)
"""
    
    def _adaptar_por_nivel(self, nivel, edad):
        """Adaptación según nivel de complejidad"""
        niveles = {
            'simple': f"""
📚 NIVEL: SIMPLE
- Trama: LINEAL (inicio → problema → solución → final)
- Personajes: 2-3 MÁXIMO
- Conflicto: UNO SOLO, muy claro
- Lección: EXPLÍCITA (los personajes la dicen directamente)
- Explicaciones: DIRECTAS, sin metáforas complejas
""",
            'medio': f"""
📚 NIVEL: MEDIO
- Trama: CON GIROS (pequeños desafíos adicionales)
- Personajes: 3-4, con roles definidos
- Conflicto: PRINCIPAL + 1 secundario
- Lección: SEMI-IMPLÍCITA (se deduce con ayuda)
- Explicaciones: ALGUNOS símiles simples permitidos
""",
            'avanzado': f"""
📚 NIVEL: AVANZADO
- Trama: MULTICAPA (subtramas entrelazadas)
- Personajes: 4-5, con desarrollo de personalidad
- Conflicto: MÚLTIPLES niveles
- Lección: IMPLÍCITA (el niño la descubre)
- Explicaciones: METÁFORAS y SIMBOLISMO apropiados
"""
        }
        return niveles.get(nivel, niveles['medio'])
    
    def _adaptar_por_estilo(self, estilo):
        """Adaptación según estilo narrativo"""
        estilos = {
            'aventurero': """
🎭 ESTILO: AVENTURERO
- Tono: ENERGÉTICO, emocionante
- Ritmo: RÁPIDO, con mucha acción
- Escenarios: DINÁMICOS (bosques, montañas, exploraciones)
- Verbos: De ACCIÓN (correr, saltar, descubrir, explorar)
- Emociones: INTENSAS pero positivas
- Elementos: Desafíos físicos, descubrimientos, valentía
Ejemplo: "¡Lucas corrió veloz hacia la cueva misteriosa!"
""",
            'educativo': """
🎭 ESTILO: EDUCATIVO
- Tono: DIDÁCTICO, explicativo
- Ritmo: PAUSADO, reflexivo
- Escenarios: COTIDIANOS (escuela, casa, parque)
- Verbos: De APRENDIZAJE (aprender, entender, pensar, descubrir)
- Emociones: MODERADAS, enfocadas en comprensión
- Elementos: Explicaciones claras, ejemplos, conclusiones
Ejemplo: "El Abuelo Sabio explicó: 'La honestidad es como una semilla...'"
""",
            'fantastico': """
🎭 ESTILO: FANTÁSTICO
- Tono: MÁGICO, maravilloso
- Ritmo: ENVOLVENTE, misterioso
- Escenarios: IMAGINATIVOS (bosques encantados, castillos, nubes)
- Verbos: De MAGIA (brillar, transformar, aparecer, volar)
- Emociones: ASOMBRO, maravilla
- Elementos: Criaturas mágicas, poderes especiales, transformaciones
Ejemplo: "Las flores brillaron con luz dorada cuando Sofía dijo la verdad"
"""
        }
        return estilos.get(estilo, estilos['aventurero'])
    
    def _adaptar_por_temas(self, temas):
        """Adaptación según temas favoritos"""
        temas_str = ', '.join(temas)
        return f"""
🎨 TEMAS FAVORITOS: {temas_str}
- Incorporar estos elementos en las escenas cuando sea posible
- Si el tema es "animales": incluir mascotas, animales del bosque, etc.
- Si el tema es "aventura": incluir exploraciones, descubrimientos
- Si el tema es "amistad": enfatizar relaciones entre personajes
- Si el tema es "ciencia": incluir experimentos, descubrimientos
- Si el tema es "naturaleza": escenarios al aire libre, plantas, ecosistemas
"""
