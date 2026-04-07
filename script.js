document.addEventListener("DOMContentLoaded", () => {
    // --- SEGURIDAD ANTI-COPIAS Y CAPTURAS ---
    // Prevenir click derecho
    document.addEventListener('contextmenu', event => event.preventDefault());
    // Prevenir atajos de teclado
    document.addEventListener('keydown', (e) => {
        if (e.key === 'F12') { e.preventDefault(); return false; }
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) { e.preventDefault(); return false; }
        if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'p' || e.key === 'u' || e.key === 'c')) { e.preventDefault(); return false; }
        if (e.key === 'PrintScreen') {
            navigator.clipboard.writeText('');
            e.preventDefault(); 
            return false;
        }
    });

    // Current Year in Footer
    document.getElementById("year").textContent = new Date().getFullYear();

    // Navbar Scroll Effect
    const navbar = document.querySelector(".navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // Mobile Menu Toggle
    const mobileBtn = document.querySelector(".mobile-menu-btn");
    const navLinks = document.querySelector(".nav-links");
    
    mobileBtn.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });

    // Smooth Scroll for Navigation Links
    document.querySelectorAll('.nav-links a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if(href === '#') {
                e.preventDefault();
                return;
            }
            
            if (href.includes('#')) {
                const hash = '#' + href.split('#')[1];
                const targetElement = document.querySelector(hash);
                
                // Si el elemento existe en ESTA página, hacemos scroll suave
                if (targetElement) {
                    e.preventDefault();
                    navLinks.classList.remove("active");
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
                // Si NO existe (estamos en otra página), no bloqueamos la navegación.
                // El navegador nos llevará naturalmente a index.html#seccion
            }
        });
    });

    // Intersection Observer for Scroll Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: stop observing once animated
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => observer.observe(el));

    // Active link highlighting on scroll
    const sections = document.querySelectorAll("section, header");
    const navItems = document.querySelectorAll(".nav-links a");

    window.addEventListener("scroll", () => {
        let current = "";
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute("id");
            }
        });

        navItems.forEach((a) => {
            a.classList.remove("active");
            if (a.getAttribute("href").includes(current) && current !== "") {
                a.classList.add("active");
            }
        });
    });

    // --- CARTA DE COLORES INTERACTIVA ---
    const colorChart = [
        { id: 'blanco', name: 'Blanco', hex: '#FFFFFF' },
        { id: 'hueso', name: 'Blanco Hueso', hex: '#F2F0E6' },
        { id: 'safari', name: 'Marrón Safari', hex: '#C69C6D' },
        { id: 'amarillo', name: 'Amarillo Claro', hex: '#FCEB6B' },
        { id: 'dalal', name: 'Naranja Dalal', hex: '#ECA764' },
        { id: 'lava', name: 'Naranja Lava', hex: '#FF7B00' },
        { id: 'kalani', name: 'Naranja Kalani', hex: '#FF6200' },
        { id: 'dingo', name: 'Marrón Dingo', hex: '#CFA58A' },
        { id: 'tana', name: 'Marrón Tana', hex: '#B97E59' },
        { id: 'glace', name: 'Marrón Glacé', hex: '#5C3A21' },
        { id: 'negro', name: 'Negro', hex: '#111111' },
        { id: 'rojo', name: 'Rojo Vivo', hex: '#E30022' },
        { id: 'burdeos', name: 'Rojo Burdeos', hex: '#8A033E' },
        { id: 'magenta', name: 'Magenta', hex: '#e3008c' },
        { id: 'comunidad', name: 'Violeta Comunidad', hex: '#9370DB' },
        { id: 'sultan', name: 'Violeta Sultán', hex: '#800080' },
        { id: 'lluvia', name: 'Azul Lluvia', hex: '#ADD8E6' },
        { id: 'libertad', name: 'Azul Libertad', hex: '#00BFFF' },
        { id: 'electrico', name: 'Azul Eléctrico', hex: '#0000FF' },
        { id: 'oscuro', name: 'Azul Oscuro', hex: '#002366' },
        { id: 'formentera', name: 'Azul Formentera', hex: '#008B8B' },
        { id: 'neon', name: 'Verde Neón', hex: '#39FF14' },
        { id: 'valle', name: 'Verde Valle', hex: '#228B22' },
        { id: 'toscana', name: 'Verde Toscana', hex: '#556B2F' },
        { id: 'java', name: 'Verde Java', hex: '#00FA9A' },
        { id: 'dragon', name: 'Verde Dragón', hex: '#004b23' },
        { id: 'perla', name: 'Gris Perla', hex: '#D3D3D3' },
        { id: 'lobo', name: 'Gris Lobo', hex: '#555555' }
    ];

    const modal = document.getElementById("colors-modal");
    const openModalBtn = document.getElementById("open-colors-modal");
    const closeModalBtn = document.querySelector(".close-modal");
    const colorsGrid = document.getElementById("colors-grid");
    const recommendationsPanel = document.getElementById("color-recommendations");

    // Open Modal
    if(openModalBtn) openModalBtn.addEventListener("click", () => {
        modal.classList.add("show");
        document.body.style.overflow = "hidden"; // Prevent background scroll
    });

    // Close Modal
    if(closeModalBtn) closeModalBtn.addEventListener("click", () => {
        modal.classList.remove("show");
        document.body.style.overflow = "auto";
    });

    // Close on outside click
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("show");
            document.body.style.overflow = "auto";
        }
    });

    // Render colors
    if (colorsGrid) {
        colorChart.forEach((color, index) => {
            const item = document.createElement("div");
            item.classList.add("color-item");
            item.style.backgroundColor = color.hex;
            
            // Add name explicitly
            const nameLabel = document.createElement("div");
            nameLabel.classList.add("color-name");
            
            // If the color is too bright, make text dark? Standard is white with background map overlay.
            nameLabel.textContent = color.name;
            item.appendChild(nameLabel);
            
            item.addEventListener("click", () => {
                document.querySelectorAll(".color-item").forEach(c => c.classList.remove("selected"));
                item.classList.add("selected");
                showRecommendations(color, index);
            });
            
            colorsGrid.appendChild(item);
        });
    }

    function showRecommendations(selectedColor, index) {
        // Always aim for a good neutral as one of the recommendations
        let neutral = colorChart.find(c => c.id === 'safari'); 
        if(selectedColor.id === 'safari' || selectedColor.id === 'blanco' || selectedColor.id === 'hueso') {
            neutral = colorChart.find(c => c.id === 'negro');
        }
        
        // Use a Set to guarantee uniqueness
        const uniqueRecs = new Set();
        uniqueRecs.add(neutral);
        
        // Add 3 more pseudo-randomly calculated colors that are offset across the chart
        const offsets = [7, 14, Math.floor(colorChart.length / 2), 4, 9, 12];
        let offsetIndex = 0;
        
        while(uniqueRecs.size < 4 && offsetIndex < offsets.length) {
            const candidate = colorChart[(index + offsets[offsetIndex]) % colorChart.length];
            if (candidate.id !== selectedColor.id) {
                uniqueRecs.add(candidate);
            }
            offsetIndex++;
        }
        
        // Fallback in case we still don't have 4 (extremely unlikely)
        let fallbackIndex = 1;
        while(uniqueRecs.size < 4) {
            const candidate = colorChart[(index + fallbackIndex) % colorChart.length];
            if (candidate.id !== selectedColor.id) {
                uniqueRecs.add(candidate);
            }
            fallbackIndex++;
        }

        const finalRecs = Array.from(uniqueRecs);

        recommendationsPanel.innerHTML = `
            <div class="selected-color-info fade-in visible">
                <div class="selected-color-swatch" style="background-color: ${selectedColor.hex}"></div>
                <h4 style="font-family: var(--font-heading); color: #fff; font-size: 1.5rem;">${selectedColor.name}</h4>
                <p style="color: var(--clr-text-muted); font-size: 0.85rem;">Combina a la perfección con:</p>
            </div>
            <div class="rec-grid fade-in visible" style="margin-top: 20px;">
                ${finalRecs.map(rec => `
                    <div class="rec-item">
                        <div class="rec-swatch" style="background-color: ${rec.hex}"></div>
                        <span class="rec-name">${rec.name}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
});

