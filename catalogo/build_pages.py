import os

template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Artemichi - {TITLE}. Arte mediante corte y grabado láser.">
    <title>{TITLE} | Artemichi</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <style>
        .category-hero {
            padding: 8rem 2rem 4rem;
            background: linear-gradient(135deg, var(--clr-bg), #110e0c);
            border-bottom: 2px solid rgba(212, 175, 55, 0.1);
        }
        .category-subtitle {
            color: var(--clr-gold);
            font-size: 1.2rem;
            letter-spacing: 4px;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }
        .category-title {
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .category-desc {
            font-size: 1.2rem;
            color: var(--clr-text-muted);
            max-width: 800px;
            margin: 0 auto 3rem;
            line-height: 1.6;
        }
        
        .product-features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .feature-card {
            background: var(--clr-card);
            border: 1px solid rgba(212, 175, 55, 0.15);
            border-radius: 12px;
            padding: 2.5rem 2rem;
            text-align: left;
            transition: transform 0.3s ease, border-color 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--clr-gold);
            box-shadow: var(--glow);
        }
        .feature-card h4 {
            color: var(--clr-gold);
            font-family: 'Cinzel', serif;
            font-size: 1.4rem;
            margin-bottom: 1rem;
        }
        .feature-card p {
            color: var(--clr-text-muted);
            line-height: 1.6;
        }
        .feature-img-placeholder {
            width: 100%;
            height: 200px;
            background: rgba(255,255,255,0.02);
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--clr-text-muted);
            border: 1px dashed rgba(212, 175, 55, 0.3);
        }
        
        .materials-section {
            background: #110e0c;
            padding: 4rem 2rem;
            text-align: center;
        }
        .materials-container {
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            justify-content: center;
        }
        .material-badge {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--clr-gold);
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            color: var(--clr-text);
        }
        .material-badge span {
            color: var(--clr-gold);
            display: block;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .cta-section {
            padding: 5rem 2rem;
            text-align: center;
        }
        .cta-section h3 {
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            color: var(--clr-gold);
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <nav class="navbar" style="background: rgba(18, 15, 12, 0.95); backdrop-filter: blur(10px);">
        <a href="index.html" class="logo">
            <img src="assets/logo.webp" alt="Artemichi Logo" class="logo-img">
            <span class="logo-text"><span class="gold-text">ARTE</span>MICHI</span>
        </a>
        <ul class="nav-links">
            <li><a href="index.html#inicio">Inicio</a></li>
            <li><a href="index.html#catalogo">Catálogo</a></li>
            <li><a href="index.html#contacto">Contacto</a></li>
            <li><a href="javascript:history.back()" class="gold-text" style="border: 1px solid var(--clr-gold); padding: 5px 15px; border-radius: 20px;">Volver</a></li>
        </ul>
        <div class="mobile-menu-btn">&#9776;</div>
    </nav>

    <header class="category-hero text-center fade-in">
        <h2 class="category-subtitle">Colección {NUMBER}</h2>
        <h1 class="category-title">{TITLE}</h1>
        <p class="category-desc">{DESC}</p>
        <a href="https://wa.me/34711240002" target="_blank" class="btn primary-btn mt-4">Consultar Precios por WhatsApp</a>
    </header>

    <section class="product-types">
        <div class="container text-center pt-5">
            <h3 class="section-heading">Modelos Destacados</h3>
            <p class="text-muted mb-3">Aquí irán las galerías fotográficas de cada variante</p>
        </div>
        <div class="product-features-grid">
            {FEATURES}
        </div>
    </section>

    <section class="materials-section fade-in">
        <h3 class="section-heading" style="font-size: 2rem;">Acabados Disponibles</h3>
        <p class="mb-4 text-muted">Configuramos el diseño con materias primas de la máxima calidad.</p>
        <div class="materials-container">
            {MATERIALS}
        </div>
    </section>

    <section class="cta-section fade-in">
        <div class="container text-center">
            <h3>Magia en cada detalle.</h3>
            <p class="mb-4 text-muted mt-3" style="font-size: 1.2rem;">Atención exclusiva para cada cliente.</p>
            <a href="https://wa.me/34711240002" target="_blank" class="btn primary-btn mt-2" style="font-size: 1.1rem; padding: 15px 30px;">Hacer mi Encargo por WhatsApp</a>
        </div>
    </section>

    <footer>
        <div class="container text-center">
            <p>&copy; <span id="year"></span> Artemichi. Arte mediante corte y grabado láser. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script src="script.js"></script>
    <script>
        const faders = document.querySelectorAll('.fade-in');
        const appearOptions = { threshold: 0.15, rootMargin: "0px 0px -50px 0px" };
        const appearOnScroll = new IntersectionObserver(function(entries, observer) {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            });
        }, appearOptions);

        faders.forEach(fader => { appearOnScroll.observe(fader); });

        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navLinks = document.querySelector('.nav-links');
        if(mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => { navLinks.classList.toggle('active'); });
        }
        
        document.getElementById('year').textContent = new Date().getFullYear();
        document.body.classList.add('loaded');
        setTimeout(() => document.querySelector('.category-hero').classList.add('visible'), 100);
    </script>
