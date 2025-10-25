from django.contrib import admin
from .models import PerfilUsuario, InteraccionSugerencia


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'edad_nino', 'nivel_complejidad', 'estilo_narrativo', 'created_at')
    list_filter = ('nivel_complejidad', 'estilo_narrativo', 'created_at')
    search_fields = ('user__username', 'user__email')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Preferencias Básicas', {
            'fields': ('edad_nino', 'nivel_complejidad', 'estilo_narrativo')
        }),
        ('Preferencias de Contenido', {
            'fields': ('temas_favoritos', 'valores_prioritarios'),
            'description': 'Usar formato JSON: ["item1", "item2"]'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(InteraccionSugerencia)
class InteraccionSugerenciaAdmin(admin.ModelAdmin):
    list_display = ('user', 'moraleja_sugerida_short', 'fue_seleccionada', 'video_generado', 'created_at')
    list_filter = ('fue_seleccionada', 'video_generado', 'created_at')
    search_fields = ('user__username', 'moraleja_sugerida', 'razon_sugerencia')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Sugerencia', {
            'fields': ('moraleja_sugerida', 'razon_sugerencia', 'valores_cubiertos')
        }),
        ('Interacción', {
            'fields': ('fue_seleccionada', 'video_generado')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def moraleja_sugerida_short(self, obj):
        """Muestra versión corta de la moraleja"""
        return obj.moraleja_sugerida[:50] + '...' if len(obj.moraleja_sugerida) > 50 else obj.moraleja_sugerida
    moraleja_sugerida_short.short_description = 'Moraleja'

