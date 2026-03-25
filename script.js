document.addEventListener("DOMContentLoaded", () => {
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
    openModalBtn.addEventListener("click", () => {
        modal.classList.add("show");
        document.body.style.overflow = "hidden"; // Prevent background scroll
    });

    // Close Modal
    closeModalBtn.addEventListener("click", () => {
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
