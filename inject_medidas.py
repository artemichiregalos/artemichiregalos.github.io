import os
import re

collections_data = {
    'natalicios.html': {'price': '15', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'relojes.html': {'price': '15', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'multicapa.html': {'price': '20', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'frases.html': {'price': '10', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'escudos.html': {'price': '6', 'sizes': [20, 30, 45, 60], 'obs': 'Medida de la madera exterior.'},
    'shadowbox.html': {'price': '25', 'sizes': [20, 30, 42, 60], 'obs': 'Medidas más 2 cm de marco.'},
    'marcos.html': {'price': '15', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'llaveros.html': {'price': '6', 'sizes': None, 'obs': ''},
    'monocapa.html': {'price': '12', 'sizes': [20, 30, 45, 60], 'obs': ''},
    'luz.html': {'price': '25', 'sizes': [20, 30, 40, 60], 'obs': 'Medidas más 2 cm de marco.'},
    'caricaturas.html': {'price': '15', 'sizes': [20, 30, 40, 60], 'obs': 'Medidas más 2 cm de marco si modelo lo lleva.'},
    'aura.html': {'price': '20', 'sizes': [20, 30, 40, 60], 'obs': 'Grosor excepcional y metacrilato de alta pureza.'},
    'epic.html': {'price': '20', 'sizes': [20, 30, 40, 60], 'obs': 'Iluminación y efecto 3D integrados.'}
}

def generate_html_block(data):
    sizes = data['sizes']
    obs = data['obs']
    price = data['price']
    
    html = f"""
    <!-- PANEL DE MEDIDAS Y PRECIOS INYECTADO -->
    <style>
        .specs-section {{ padding: 4rem 2rem; max-width: 850px; margin: 0 auto; position: relative; z-index: 1; }}
        .specs-card {{ background: rgba(10, 8, 20, 0.4); backdrop-filter: blur(8px); border: 1px solid var(--clr-gold, #d4af37); border-radius: 12px; padding: 2.5rem; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.4); }}
        .specs-title {{ font-family: 'Cinzel', serif; font-size: 1.8rem; color: var(--clr-gold, #d4af37); margin-bottom: 0.5rem; }}
        .specs-subtitle {{ font-size: 0.9rem; color: var(--clr-text-muted, rgba(255,255,255,0.6)); margin-bottom: 2rem; line-height: 1.5; }}
        .sizes-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 1rem; margin-bottom: 2rem; justify-content: center; }}
        .size-box {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem 0.5rem; transition: transform 0.3s, border-color 0.3s; }}
        .size-box:hover {{ transform: translateY(-3px); border-color: var(--clr-gold, rgba(212, 175, 55, 0.5)); background: rgba(212, 175, 55, 0.05); }}
        .size-box span {{ display: block; font-size: 1.2rem; font-weight: 700; color: rgba(255,255,255,0.3); margin-bottom: 0.2rem; }}
        .size-box strong {{ font-size: 1.3rem; color: #fff; }}
        .specs-footer {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; gap: 1.5rem; border: 1px solid rgba(255,255,255,0.05); }}
        .specs-observations, .shipping-banner {{ display: flex; align-items: flex-start; gap: 10px; text-align: left; font-size: 0.9rem; color: var(--clr-text-muted, rgba(255,255,255,0.7)); line-height: 1.4; }}
        .specs-observations .icon, .shipping-banner .icon {{ font-size: 1.3rem; margin-top: 2px; }}
        .specs-pricing {{ text-align: right; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 1.5rem; min-width: 140px; }}
        .price-label {{ display: block; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--clr-gold, rgba(212, 175, 55, 0.8)); margin-bottom: 0.2rem; }}
        .price-amount {{ font-family: 'Cinzel', serif; font-size: 2.2rem; color: #fff; font-weight: 700; line-height: 1; }}
        .shipping-banner {{ background: rgba(212, 175, 55, 0.08); border-radius: 8px; padding: 1rem; border: 1px dashed rgba(212, 175, 55, 0.3); justify-content: center; align-items: center; text-align: center; margin-bottom: 2rem; }}
        @media (max-width: 600px) {{ .specs-footer {{ flex-direction: column; align-items: center; text-align: center; }} .specs-observations {{ justify-content: center; text-align: center; }} .specs-pricing {{ border-left: none; border-top: 1px solid rgba(255,255,255,0.1); padding-left: 0; padding-top: 1rem; width: 100%; text-align: center; }} .sizes-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    </style>
    <section class="specs-section fade-in">
        <div class="specs-card">
            <h3 class="specs-title">Formatos Disponibles y Precios</h3>
    """
    
    if sizes:
        html += """
            <p class="specs-subtitle">La medida indicada corresponde al <b>lado más largo</b> (según la orientación o proporción del diseño).</p>
            <div class="sizes-grid">
        """
        for label, val in zip(['S', 'M', 'L', 'XL'], sizes):
            html += f"""<div class="size-box"><span>{label}</span><strong>{val} cm</strong></div>\n"""
            
        html += """            </div>"""
    else:
        # Para llaveros, tamaño único
        html += """
            <p class="specs-subtitle">Diseños optimizados en un <b>tamaño y proporción únicos</b> para garantizar portabilidad y resistencia.</p>
        """

    html += f"""
            <div class="specs-footer">
    """
    
    if obs:
        html += f"""
                <div class="specs-observations">
                    <span class="icon">ℹ️</span> 
                    <p><strong>Observaciones:</strong> {obs}</p>
                </div>
        """
    else:
        html += f"""
                <div class="specs-observations">
                    <span class="icon">ℹ️</span> 
                    <p>Producción artesanal a medida tras validación del diseño final.</p>
                </div>
        """

    html += f"""
                <div class="specs-pricing">
                    <span class="price-label">Precio Desde</span>
                    <span class="price-amount">{price} €</span>
                </div>
            </div>

            <div class="shipping-banner">
                <span class="icon">📦</span> 
                <p><strong>Envíos:</strong> De 1,99€ a 4,99€. <strong>¡GRATIS para pedidos superiores a 75€!</strong></p>
            </div>

            <a href="https://wa.me/34711240002" target="_blank" class="btn primary-btn mt-4" style="width: 100%; text-align: center; display: block; font-size: 1.1rem; padding: 15px;">Pedir Presupuesto / Hacer Encargo</a>
        </div>
    </section>
    <!-- FIN PANEL INYECTADO -->
    """
    
    return html

for filename, data in collections_data.items():
    if not os.path.exists(filename):
        print(f"Skipping {filename}, not found.")
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Limpiar panel inyectado previo si lo hubiera (por re-runs)
    content = re.sub(r'\s*<!-- PANEL DE MEDIDAS Y PRECIOS INYECTADO -->.*?<!-- FIN PANEL INYECTADO -->\s*', '', content, flags=re.DOTALL)
        
    if filename in ['aura.html', 'epic.html']:
        # Remover las secciones product-info previas
        content = re.sub(r'<section class="product-info">.*?</section>', '', content, flags=re.DOTALL)
        
    # Encontrar ancla.
    # Primero buscamos '<!-- PROCESO -->' o '<section class="process' o '<div class="proceso-section'
    anchor_re = re.compile(r'(\s*<(?:section|div)[^>]*class="[^"]*(?:process-bg|process-section|proceso-section).*?>)', re.IGNORECASE)
    
    # Si no tiene proceso, buscaremos 'cta-section' (ej: relojes.html)
    if not anchor_re.search(content):
        anchor_re = re.compile(r'(\s*<section[^>]*class="[^"]*cta-section.*?>)', re.IGNORECASE)
        
    match = anchor_re.search(content)
    if match:
        block = generate_html_block(data)
        content = content[:match.start()] + '\n' + block + '\n' + content[match.start():]
        print(f"Inyectado en {filename} antes del ancla.")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"No se pudo encontrar ancla en {filename}")
