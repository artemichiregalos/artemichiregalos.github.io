"""
Script para renombrar archivos del catalogo local anadiendo el Nro de modelo delante.
Ejemplo: aguila.png -> 004_aguila.png
"""

import json
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# -- Configuracion --
MODELOS_JSON = r"c:\Users\kiria\OneDrive\Escritorio\artemichiregalos.github.io\modelos.json"
CATALOGO_DIR = r"C:\Users\kiria\Mi unidad\LASER\CATALOGO"
DRY_RUN = False  # True = solo muestra lo que haria, False = renombra de verdad

# Extensiones de archivo a procesar
EXTENSIONES = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.bmp', '.tiff'}

# Archivos a ignorar
IGNORAR = {'desktop.ini', 'thumbs.db'}

def normalize_name(name):
    return name.strip().lower()

def main():
    # 1. Cargar modelos.json
    with open(MODELOS_JSON, 'r', encoding='utf-8') as f:
        modelos = json.load(f)
    
    nombre_a_id = {}
    duplicados = {}
    
    for m in modelos:
        archivo = m.get('archivo', '')
        mid = m.get('id', 0)
        basename = os.path.splitext(os.path.basename(archivo))[0]
        key = normalize_name(basename)
        
        if key in nombre_a_id:
            if key not in duplicados:
                duplicados[key] = [nombre_a_id[key]]
            duplicados[key].append(mid)
        else:
            nombre_a_id[key] = mid
    
    print(f"[INFO] Modelos cargados: {len(modelos)}")
    print(f"[INFO] Nombres unicos mapeados: {len(nombre_a_id)}")
    if duplicados:
        print(f"[AVISO] Nombres duplicados (mismo archivo, varios IDs): {len(duplicados)}")
    print()
    
    # 2. Recorrer catalogo local recursivamente
    catalogo = Path(CATALOGO_DIR)
    renombrados = []
    sin_match = []
    ya_renombrados = []
    
    for filepath in sorted(catalogo.rglob('*')):
        if not filepath.is_file():
            continue
        if filepath.suffix.lower() not in EXTENSIONES:
            continue
        if filepath.name.lower() in IGNORAR:
            continue
        
        nombre_sin_ext = filepath.stem
        key = normalize_name(nombre_sin_ext)
        
        # Comprobar si ya tiene prefijo de ID (ej: "0004_aguila")
        parts = nombre_sin_ext.split('_', 1)
        if len(parts) > 1 and parts[0].isdigit() and len(parts[0]) >= 3:
            ya_renombrados.append(filepath)
            continue
        
        if key in nombre_a_id:
            mid = nombre_a_id[key]
            nuevo_nombre = f"{mid:04d}_{filepath.name}"
            nuevo_path = filepath.parent / nuevo_nombre
            renombrados.append((filepath, nuevo_path, mid))
        else:
            sin_match.append(filepath)
    
    # 3. Mostrar resultados
    print("=" * 110)
    if DRY_RUN:
        print("  MODO SIMULACION (DRY RUN) -- No se renombrara nada")
    else:
        print("  MODO EJECUCION -- Se renombraran los archivos")
    print("=" * 110)
    print()
    
    print(f"[OK] Archivos a renombrar: {len(renombrados)}")
    print("-" * 110)
    for old, new, mid in renombrados:
        rel_old = old.relative_to(catalogo)
        rel_new_dir = old.parent.relative_to(catalogo)
        print(f"  N.{mid:>4d}  {str(rel_old):<65s} -> {new.name}")
    print()
    
    if sin_match:
        print(f"[SIN MATCH] Archivos sin coincidencia en modelos.json: {len(sin_match)}")
        print("-" * 110)
        for fp in sin_match:
            rel = fp.relative_to(catalogo)
            print(f"  {rel}")
        print()
    
    if ya_renombrados:
        print(f"[SKIP] Ya tienen prefijo numerico (se omiten): {len(ya_renombrados)}")
        print()
    
    if duplicados:
        print(f"[AVISO] Nombres con multiples IDs (se uso el primero):")
        print("-" * 110)
        for name, ids in list(duplicados.items()):
            print(f"  \"{name}\" -> IDs: {ids}")
        print()
    
    # 4. Ejecutar
    if not DRY_RUN and renombrados:
        print("Renombrando archivos...")
        ok = 0
        errores = 0
        for old, new, mid in renombrados:
            try:
                old.rename(new)
                ok += 1
            except Exception as e:
                print(f"  ERROR renombrando {old.name}: {e}")
                errores += 1
        print(f"\nCompletado: {ok} renombrados, {errores} errores")
    elif DRY_RUN and renombrados:
        print("=> Para ejecutar el renombrado real, cambia DRY_RUN = False en el script")
        print("   y vuelve a ejecutar: python renombrar_catalogo.py")

if __name__ == "__main__":
    main()