// --- GLOBAL LIGHTBOX GALLERY ---
let galleryImages = [];
let currentGalleryIndex = 0;
let galleryInterval = null;

function createGalleryOverlay() {
    if (document.getElementById('global-gallery-modal')) return;
    
    const modalHTML = `
        <div id="global-gallery-modal" class="image-gallery-modal">
            <span class="close-gallery" onclick="cerrarGaleria()">×</span>
            <div class="gallery-nav-btn gallery-prev" onclick="cambiarImagenGaleria(-1, event)">‹</div>
            <div class="gallery-image-container" id="gallery-image-container" onclick="event.stopPropagation()">
                <!-- Imágenes se inyectarán aquí -->
            </div>
            <div class="gallery-nav-btn gallery-next" onclick="cambiarImagenGaleria(1, event)">›</div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Close on clicking outside
    document.getElementById('global-gallery-modal').addEventListener('click', function(e) {
        if (e.target.id === 'global-gallery-modal') {
            cerrarGaleria();
        }
    });
}

window.abrirGaleria = function(imagesArray) {
    if (!imagesArray || imagesArray.length === 0) return;
    createGalleryOverlay();
    
    galleryImages = imagesArray;
    currentGalleryIndex = 0;
    
    const container = document.getElementById('gallery-image-container');
    container.innerHTML = '';
    
    // Create image elements
    imagesArray.forEach((src, idx) => {
        const img = document.createElement('img');
        img.src = src;
        if (idx === 0) img.classList.add('active');
        container.appendChild(img);
    });
    
    const modal = document.getElementById('global-gallery-modal');
    modal.style.display = 'flex';
    // Trigger reflow for transition
    setTimeout(() => { modal.classList.add('show'); }, 10);
    
    // Navigation arrows visibility
    const prevBtn = document.querySelector('.gallery-prev');
    const nextBtn = document.querySelector('.gallery-next');
    if (imagesArray.length > 1) {
        prevBtn.style.display = 'flex';
        nextBtn.style.display = 'flex';
        iniciarIntervaloGaleria();
    } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
        detenerIntervaloGaleria();
    }
};

window.cerrarGaleria = function() {
    const modal = document.getElementById('global-gallery-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => { modal.style.display = 'none'; }, 400);
    }
    detenerIntervaloGaleria();
};

window.cambiarImagenGaleria = function(dir, event) {
    if (event) event.stopPropagation();
    detenerIntervaloGaleria(); // Stop auto rotation if user clicks manually
    
    const imgs = document.getElementById('gallery-image-container').querySelectorAll('img');
    imgs[currentGalleryIndex].classList.remove('active');
    
    currentGalleryIndex = (currentGalleryIndex + dir + galleryImages.length) % galleryImages.length;
    
    imgs[currentGalleryIndex].classList.add('active');
};

function iniciarIntervaloGaleria() {
    detenerIntervaloGaleria();
    galleryInterval = setInterval(() => {
        const imgs = document.getElementById('gallery-image-container').querySelectorAll('img');
        if(imgs.length > 0) {
            imgs[currentGalleryIndex].classList.remove('active');
            currentGalleryIndex = (currentGalleryIndex + 1) % galleryImages.length;
            imgs[currentGalleryIndex].classList.add('active');
        }
    }, 3500);
}

function detenerIntervaloGaleria() {
    if (galleryInterval) {
        clearInterval(galleryInterval);
        galleryInterval = null;
    }
}

// ─── BANNER DE COOKIES (AEPD-compliant) ─────────────────────────────────────
(function initCookieBanner() {
    if (localStorage.getItem('artemichi_cookies_consent')) return;

    const banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.innerHTML = `
        <div style="
            position:fixed; bottom:0; left:0; right:0; z-index:99999;
            background:rgba(15,12,9,0.97); backdrop-filter:blur(12px);
            border-top:1px solid rgba(212,175,55,0.25);
            padding:1.25rem 2rem; display:flex; align-items:center;
            gap:1.5rem; flex-wrap:wrap; justify-content:space-between;
            box-shadow:0 -4px 30px rgba(0,0,0,0.6);
            animation: slideUpBanner 0.4s ease;
        ">
            <div style="flex:1; min-width:220px;">
                <p style="color:#e8e2d2; font-size:0.9rem; margin:0 0 0.3rem; line-height:1.6;">
                    🍪 <strong style="color:#d4af37;">Artemichi usa cookies</strong> técnicas para el correcto funcionamiento del sitio web.
                </p>
                <p style="color:#a9a396; font-size:0.8rem; margin:0;">
                    Puedes consultar nuestra <a href="cookies.html" style="color:#d4af37; text-decoration:none;">Política de Cookies</a> y <a href="privacidad.html" style="color:#d4af37; text-decoration:none;">Política de Privacidad</a>.
                </p>
            </div>
            <div style="display:flex; gap:0.75rem; flex-shrink:0;">
                <button id="cookies-reject" style="
                    background:transparent; border:1px solid rgba(255,255,255,0.2);
                    color:#a9a396; border-radius:6px; padding:0.5rem 1.25rem;
                    cursor:pointer; font-size:0.88rem; transition:all 0.2s;
                " onmouseover="this.style.borderColor='#fff';this.style.color='#fff'" onmouseout="this.style.borderColor='rgba(255,255,255,0.2)';this.style.color='#a9a396'">
                    Solo técnicas
                </button>
                <button id="cookies-accept" style="
                    background:linear-gradient(135deg,#c9a227,#a07d1a); border:none;
                    color:#1a1208; border-radius:6px; padding:0.5rem 1.25rem;
                    cursor:pointer; font-size:0.88rem; font-weight:700; transition:opacity 0.2s;
                " onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                    Aceptar todas
                </button>
            </div>
        </div>
        <style>
            @keyframes slideUpBanner {
                from { transform: translateY(100%); }
                to { transform: translateY(0); }
            }
        </style>
    `;
    document.body.appendChild(banner);

    document.getElementById('cookies-accept').addEventListener('click', () => {
        localStorage.setItem('artemichi_cookies_consent', 'all');
        banner.style.transition = 'opacity 0.4s';
        banner.style.opacity = '0';
        setTimeout(() => banner.remove(), 400);
    });

    document.getElementById('cookies-reject').addEventListener('click', () => {
        localStorage.setItem('artemichi_cookies_consent', 'essential');
        banner.style.transition = 'opacity 0.4s';
        banner.style.opacity = '0';
        setTimeout(() => banner.remove(), 400);
    });
})();
