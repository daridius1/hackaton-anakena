"""
Agente educativo principal (EduAgent)
Integra el filtro ético y el motor de preferencias
"""

from .content_filter import ContentFilter
from .preference_engine import PreferenceEngine


class EduAgent:
    """
    Agente educativo que:
    1. Genera sugerencias personalizadas
    2. Filtra contenidos inapropiados
    3. Aprende de las preferencias del usuario
    """
    
    def __init__(self, user_profile=None):
        self.profile = user_profile
        self.content_filter = ContentFilter()
        self.preference_engine = PreferenceEngine()
    
    def obtener_sugerencias(self, n=5):
        """
        Obtiene sugerencias personalizadas para el usuario.
        
        Args:
            n: Número de sugerencias a generar
            
        Returns:
            list: Lista de sugerencias validadas
        """
        if not self.profile:
            return self._get_sugerencias_genericas(n)
        
        # Obtener historial de interacciones
        historial = self.profile.user.interacciones.all()
        
        # Generar sugerencias personalizadas
        sugerencias = self.preference_engine.generar_sugerencias(
            self.profile,
            historial,
            n=n
        )
        
        return sugerencias
    
    def validar_moraleja(self, moraleja):
        """
        Valida que una moraleja sea apropiada.
        
        Args:
            moraleja (str): La moraleja a validar
            
        Returns:
            dict: Resultado de la validación
        """
        return self.content_filter.validar_moraleja(moraleja)
    
    def registrar_interaccion(self, moraleja, razon, valores, seleccionada=False):
        """
        Registra la interacción del usuario con una sugerencia.
        
        Args:
            moraleja (str): La moraleja sugerida
            razon (str): Por qué se sugirió
            valores (list): Valores cubiertos
            seleccionada (bool): Si el usuario la seleccionó
        """
        if not self.profile:
            return
        
        from webapp.models import InteraccionSugerencia
        
        InteraccionSugerencia.objects.create(
            user=self.profile.user,
            moraleja_sugerida=moraleja,
            razon_sugerencia=razon,
            valores_cubiertos=valores,
            fue_seleccionada=seleccionada
        )
    
    def marcar_video_generado(self, moraleja):
        """
        Marca que se generó un video para una moraleja específica.
        
        Args:
            moraleja (str): La moraleja del video generado
        """
        if not self.profile:
            return
        
        from webapp.models import InteraccionSugerencia
        
        # Buscar la última interacción con esta moraleja
        interaccion = InteraccionSugerencia.objects.filter(
            user=self.profile.user,
            moraleja_sugerida=moraleja
        ).first()
        
        if interaccion:
            interaccion.video_generado = True
            interaccion.fue_seleccionada = True
            interaccion.save()
    
    def _get_sugerencias_genericas(self, n):
        """Sugerencias genéricas para usuarios no logueados"""
        return [
            {
                'moraleja': 'compartir con los demás',
                'razon': 'Enseña generosidad y empatía',
                'valores': ['empatía', 'generosidad'],
                'prioridad': 5
            },
            {
                'moraleja': 'ser honesto siempre',
                'razon': 'Refuerza la importancia de la verdad',
                'valores': ['honestidad', 'integridad'],
                'prioridad': 5
            },
            {
                'moraleja': 'no hablar con extraños',
                'razon': 'Enseña seguridad personal',
                'valores': ['seguridad', 'precaución'],
                'prioridad': 4
            },
            {
                'moraleja': 'cuidar el medio ambiente',
                'razon': 'Conciencia ambiental',
                'valores': ['responsabilidad', 'respeto'],
                'prioridad': 4
            },
            {
                'moraleja': 'ayudar a los demás',
                'razon': 'Desarrolla solidaridad',
                'valores': ['empatía', 'solidaridad'],
                'prioridad': 3
            }
        ][:n]
