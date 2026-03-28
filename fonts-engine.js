/**
 * Artemichi Font Engine
 * Core logic for font metadata, responsive previews, and AI-lite recommendations.
 * (User uploads disabled - Permanent library only)
 */

// Global state
window.PAGES = window.PAGES || [];

const FONT_STYLE = {
  "Cooper Black":    "Nombres · Decoración hogar",
  "Gil Sans Ultra":  "Nombres · Moderno y limpio",
  "MarvinVisions":   "Frases · Estilo actual",
  "Impact":          "Deporte · Clubes · Impacto",
  "Bauhaus 93":      "Moderno · Geométrico",
  "Britannic Bold":  "Títulos · Elegante y serio",
  "Showcard Gothic": "Comercios · Carteles",
  "Magneto":         "Tecnología · Ciencia ficción",
  "Matura SC":       "Bodas · Elegancia clásica",
  "Harlow Italic":   "Bodas · Romántico · Femenino",
  "Ananda Black":    "Caligrafía · Regalos · Amor",
  "Ananda":          "Caligrafía · Frases delicadas",
  "Super Joyful":    "Infantil · Cumpleaños · Alegre",
  "Forte":           "Frases cortas · Decorativo",
  "Harrington":      "Clásico ornamental · Marcos",
  "ITC Blackadder":  "Halloween · Misterio · Terror",
  "Ravie":           "Infantil · Divertido · Colorido",
  "CCUpUpAndAway":   "Cómics · Superhéroes · Niños",
  "Corleone":        "Mafia · El Padrino · Clásico",
  "Gill Sans Cd":    "Texto largo · Frases · Limpio",
  "Old English":     "Apellidos · Rock · Heráldica",
  "Germania":        "Medieval · Viking · Metal",
  "Celtic":          "Celta · Vikingo · Naturaleza",
  "Heraldica":       "Escudos · Heráldica · Linaje",
  "Heralcica":       "Escudos · Familia · Nobleza",
  "Aljaziran":       "Árabe · Oriente · Exótico",
  "Star Jedi":       "Star Wars · Ciencia ficción",
  "Batman":          "Batman · DC Comics · Superhéroes",
  "Saiyan Sans":     "Dragon Ball · Anime · Manga",
  "Assassins":       "Assassin's Creed · Videojuegos",
  "Heineken":        "Cervezas · Bares · Hostelería",
  "Love Live":       "Anime · Pop japonés · Kawaii",
  "Artemichi":       "Marca Artemichi · Corporativo",
  "aAngkatanBersenjata": "Militar · Letra de stencil",
  "Bulletto Killa":    "Script · Urbano · Graffiti",
  "cocacola":          "Marca Cocacola · Refresco · Retro",
  "HERALCICA":         "Heráldica · Escudos · Nobleza",
  "HERALDICA":         "Heráldica · Escudos · Linaje",
  "LOKICOLA":          "Script · Marca · Cocacola Variación",
  "Meliane":           "Caligrafía · Elegante · Invitaciones",
  "Tenada":            "Sólida · Letra gruesa · Carteles",
  "The Secret Mouse":  "Infantil · Disney · Divertido",
  "waltographUI":      "Marca Disney · Waltograph · Mágico",
};

