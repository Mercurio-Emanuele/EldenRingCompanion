// ═══════════════════════════════════════════════════════════════
//  I18N.JS — Italian / English translations
// ═══════════════════════════════════════════════════════════════

const TRANSLATIONS = {
  it: {
    // Nav
    nav_tracker:      'Tracker',
    nav_map:          'Mappa',
    nav_build:        'Build Planner',
    nav_bestiary:     'Bestiario',
    nav_wiki:         'Wiki',
    nav_progress:     'trovati',
    nav_wip:          'In arrivo',

    // Tracker page
    tracker_title:    'Item Tracker',
    tracker_sub:      'Base Game + Shadow of the Erdtree',
    search_ph:        'Cerca item, effetto, localizzazione…',
    filter_all:       'Tutti',
    filter_found:     '✓ Trovati',
    filter_notfound:  '✗ Non trovati',
    filter_sote:      'DLC: Shadow of the Erdtree',
    filter_base:      'Solo Base Game',
    results:          'risultati',
    found_of:         'trovati su',
    pct_label:        '%',

    // Categories
    cat_talismans:    'Talismani',
    cat_weapons:      'Armi',
    cat_armor:        'Armature',
    cat_sorceries:    'Incantesimi',
    cat_incantations: 'Incantazioni',
    cat_spiritashes:  'Spirit Ashes',
    cat_shields:      'Scudi',

    // Map page
    map_title:        'Mappa Interattiva',
    map_sub:          'Localizzazione di ogni item nelle Interregnum',
    map_coming:       'In costruzione',
    map_coming_desc:  'La mappa interattiva con i pin di ogni item è in sviluppo. Torna presto!',

    // Build planner
    build_title:      'Build Planner',
    build_sub:        'Pianifica il tuo personaggio',
    build_coming:     'In costruzione',
    build_coming_desc:'Il calcolatore di build con scaling armi e stat è in sviluppo.',

    // Bestiary
    bestiary_title:   'Bestiario',
    bestiary_sub:     'Nemici, boss, drop e strategie',
    bestiary_coming:  'In costruzione',
    bestiary_coming_desc: 'L\'enciclopedia di nemici e boss con strategie e drop table è in sviluppo.',

    // Item card
    dlc_base:   'Base',
    dlc_sote:   'SotE',
    loc_label:  'Posizione',

    // Footer
    footer_disclaimer: 'Fan project non ufficiale. Elden Ring è di FromSoftware / Bandai Namco.',
    footer_wiki:       'Dati basati su eldenring.wiki.gg',
  },

  en: {
    // Nav
    nav_tracker:      'Tracker',
    nav_map:          'Map',
    nav_build:        'Build Planner',
    nav_bestiary:     'Bestiary',
    nav_wiki:         'Wiki',
    nav_progress:     'found',
    nav_wip:          'Coming soon',

    // Tracker page
    tracker_title:    'Item Tracker',
    tracker_sub:      'Base Game + Shadow of the Erdtree',
    search_ph:        'Search items, effects, locations…',
    filter_all:       'All',
    filter_found:     '✓ Found',
    filter_notfound:  '✗ Not found',
    filter_sote:      'DLC: Shadow of the Erdtree',
    filter_base:      'Base Game only',
    results:          'results',
    found_of:         'found of',
    pct_label:        '%',

    // Categories
    cat_talismans:    'Talismans',
    cat_weapons:      'Weapons',
    cat_armor:        'Armor',
    cat_sorceries:    'Sorceries',
    cat_incantations: 'Incantations',
    cat_spiritashes:  'Spirit Ashes',
    cat_shields:      'Shields',

    // Map page
    map_title:        'Interactive Map',
    map_sub:          'Item locations across the Interregnum',
    map_coming:       'Under construction',
    map_coming_desc:  'The interactive map with item pins is in development. Check back soon!',

    // Build planner
    build_title:      'Build Planner',
    build_sub:        'Plan your character',
    build_coming:     'Under construction',
    build_coming_desc:'The build calculator with weapon scaling and stats is in development.',

    // Bestiary
    bestiary_title:   'Bestiary',
    bestiary_sub:     'Enemies, bosses, drops and strategies',
    bestiary_coming:  'Under construction',
    bestiary_coming_desc: 'The enemy and boss encyclopedia with strategies and drop tables is in development.',

    // Item card
    dlc_base:   'Base',
    dlc_sote:   'SotE',
    loc_label:  'Location',

    // Footer
    footer_disclaimer: 'Unofficial fan project. Elden Ring is owned by FromSoftware / Bandai Namco.',
    footer_wiki:       'Data sourced from eldenring.wiki.gg',
  }
};

// ── ITEM DATA TRANSLATIONS (effect/loc shown in chosen lang) ──
// Since item data is already Italian in the tracker, we keep a flag.
// For full bilingual item data we'd need a second data file –
// for now the UI chrome toggles language, item data stays as-is.

function getLang() {
  return localStorage.getItem('er_lang') || 'it';
}
function setLang(lang) {
  localStorage.setItem('er_lang', lang);
  document.documentElement.lang = lang;
  applyTranslations(lang);
  // Fire custom event so pages can re-render dynamic content
  window.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
}
function t(key) {
  const lang = getLang();
  return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) ||
         (TRANSLATIONS['it'][key]) || key;
}

function applyTranslations(lang) {
  const tr = TRANSLATIONS[lang] || TRANSLATIONS['it'];
  // Apply [data-i18n] attributes
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (tr[key] !== undefined) el.textContent = tr[key];
  });
  // Apply [data-i18n-ph] for placeholders
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.dataset.i18nPh;
    if (tr[key] !== undefined) el.placeholder = tr[key];
  });
  // Update lang buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

// Init on load
document.addEventListener('DOMContentLoaded', () => {
  applyTranslations(getLang());
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLang(btn.dataset.lang));
  });
});
