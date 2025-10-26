from django.contrib import admin
from .models import PerfilUsuario, InteraccionSugerencia


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'valores_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Valores Prioritarios', {
            'fields': ('valores_prioritarios',),
            'description': 'Usar formato JSON: ["empatía", "honestidad", "responsabilidad"]'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def valores_count(self, obj):
        """Muestra cantidad de valores prioritarios"""
        return len(obj.valores_prioritarios) if obj.valores_prioritarios else 0
    valores_count.short_description = 'Valores'


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