const THEMES = {
    "star wars": ["Star Jedi"], "starwars": ["Star Jedi"], "jedi": ["Star Jedi"], "darth": ["Star Jedi"], 
    "batman": ["Batman"], "gotham": ["Batman"], 
    "dragon ball": ["Saiyan Sans"], "goku": ["Saiyan Sans"], "saiyan": ["Saiyan Sans"], "dbz": ["Saiyan Sans"], "vegeta": ["Saiyan Sans"], 
    "assassin": ["Assassins"], 
    "heineken": ["Heineken"], "cerveza": ["Heineken"], 
    "love live": ["Love Live"], "anime": ["Love Live", "Saiyan Sans"], 
    "disney": ["The Secret Mouse", "waltographUI"], 
    "militar": ["aAngkatanBersenjata"], "stencil": ["aAngkatanBersenjata"],
    "urbano": ["Bulletto Killa"], "graffiti": ["Bulletto Killa"],
    "cocacola": ["cocacola", "LOKICOLA"],
    "metallica": ["Old English"], "rock": ["Old English", "Germania"], "metal": ["Old English", "Germania"], 
    "medieval": ["Old English", "Germania", "Celtic"], "vikingo": ["Celtic", "Germania"], "celta": ["Celtic", "Germania"], 
    "escudo": ["Heraldica", "Heralcica", "Old English", "HERALDICA", "HERALCICA"], "heraldica": ["Heraldica", "Heralcica", "HERALDICA", "HERALCICA"], 
    "familia": ["Old English", "Corleone", "Germania"], "apellido": ["Old English", "Corleone", "Germania"], 
    "boda": ["Harlow Italic", "Matura SC", "Ananda", "Meliane"], "amor": ["Ananda", "Harlow Italic"], 
    "niño": ["CCUpUpAndAway", "Super Joyful", "Ravie", "The Secret Mouse"], "niña": ["CCUpUpAndAway", "Super Joyful", "Ananda", "The Secret Mouse"], 
    "infantil": ["CCUpUpAndAway", "Super Joyful", "Cooper Black", "The Secret Mouse"], 
    "mafia": ["Corleone"], "padrino": ["Corleone"], 
    "arabe": ["Aljaziran"], "arabic": ["Aljaziran"], 
    "navidad": ["Super Joyful", "Ananda Black"], 
    "futbol": ["Impact", "Bauhaus 93"], "deporte": ["Impact", "Bauhaus 93"], 
    "elegante": ["Matura SC", "Harlow Italic", "Corleone", "Meliane"], 
    "artemichi": ["Artemichi"]
};

/**
 * VIBES Keyword Mapping for the AI-Lite recommendation engine
 */
const VIBES = {
    "Romantic": {
        keywords: ["amor", "love", "siempre", "boda", "wedding", "novios", "pareja", "corazon", "heart", "querido", "querida"],
        boost: ["Ananda", "Harlow Italic", "Matura SC", "Ananda Black"]
    },
    "Kids/Playful": {
        keywords: ["niño", "niña", "kids", "bebe", "baby", "cumple", "birthday", "juego", "toy", "infantil", "alegre"],
        boost: ["CCUpUpAndAway", "Super Joyful", "Ravie", "Cooper Black"]
    },
    "SciFi/Tech": {
        keywords: ["tecnologia", "futuro", "juego", "game", "robot", "star wars", "jedi", "batman", "espacio"],
        boost: ["Star Jedi", "Batman", "Magneto", "Assassins"]
    },
    "Elegant/Formal": {
        keywords: ["elegante", "formal", "titulo", "certificado", "señor", "señora", "empresa", "corporativo"],
        boost: ["Matura SC", "Britannic Bold", "Bauhaus 93", "Artemichi"]
    },
    "Retro/Vintage": {
        keywords: ["vintage", "retro", "viejo", "old", "clasico", "classic", "rock", "metal"],
        boost: ["Old English", "Germania", "Celtic", "Corleone"]
    }
};

/**
 * Calculates responsive font size for previews
 */
function getClampedSize() {
    if (typeof state === 'undefined') return 40;
    let base = state.fontSize || 40;
    if (state.texto) {
        if (state.texto.length > 25) base = 30;
        if (state.texto.length > 45) base = 22;
    }
    const maxByScreen = Math.floor(window.innerWidth * 0.11);
    const finalSize = Math.min(base, maxByScreen, 60);
    return Math.max(finalSize, 16);
}

/**
 * Detects thematic matches based on user text
 */
function detectThemes(text) {
    if (!text) return [];
    const lower = text.toLowerCase();
    const matched = new Set();
    for (const [kw, fnames] of Object.entries(THEMES)) {
        if (lower.includes(kw)) {
            fnames.forEach(f => matched.add(f));
        }
    }
    return [...matched];
}

