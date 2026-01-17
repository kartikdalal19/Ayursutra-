// ---------------------------------------------------------------------------
// AyurSutra Translation Module
// ---------------------------------------------------------------------------

// A global object to hold our translations
let translations = {};

// Default language if none is detected or stored
const defaultLang = 'en';

// Function to fetch the language JSON file
async function fetchTranslations(lang) {
    try {
        const response = await fetch(`languages/${lang}.json`);
        if (!response.ok) {
            console.error(`Could not load translation file for: ${lang}`);
            return {};
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching translation file:', error);
        return {};
    }
}

// Function to apply the translations to the page
function applyTranslations() {
    // Find all elements that have a data-translate-key attribute
    document.querySelectorAll('[data-translate-key]').forEach(element => {
        const key = element.getAttribute('data-translate-key');
        // If a translation exists for this key, update the element's text
        if (translations[key]) {
            // Use textContent for most elements, but check for placeholders in inputs
            if (element.placeholder) {
                element.placeholder = translations[key];
            } else {
                element.textContent = translations[key];
            }
        }
    });
}

// Function to change the language and re-translate the page
async function setLanguage(lang) {
    // Store the selected language in localStorage to remember the choice
    localStorage.setItem('ayursutra_lang', lang);

    // Fetch the new language file
    translations = await fetchTranslations(lang);

    // Re-apply the translations to the entire page
    applyTranslations();

    // Update the language selector display
    updateLanguageSelector(lang);
}

// Function to initialize the translator
async function initTranslator() {
    // Get the stored language or detect browser language, fall back to default
    let currentLang = localStorage.getItem('ayursutra_lang') || navigator.language.split('-')[0] || defaultLang;

    // A list of supported languages. Add new language codes here.
    const supportedLangs = ['en', 'hi', 'es', 'fr']; // English, Hindi, Spanish, French
    
    // If the detected language is not supported, fall back to English
    if (!supportedLangs.includes(currentLang)) {
        currentLang = defaultLang;
    }

    // Load the translations and apply them
    translations = await fetchTranslations(currentLang);
    applyTranslations();
    
    // Populate and set up the language switcher dropdown
    setupLanguageSelector(supportedLangs, currentLang);
}

// Creates the language dropdown in the navbar
function setupLanguageSelector(supportedLangs, currentLang) {
    const container = document.getElementById('language-switcher-container');
    if (!container) return;

    // The structure: Icon -> Dropdown Button -> Dropdown Menu
    container.innerHTML = `
        <i class="fa-solid fa-globe me-1"></i>
        <div class="dropdown">
            <button class="btn btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                ${currentLang.toUpperCase()}
            </button>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="languageDropdown">
                ${supportedLangs.map(lang => `<li><a class="dropdown-item" href="#" data-lang="${lang}">${getLanguageName(lang)}</a></li>`).join('')}
            </ul>
        </div>
    `;
    
    updateLanguageSelector(currentLang);

    // Add event listeners to the new dropdown items
    container.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const lang = e.target.getAttribute('data-lang');
            setLanguage(lang);
        });
    });
}

// Updates the dropdown button to show the current language
function updateLanguageSelector(lang) {
    const dropdownButton = document.getElementById('languageDropdown');
    if (dropdownButton) {
        dropdownButton.textContent = lang.toUpperCase();
    }
}

// Helper to get the full name of a language from its code
function getLanguageName(langCode) {
    const names = {
        'en': 'English',
        'hi': 'हिन्दी (Hindi)',
        'es': 'Español (Spanish)',
        'fr': 'Français (French)'
    };
    return names[langCode] || langCode.toUpperCase();
}


// Run the translator when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initTranslator);
