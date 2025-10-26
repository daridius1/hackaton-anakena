"""
Gestor de Escenarios - Sistema de coherencia visual para backgrounds

Este módulo detecta y gestiona escenarios (backgrounds) para mantener
consistencia visual a lo largo de todas las escenas de un cuento.

Funcionalidad:
1. Detecta escenarios mencionados en las descripciones de escenas
2. Genera una imagen de referencia para cada escenario nuevo
3. Reutiliza escenarios existentes para mantener coherencia
4. Guarda escenarios en base de datos JSON para uso futuro
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from google import genai
from PIL import Image as PILImage

# Mapeo de palabras clave a escenarios
ESCENARIOS_KEYWORDS = {
    "bosque": ["bosque", "árboles", "naturaleza", "selva", "monte", "floresta"],
    "hospital": ["hospital", "clínica", "consultorio médico", "sala de emergencias", "enfermería"],
    "plaza": ["plaza", "parque", "área pública", "zona verde", "espacio público"],
    "calle": ["calle", "avenida", "vereda", "acera", "ciudad", "urbano", "camino"],
    "habitacion": ["habitación", "dormitorio", "cuarto", "pieza", "recámara"],
    "sala_de_clases": ["sala de clases", "aula", "salón", "clase", "escuela", "colegio"],
}


class GestorEscenarios:
    """Gestiona la coherencia visual de escenarios/backgrounds"""
    
    def __init__(self, db_path: str = "escenarios/escenarios.json", api_key: str = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.escenarios_db = self._cargar_db()
        self.api_key = api_key or "AIzaSyD6B6z-Q8En35eLWd401WDH6Rcvy5zkNZk"
        self.client = genai.Client(api_key=self.api_key)
        
    def _cargar_db(self) -> Dict:
        """Carga la base de datos de escenarios guardados"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _guardar_db(self):
        """Guarda la base de datos de escenarios"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.escenarios_db, f, ensure_ascii=False, indent=2)
    
    def detectar_escenario(self, descripcion: str) -> Optional[str]:
        """
        Detecta qué tipo de escenario se menciona en la descripción.
        
        Args:
            descripcion: Texto de imagen_descripcion de una escena
            
        Returns:
            Nombre del escenario detectado (ej: "parque", "bosque") o None
        """
        descripcion_lower = descripcion.lower()
        
        for escenario, keywords in ESCENARIOS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in descripcion_lower:
                    return escenario
        
        return None
    
    def analizar_cuento(self, escenas: List[Dict]) -> Dict[str, List[int]]:
        """
        Analiza todas las escenas del cuento para detectar escenarios.
        
        Args:
            escenas: Lista de escenas del guion.json
            
        Returns:
            Dict mapeando nombre_escenario -> [números de escena donde aparece]
        """
        escenarios_por_cuento = {}
        
        for escena in escenas:
            num_escena = escena.get("numero_escena")
            descripcion = escena.get("imagen_descripcion", "")
            
            escenario = self.detectar_escenario(descripcion)
            
            if escenario:
                if escenario not in escenarios_por_cuento:
                    escenarios_por_cuento[escenario] = []
                escenarios_por_cuento[escenario].append(num_escena)
        
        return escenarios_por_cuento
    
    def obtener_o_crear_escenario(self, nombre_escenario: str, descripcion_ejemplo: str = None) -> Optional[str]:
        """
        Obtiene la ruta de un escenario existente o genera uno nuevo.
        
        Args:
            nombre_escenario: Tipo de escenario (parque, bosque, etc.)
            descripcion_ejemplo: Descripción específica del cuento para generar
            
        Returns:
            Ruta al archivo PNG del escenario o None si falla
        """
        # Verificar si ya existe
        if nombre_escenario in self.escenarios_db:
            ruta_existente = self.escenarios_db[nombre_escenario].get("ruta")
            if ruta_existente and Path(ruta_existente).exists():
                print(f"      ♻️  Reutilizando escenario: {nombre_escenario}")
                return ruta_existente
        
        # Generar nuevo escenario
        print(f"      🎨 Generando nuevo escenario: {nombre_escenario}")
        ruta_imagen = self._generar_escenario(nombre_escenario, descripcion_ejemplo)
        
        if ruta_imagen:
            # Guardar en base de datos
            self.escenarios_db[nombre_escenario] = {
                "ruta": ruta_imagen,
                "descripcion": descripcion_ejemplo or f"Escenario tipo {nombre_escenario}",
                "generado_auto": True
            }
            self._guardar_db()
            
        return ruta_imagen
    
    def _generar_escenario(self, tipo_escenario: str, descripcion_ref: str = None) -> Optional[str]:
        """
        Genera una imagen de escenario/background usando Gemini.
        
        Args:
            tipo_escenario: Tipo de escenario (parque, bosque, etc.)
            descripcion_ref: Descripción de referencia del cuento
            
        Returns:
            Ruta al archivo generado o None si falla
        """
        # Prompts específicos por tipo de escenario
        prompts_escenarios = {
            "bosque": "Bosque mágico chileno con árboles altos de troncos marrones, hojas verdes abundantes, rayos de sol filtrándose entre las ramas, helechos, flores silvestres de colores, camino de tierra, ambiente misterioso y acogedor. Ilustración de libro infantil, sin personas.",
            
            "hospital": "Interior de hospital infantil moderno y acogedor con paredes celestes o verde menta, camilla blanca, equipo médico básico organizado, ventana grande con luz natural, pósters educativos alegres en las paredes, ambiente limpio y tranquilizador. Ilustración de libro infantil, sin personas.",
            
            "plaza": "Plaza pública alegre y colorida con árboles grandes, bancas de madera verde, flores en maceteros, pasto verde brillante, caminos de baldosas, faroles decorativos, cielo azul con nubes, ambiente acogedor y familiar. Ilustración de libro infantil, sin personas.",
            
            "calle": "Calle urbana chilena tranquila con casas coloridas, veredas amplias, árboles en las aceras, faroles, letreros de tiendas amigables, cielo azul, ambiente seguro y familiar. Ilustración de libro infantil, sin personas.",
            
            "habitacion": "Habitación infantil acogedora con cama con edredón colorido, ventana con cortinas alegres, estante con libros y juguetes, alfombra suave, lámpara de mesita, pósters en las paredes, ambiente cálido y seguro. Ilustración de libro infantil, sin personas.",
            
            "sala_de_clases": "Sala de clases infantil moderna con pizarra blanca o verde, escritorios pequeños de colores, estantes con libros y materiales educativos, ventanas grandes con luz natural, pósters educativos alegres en las paredes, mapas, números y letras decorativos. Ilustración de libro infantil, sin personas.",
        }
        
        prompt_base = prompts_escenarios.get(
            tipo_escenario,
            f"{tipo_escenario.capitalize()} colorido y alegre, ambiente infantil. Ilustración de libro infantil, sin personas."
        )
        
        prompt = f"""GENERAR ESCENARIO/BACKGROUND PARA CUENTO INFANTIL:

TIPO: {tipo_escenario}

DESCRIPCIÓN:
{prompt_base}

IMPORTANTE:
- NO incluir personas, niños, adultos ni personajes
- Solo el escenario/ambiente/lugar
- Colores brillantes y vibrantes
- Estilo de ilustración infantil profesional
- Perspectiva amplia del lugar
- Apropiado para superponer personajes después
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=prompt
            )
            
            # Extraer imagen
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Guardar imagen
                    output_dir = self.db_path.parent
                    output_file = output_dir / f"{tipo_escenario}_background.png"
                    
                    with open(output_file, "wb") as f:
                        f.write(part.inline_data.data)
                    
                    return str(output_file)
            
        except Exception as e:
            print(f"         ❌ Error generando escenario: {e}")
        
        return None
    
    def listar_escenarios(self):
        """Lista todos los escenarios disponibles en la base de datos"""
        if not self.escenarios_db:
            print("No hay escenarios guardados")
            return
        
        print("\n" + "=" * 60)
        print("ESCENARIOS DISPONIBLES")
        print("=" * 60)
        for nombre, datos in self.escenarios_db.items():
            print(f"\n🏞️  {nombre.upper()}")
            print(f"   Ruta: {datos.get('ruta')}")
            print(f"   Descripción: {datos.get('descripcion', 'N/A')}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    # Test del gestor
    gestor = GestorEscenarios()
    
    print("Generando escenarios de prueba...")
    
    # Generar escenarios básicos
    for escenario in ["parque", "bosque", "casa"]:
        ruta = gestor.obtener_o_crear_escenario(escenario)
        if ruta:
            print(f"✅ {escenario}: {ruta}")
    
    gestor.listar_escenarios()
