import json

with open('modelos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total modelos: {len(data)}\n")
print(f"{'ID':>5} | {'NOMBRE':<45} | {'CATEGORIA':<25} | ARCHIVO LOCAL")
print("-" * 140)
for m in data[:15]:
    mid = m.get('id', '?')
    nombre = m.get('nombre', '?')
    cat = m.get('categoria', '?')
    archivo = m.get('archivo', '?')
    print(f"{mid:>5} | {nombre:<45} | {cat:<25} | {archivo}")

print(f"\n... y {len(data)-15} modelos más.")
