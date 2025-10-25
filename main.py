#!/usr/bin/env python3
"""
Orquestador Principal - Generador de Cuentos Infantiles
Ejecuta los 4 pipelines en secuencia para crear un video educativo completo.

Flujo:
1. Pipeline 1 (Guion): moraleja -> guion.json
2. Pipeline 2 (Audio): guion.json -> dialogue_N.mp3
3. Pipeline 3 (Imagen): guion.json -> image_N.png
4. Pipeline 4 (Video): todos los assets -> cuento_final.mp4

Uso:
    python main.py "no hablar con extraños"
    python main.py "compartir con los demás" --output mi_cuento.mp4
"""
import sys
import argparse
from pathlib import Path
from pipelines import Pipeline1Guion, Pipeline2Audio, Pipeline3Imagen, Pipeline4Video


def main():
    parser = argparse.ArgumentParser(
        description="Generador completo de cuentos infantiles educativos",
        epilog="Ejemplo: python main.py 'no hablar con extraños'"
    )
    parser.add_argument(
        "moraleja",
        help="La moraleja o lección de la historia (ej: 'no hablar con extraños')"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="cuento_final.mp4",
        help="Nombre del video de salida (default: cuento_final.mp4)"
    )
    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Saltar Pipeline 2 (útil si tus colegas no lo han implementado aún)"
    )
    parser.add_argument(
        "--skip-imagen",
        action="store_true",
        help="Saltar Pipeline 3 (útil si tus colegas no lo han implementado aún)"
    )
    parser.add_argument(
        "--skip-video",
        action="store_true",
        help="Saltar Pipeline 4 (útil para solo generar guion y assets)"
    )
    parser.add_argument(
        "--guion-only",
        action="store_true",
        help="Solo ejecutar Pipeline 1 (solo generar guion.json)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎨 GENERADOR DE CUENTOS INFANTILES EDUCATIVOS")
    print("=" * 70)
    print(f"Moraleja: '{args.moraleja}'")
    print(f"Output: {args.output}")
    print("=" * 70)
    print()
    
    try:
        # PIPELINE 1: Generar guion
        print("PASO 1/4: Generando guion...")
        pipeline1 = Pipeline1Guion()
        guion = pipeline1.generar(args.moraleja, output_path="guion.json")
        print()
        
        if args.guion_only:
            print("✅ Guion generado. Proceso terminado (--guion-only activado).")
            return 0
        
        # PIPELINE 2: Generar audio
        if not args.skip_audio:
            print("PASO 2/4: Generando audio de diálogos...")
            pipeline2 = Pipeline2Audio()
            audio_files = pipeline2.generar(guion_path="guion.json")
            print()
        else:
            print("⏭️  PASO 2/4: Audio SALTADO (--skip-audio activado)")
            print()
        
        # PIPELINE 3: Generar imágenes
        if not args.skip_imagen:
            print("PASO 3/4: Generando imágenes de escenas...")
            pipeline3 = Pipeline3Imagen()
            image_files = pipeline3.generar(guion_path="guion.json")
            print()
        else:
            print("⏭️  PASO 3/4: Imágenes SALTADAS (--skip-imagen activado)")
            print()
        
        # PIPELINE 4: Ensamblar video
        if not args.skip_video:
            print("PASO 4/4: Ensamblando video final...")
            pipeline4 = Pipeline4Video()
            video_path = pipeline4.generar(guion_path="guion.json", output_name=args.output)
            print()
        else:
            print("⏭️  PASO 4/4: Video SALTADO (--skip-video activado)")
            print()
        
        # Resumen final
        print("=" * 70)
        print("🎉 PROCESO COMPLETADO")
        print("=" * 70)
        print("Archivos generados:")
        print(f"  📄 Guion: guion.json")
        
        if not args.skip_audio:
            print(f"  🎵 Audio: assets/voices/dialogue_*.mp3")
        
        if not args.skip_imagen:
            print(f"  🖼️  Imágenes: assets/images/image_*.png")
        
        if not args.skip_video:
            print(f"  🎬 Video: assets/outputs/{args.output}")
        
        print()
        print("⚠️  NOTA: Los pipelines 2, 3 y 4 son placeholders.")
        print("   Tus colegas deben implementar las APIs de TTS e imágenes.")
        print("   Para video, instalar: pip install moviepy")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN EL PROCESO")
        print("=" * 70)
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print()
        print("Revisa:")
        print("  1. Que DEEPSEEK_API_KEY esté configurada en .env")
        print("  2. Que tengas conexión a internet")
        print("  3. Los logs arriba para más detalles")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