/**
 * Injects @font-face style
 */
function registerFont(name, base64) {
    const styleId = `font-face-${name.replace(/\s+/g, '-')}`;
    if (document.getElementById(styleId)) return;
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `@font-face { font-family: "${name}"; src: url(data:font/ttf;base64,${base64}); }`;
    document.head.appendChild(style);
}

/**
 * Core pagination
 */
function paginateFonts(fontList) {
    window.PAGES = [];
    for (let i = 0; i < fontList.length; i += 12) {
        window.PAGES.push(fontList.slice(i, i + 12));
    }
}

/**
 * AI-Lite Recommendations
 */
function getAdvancedRecommendations() {
    if (typeof state === 'undefined' || typeof FONTS === 'undefined') return [];

    let scores = {};
    const allFontNames = Object.keys(window.FONTS);
    allFontNames.forEach(fn => scores[fn] = 0);

    // 1. Theme matching
    if (state.tema) {
        const themeKey = state.tema.toLowerCase();
        for (let [kw, fnames] of Object.entries(THEMES)) {
            if (kw === themeKey) {
                fnames.forEach(fn => { if (scores[fn] !== undefined) scores[fn] += 20; });
            }
        }
    }

    // 2. Text Analysis
    if (state.texto) {
        const lowerText = state.texto.toLowerCase();
        for (let vibe in VIBES) {
            if (VIBES[vibe].keywords.some(kw => lowerText.includes(kw))) {
                VIBES[vibe].boost.forEach(fn => {
                    if (scores[fn] !== undefined) scores[fn] += 12;
                });
            }
        }
        const autoMatched = detectThemes(state.texto);
        autoMatched.forEach(fn => {
            if (scores[fn] !== undefined) scores[fn] += 10;
        });
        const textLen = state.texto.length;
        if (textLen < 8) {
            ["Cooper Black", "Impact", "Magneto", "Star Jedi"].forEach(fn => {
                if (scores[fn] !== undefined) scores[fn] += 5;
            });
        } else if (textLen > 40) {
            ["Gill Sans Cd", "Gil Sans Ultra", "Bauhaus 93"].forEach(fn => {
                if (scores[fn] !== undefined) scores[fn] += 5;
            });
        }
    }

    // 3. Usage matching
    if (state.uso) {
        const usageSearch = state.uso.toLowerCase();
        allFontNames.forEach(fn => {
            const styleLabel = (FONT_STYLE[fn] || "").toLowerCase();
            if (styleLabel.includes(usageSearch)) scores[fn] += 8;
        });
    }

    let ranked = allFontNames.filter(fn => scores[fn] > 0);
    ranked.sort((a, b) => scores[b] - scores[a] || a.localeCompare(b));
    return ranked;
}

/**
 * Navigation & Interaction
 */
function jumpToFont(name) {
    if (typeof PAGES === 'undefined') return;
    for (let i = 0; i < PAGES.length; i++) {
        if (PAGES[i].includes(name)) {
            state.page = i;
            if (typeof renderPage === 'function') renderPage();
            break;
        }
    }
    setTimeout(() => {
        const card = document.querySelector(`.font-card[data-font="${name}"]`);
        if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 150);
}

function changePage(dir) {
    if (typeof state === 'undefined') return;
    const np = state.page + dir;
    if (np >= 0 && np < PAGES.length) {
        state.page = np;
        if (typeof renderPage === 'function') renderPage();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function sendWA() {
    if (!state.selected) return;
    const msg = encodeURIComponent(
        `Hola! Me gustaría un letrero con la fuente *${state.selected}*.` +
        (state.texto ? `\n\nTexto: "${state.texto}"` : "")
    );
    window.open(`https://wa.me/34644040994?text=${msg}`, '_blank');
}

// Global Initialization
document.addEventListener('DOMContentLoaded', () => {
    if (typeof paginateFonts === 'function' && typeof FONTS !== 'undefined') {
        const allFonts = Object.keys(window.FONTS);
        paginateFonts(allFonts);
    }
});