</body>
</html>"""

def make_feature(title, desc):
    return f'''<div class="feature-card fade-in">
                <div class="feature-img-placeholder">[ Espacio para Imagen ]</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>'''

def make_material(icon, title, desc):
    return f'''<div class="material-badge">
                {icon} {title}
                <span>{desc}</span>
            </div>'''

pages_data = {
    'natalicios.html': {
        'TITLE': 'Natalicios',
        'NUMBER': '01',
        'DESC': 'El mejor comienzo merece el regalo más especial. Transformamos el instante mágico del nacimiento en un recuerdo eterno, artesanal y personalizado.',
        'FEATURES': [
            ('Placas con Cigüeña', 'Nombre, fecha, hora, peso y talla grabados en madera con espacio destinado para foto del bebé.'),
            ('Temáticas Personalizadas', 'Anime, superhéroes, naturaleza o universos mágicos. Diseños adaptados al gusto de los padres.'),
            ('A Medida', 'Cualquier temática, diversos tamaños, materiales y acabados para ser inigualable.'),
        ],
        'MATERIALS': [
            ('🪵', 'Madera Natural', 'Roble, Pino o Wengué.'),
            ('🎨', 'Foam Color', 'Pintado con la temática elegida.'),
        ]
    },
    'relojes.html': {
        'TITLE': 'Relojes de Pared',
        'NUMBER': '02',
        'DESC': 'Funcionalidad y arte grabados en el tiempo. Instrumentos para medir el tiempo convertidos en obras de arte decorativas únicas.',
        'FEATURES': [
            ('Temáticos de Ciudad', 'Skylines, monumentos y símbolos de cualquier ciudad del mundo elaborados con máxima precisión.'),
            ('Pop Culture y Personajes', 'Universo anime, diseño de videojuegos, películas, series... Tu pasión marcando las horas.'),
            ('Engranajes Steampunk', 'Mecanismo decorativo visualmente impactante, con estilo industrial y encanto artístico.'),
            ('Dedicados y Personalizados', 'Grabado de nombres, mensajes y fechas en un regalo funcional apto para conmemoraciones.')
        ],
        'MATERIALS': [
            ('🪵', 'Madera Monocapa/Bicapa', 'Múltiples texturas expuestas con precisión láser.'),
            ('✨', 'Acrílicos y Vinilos', 'Para toques metalizados exclusivos.'),
        ]
    },
    'multicapa.html': {
        'TITLE': 'Cuadros Multicapa',
        'NUMBER': '03',
        'DESC': 'Arte con profundidad y dimensión 3D. Obras tridimensionales impresionantes generadas mediante superposición de numerosas capas de material.',
        'FEATURES': [
            ('Paisajes Naturales', 'Montañas, bosques, atardeceres y oceanografía capturando majestuosidad volumétrica.'),
            ('Mecanismos y Engranajes', 'Relojería abstracta superponiendo mecanismos precisos con texturas variadas.'),
            ('Retratos Artísticos', 'La profundidad realza personas, mascotas o figuras emblemáticas capa sobre capa.'),
            ('Escenas Temáticas Custom', 'Proyección arquitectónica adaptada al gusto del decorador o cliente particular.')
        ],
        'MATERIALS': [
            ('🪵', 'Maderas MDF y Pino', 'Capas resistentes para gran grosor.'),
            ('✨', 'Combinación Texturas', 'Variación en colores por estratos.')
        ]
    },
    'escudos.html': {
        'TITLE': 'Escudos Heráldicos',
        'NUMBER': '05',
        'DESC': 'El orgullo de tu linaje tallado para siempre. Representación familiar, heráldica e historia elaboradas con la máxima fidelidad y grabado láser.',
        'FEATURES': [
            ('Formato de Pared Gran Tamaño', 'Reproducción espectacular para presidir estancias, salones y pasillos blasonados.'),
            ('Formato Sobremesa Clásico', 'Ideal para regalos informales, despachos elegantes y decoración central en vitrinas.'),
            ('Llaveros Heráldicos Premium', 'Grabado de su símbolo histórico en aluminio o maderas nobles a doble o una cara.'),
            ('Personalización Detallada', 'Inclusión de yelmos, listones y mantos diseñados por nuestro equipo.')
        ],
        'MATERIALS': [
            ('🛡️', 'Madera Gruesa Teñida', 'Sólido soporte rústico (15mm).'),
            ('⬛', 'Foam Negro Mate', 'Elegancia contrastada de alto relieve.')
        ]
    },
    'shadowbox.html': {
        'TITLE': 'Shadowbox (Luz y Sombra)',
        'NUMBER': '06',
        'DESC': 'Cajas en sombra donde se fusionan luz LED, láminas superpuestas y marcos estructurados para generar magia visual desde el primer segundo.',
        'FEATURES': [
            ('Universos Pop Culture con Luz', 'Películas, ciencia ficción y mangas retroiluminados desde la base creando un ambiente onírico.'),
            ('Naturaleza y Fauna Nocturna', 'Escenarios marinos, montañas y animales iluminados creando atardeceres impresionantes.'),
            ('Bodas y Conmemoraciones', 'Preservación temática iluminada de recuerdos entrañables e instantáneas preciosas.')
        ],
        'MATERIALS': [
            ('💡', 'LED Integrado', 'Sistema eléctrico oculto en tonos cálido/frío.'),
            ('🪟', 'Marco de Pino Profundo', 'Construido a mano para encapsular la escena.')
        ]
    },
    'marcos.html': {
        'TITLE': 'Marcos para Fotos',
        'NUMBER': '07',
        'DESC': 'Cada momento merece un encuadre espectacular. Transforma un borde básico en el preámbulo visual y narrativo de un recuerdo inquebrantable.',
        'FEATURES': [
            ('Siluetas Decorativas y Especiales', 'Geometría láser integrando contornos de animales, mapas urbanos o naturaleza.'),
            ('Texto y Frases Alrededor', 'Fechas, nombres cursivos o juramentos distribuidos rodeando el instante atrapado.'),
            ('Collage Multi-Cuadro', 'Varias ranuras diseñadas meticulosamente para narrativas familiares completas de alto valor.')
        ],
        'MATERIALS': [
            ('🖼️', 'Madera y Foam Texturado', 'Cortes milimétricos al formato necesario.'),
        ]
    },
    'llaveros.html': {
        'TITLE': 'Llaveros Personalizados',
        'NUMBER': '08',
        'DESC': 'Pequeñas obras de arte que acompañan tu día a día, perfectos para un regalo íntimo o seguridad identificativa robusta.',
        'FEATURES': [
            ('Madera de Haya Grabada', 'Acabado visual artesanal, natural y cálido con la inscripción inconfundible del láser.'),
            ('Acrílico con Relleno Color', 'Estilo inquebrantable elegante con capa acrílica grabada a gran profundidad.'),
            ('Aluminio Anodizado', 'Material top muy resistente y ligero, que revela la base resplandeciente del metal rascando la capa superior.'),
            ('Identificativos de Mascotas', 'Formas juguetonas y creativas para portar nombre, teléfono y microchips salvavidas.')
        ],
        'MATERIALS': [
            ('🪵', 'Madera de Haya', 'Noble, resistente a golpes.'),
            ('⚙️', 'Aluminio Anodizado', 'Ligeros pero ultra perdurables.')
        ]
    },
    'monocapa.html': {
        'TITLE': 'Cuadros Monocapa',
        'NUMBER': '09',
        'DESC': 'Minimalismo con alma: siluetas precisas de una sola capa cortadas con impacto directo que visten y reinventan la pared que ocupan.',
        'FEATURES': [
            ('Conceptuales en Madera Natural', 'Contornos estilizados proyectando calidez total ideal para estilos de decoración nórdica.'),
            ('Mandalas y Geometrías', 'Cortes intrincados entrelazados que sirven de atrayente y descanso visual mural.'),
            ('Iconografía y Vinilados', 'Figuras deportivas, retratos pop y acabados espejo que reflejan y multiplican la amplitud del espacio.'),
        ],
        'MATERIALS': [
            ('⬛', 'Foam Pintado Especial', 'Ligeros para escaparates y locales.'),
            ('✨', 'Fibra y Metálicos', 'Acabados singulares con vinilos luxury.')
        ]
    },
    'luz.html': {
        'TITLE': 'Cuadros de Luz',
        'NUMBER': '10',
        'DESC': 'Luz, decoración y láser. Una alternativa contemporánea al tradicional cuadro. Una lámina translúcida se enciende mostrando diseños espectaculares que enamoran en la oscuridad.',
        'FEATURES': [
            ('Marcos Premium Retroiluminados', 'Bastidor natural trabajado y oscurecido por nosotros enmarcando plexiglás reactivo a la luz lateral.'),
            ('Iluminación Ambienta Controlada', 'Integración perfecta cálida / fría creando destellos cautivadores e invisibles si están apagados.'),
            ('Bodas, Regalos y Negocios', 'Impresionante para destacar firmas locales comerciales o captar la atención total a una memoria de pareja.')
        ],
        'MATERIALS': [
            ('💡', 'LED Lateral Reactivo', 'Cristalería acrílica cortada e impactada que frena y refracta luz.'),
        ]
    }
}

target_dir = "../"
for filename, data in pages_data.items():
    feats_str = "\\n".join([make_feature(t, d) for t, d in data['FEATURES']])
    mats_str = "\\n".join([make_material(i, t, d) for i, t, d in data['MATERIALS']])
    
    html = template.replace("{TITLE}", data['TITLE']) \
                   .replace("{NUMBER}", data['NUMBER']) \
                   .replace("{DESC}", data['DESC']) \
                   .replace("{FEATURES}", feats_str) \
                   .replace("{MATERIALS}", mats_str)
    
    filepath = os.path.join(target_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {filename}")
