"""
URLs de la aplicación web de cuentos infantiles
"""
from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('generar/', views.generar_video, name='generar_video'),
    path('resultado/<str:video_id>/', views.resultado, name='resultado'),
    path('api/progreso/<str:task_id>/', views.progreso_api, name='progreso_api'),
]
