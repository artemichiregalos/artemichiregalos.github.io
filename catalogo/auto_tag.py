"""
Script para auto-etiquetar todos los PNGs de diseños usando GPT-4o Vision.
Lee cada SUBCARPETA de assets/modelos/ y usa el nombre de carpeta como categoría.
Genera modelos.json con nombre, categoria, tags, estilo y ambiente para cada diseño.

ESTRUCTURA DE CARPETAS ESPERADA:
  assets/modelos/
    animales/       → 1.png, 2.png ...
    naturaleza/     → 10.png, 11.png ...
    geometria/      → ...
    (etc.)

USO:
  1. Pon tus PNGs en la subcarpeta correcta dentro de assets/modelos/
  2. Pon tu OPENAI_API_KEY abajo
  3. Ejecuta: python catalogo/auto_tag.py
  4. Se generará: modelos.json en la raíz del proyecto

Coste estimado: ~$0.10 - $0.15 para 1000 imágenes (coste único, una sola vez)
Si se interrumpe, vuelve a ejecutarlo: retoma desde donde quedó.
"""

import os
import json
import base64
import time
from pathlib import Path
from openai import OpenAI

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
OPENAI_API_KEY = "TU_CLAVE_API_AQUI"   # ← Pon tu clave API aquí
MODELOS_DIR    = "../assets/modelos"     # Carpeta raíz con subcarpetas
OUTPUT_FILE    = "../modelos.json"       # Archivo de salida
BATCH_SIZE     = 10                      # Guardar progreso cada N imágenes
DELAY_SECONDS  = 1                       # Pausa entre tandas (evitar rate limit)
# ──────────────────────────────────────────────────────────────────────────────

# La categoría se toma del nombre de la subcarpeta, la IA solo genera lo demás
PROMPT_SISTEMA = """Eres un asistente que analiza diseños para corte láser monocapa.
Los diseños son siluetas o ilustraciones en negro sobre fondo blanco.
Ya conoces la categoría del diseño. Solo necesitas generar nombre, tags, estilo y ambiente.
Responde ÚNICAMENTE con un JSON válido, sin texto extra ni bloques de código.

Formato de respuesta (exactamente este JSON, sin nada más):
{
  "nombre": "nombre descriptivo corto en español (ej: Lobo aullando al claro de luna)",
  "tags": ["5 a 10 palabras clave en español que describan el diseño con detalle"],
  "estilo": "minimalista|detallado|geometrico|organico|caligrafico",
  "ambiente": "infantil|moderno|rustico|elegante|divertido|misterioso|romantico|neutro"
}"""

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def tag_image(client: OpenAI, image_path: Path, image_id: int, categoria: str, carpeta_real: str) -> dict:
    """Envía una imagen a GPT-4o Vision y obtiene nombre, tags, estilo y ambiente."""
    try:
        b64 = encode_image(str(image_path))
        ext = image_path.suffix.lstrip(".").lower()
        mime = f"image/{'jpeg' if ext in ['jpg','jpeg'] else 'png'}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "low"}
                        },
                        {
                            "type": "text",
                            "text": f"Categoría del diseño: {categoria}. Analiza la imagen y responde con el JSON."
                        }
                    ]
                }
            ],
            max_tokens=250,
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        # Limpiar posibles bloques markdown ```json ... ```
        if "```" in content:
            parts = content.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    content = part
                    break

        data = json.loads(content)
        # Añadir campos que la IA no genera (los ponemos nosotros)
        data["id"]        = image_id
        data["categoria"] = categoria
        data["archivo"]   = f"assets/modelos/{carpeta_real}/{image_path.name}"
        return data

    except json.JSONDecodeError as e:
        print(f"\n  [WARN]  JSON inválido en {image_path.name}: {e}")
        return _fallback(image_id, imagen_path=image_path, categoria=categoria, carpeta_real=carpeta_real)
    except Exception as e:
        print(f"\n  [ERROR] Error en {image_path.name}: {e}")
        return None

def _fallback(image_id: int, imagen_path: Path, categoria: str, carpeta_real: str) -> dict:
    """Devuelve un registro mínimo cuando falla la API."""
    return {
        "id":       image_id,
        "archivo":  f"assets/modelos/{carpeta_real}/{imagen_path.name}",
        "nombre":   f"Diseño {image_id}",
        "categoria": categoria,
        "tags":     [categoria],
        "estilo":   "minimalista",
        "ambiente": "neutro"
    }

