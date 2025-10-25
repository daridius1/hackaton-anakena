"""
CLI to generate a children's script (guion) given ONLY the moral (moraleja).

Usage:
  python generate_guion.py "no hablar con extraños"

The script reads `DEEPSEEK_API_KEY` and `DEEPSEEK_API_URL` from the environment.
"""
import argparse
import json
import os
import sys

from deepseek_client import DeepseekClient


def main():
    parser = argparse.ArgumentParser(description="Genera un guion infantil en JSON partiendo de una moraleja")
    parser.add_argument("moraleja", help="La moraleja (ej: 'no hablar con extraños')")
    parser.add_argument("--save", help="Ruta a archivo donde guardar el JSON de salida", default=None)
    args = parser.parse_args()

    try:
        client = DeepseekClient()
    except Exception as exc:
        print("ERROR: no se pudo inicializar el cliente Deepseek:", str(exc), file=sys.stderr)
        print("Asegúrate de haber puesto DEEPSEEK_API_KEY y DEEPSEEK_API_URL en el entorno (o en .env).", file=sys.stderr)
        sys.exit(2)

    try:
        result = client.generate_guion(args.moraleja)
    except Exception as exc:
        print("ERROR generando guion:", str(exc), file=sys.stderr)
        sys.exit(3)

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Salida guardada en {args.save}")
    else:
        print(text)


if __name__ == "__main__":
    main()