def folder_to_categoria(folder_name: str) -> str:
    """
    Convierte el nombre de carpeta a un identificador de categoría
    limpio: minúsculas, espacios → guiones bajos.
    Ej: 'CUADROS MONOCAPA' → 'cuadros_monocapa'
    """
    return folder_name.strip().lower().replace(" ", "_")

def collect_images(base_path: Path) -> list[tuple[Path, str, str]]:
    """
    Recorre todas las subcarpetas de base_path y devuelve
    una lista de (ruta_imagen, categoria_clave, nombre_real_carpeta).
    Ignora archivos sueltos en la raíz (sin subcarpeta).
    """
    images = []
    for subfolder in sorted(base_path.iterdir()):
        if not subfolder.is_dir():
            continue
        categoria  = folder_to_categoria(subfolder.name)  # clave normalizada
        carpeta_real = subfolder.name                     # nombre tal cual en disco
        for img in sorted(
            list(subfolder.glob("*.png")) +
            list(subfolder.glob("*.jpg")) +
            list(subfolder.glob("*.jpeg")),
            key=lambda x: int(x.stem) if x.stem.isdigit() else 999999
        ):
            images.append((img, categoria, carpeta_real))
    return images

def main():
    modelos_path = Path(MODELOS_DIR)
    if not modelos_path.exists():
        print(f"[ERROR] No existe la carpeta: {modelos_path.resolve()}")
        return

    print("[>] Escaneando subcarpetas...")
    imagenes = collect_images(modelos_path)

    if not imagenes:
        print("[ERROR] No se encontraron imágenes en ninguna subcarpeta.")
        print(f"   Asegúrate de poner los PNGs dentro de subcarpetas en: {modelos_path.resolve()}")
        return

    # Resumen por categoría
    from collections import Counter
    conteo = Counter(cat for _, cat, _r in imagenes)
    print(f"\n[OK] {len(imagenes)} imágenes encontradas en {len(conteo)} categorías:")
    for cat, n in sorted(conteo.items()):
        print(f"   [DIR] {cat}: {n} diseños")
    print(f"\n[$] Coste estimado: ${len(imagenes) * 0.00015:.3f} aprox.\n")

    # ── Cargar progreso existente ──────────────────────────────────────────
    output_path = Path(OUTPUT_FILE)
    resultados: list[dict] = []
    ids_procesados: set[int] = set()

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            resultados = json.load(f)
            ids_procesados = {r["id"] for r in resultados}
        print(f"[~] Retomando — ya tienen datos {len(ids_procesados)} modelos\n")

    # ── ID global (continúa desde el último) ──────────────────────────────
    next_id = max(ids_procesados, default=0) + 1

    client = OpenAI(api_key=OPENAI_API_KEY)
    procesados_esta_sesion = 0

    for img_path, categoria, carpeta_real in imagenes:
        # Asignar ID: si el nombre es un número usamos ese, si no usamos el contador
        if img_path.stem.isdigit():
            img_id = int(img_path.stem)
        else:
            img_id = next_id
            next_id += 1

        if img_id in ids_procesados:
            continue

        print(f"[...] [{carpeta_real}] {img_path.name} (id={img_id})...", end=" ", flush=True)
        resultado = tag_image(client, img_path, img_id, categoria, carpeta_real)

        if resultado:
            resultados.append(resultado)
            ids_procesados.add(img_id)
            procesados_esta_sesion += 1
            print(f"[OK] \"{resultado.get('nombre', '?')}\"")
        else:
            fallback = _fallback(img_id, img_path, categoria, carpeta_real)
            resultados.append(fallback)
            ids_procesados.add(img_id)
            procesados_esta_sesion += 1
            print("[ERROR] Error → guardado registro mínimo")

        # Guardar progreso periódicamente
        if procesados_esta_sesion % BATCH_SIZE == 0:
            _guardar(resultados, output_path)
            print(f"\n[SAVE] Progreso guardado ({len(resultados)} modelos en total)\n")
            time.sleep(DELAY_SECONDS)

    # ── Guardar resultado final ────────────────────────────────────────────
    _guardar(resultados, output_path)
    print(f"\n[!] ¡Completado! {len(resultados)} modelos etiquetados en total.")
    print(f"[FILE] Archivo: {output_path.resolve()}")

def _guardar(resultados: list, output_path: Path):
    ordenados = sorted(resultados, key=lambda x: (x.get("categoria",""), x["id"]))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ordenados, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()


