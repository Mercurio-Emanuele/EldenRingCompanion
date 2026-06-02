// ═══════════════════════════════════════════════════════════════
//  NAV.JS — Injects topnav into every page, manages global state
// ═══════════════════════════════════════════════════════════════

const NAV_PAGES = [
  { id: 'tracker',   href: 'index.html',     icon: '📋', key: 'nav_tracker'  },
  { id: 'map',       href: 'map.html',        icon: '🗺️', key: 'nav_map',       wip: false },
  { id: 'build',     href: 'build.html',      icon: '⚙️', key: 'nav_build',     wip: true  },
  { id: 'bestiary',  href: 'bestiary.html',   icon: '📖', key: 'nav_bestiary',  wip: true  },
];

function getFound() {
  return JSON.parse(localStorage.getItem('er_found') || '{}');
}
function getTotalItems() {
  // Sum all items across categories - updated when data.js loads
  if (typeof ITEMS !== 'undefined') {
    return Object.values(ITEMS).reduce((s, arr) => s + arr.length, 0);
  }
  return 469;
}
function getFoundCount() {
  const found = getFound();
  return Object.values(found).filter(Boolean).length;
}

function buildNav(activePageId) {
  const lang = getLang();
  const found = getFoundCount();
  const total = getTotalItems();
  const pct   = total ? Math.round(found / total * 100) : 0;

  const linksHtml = NAV_PAGES.map(p => {
    const label = t(p.key);
    const wip   = p.wip ? `<span class="nav-wip" data-i18n="nav_wip">${t('nav_wip')}</span>` : '';
    return `<a href="${p.href}" class="nav-link${p.id === activePageId ? ' active' : ''}">
      <span class="nav-icon">${p.icon}</span>
      <span>${label}</span>
      ${wip}
    </a>`;
  }).join('');

  const navHtml = `
<nav class="topnav" role="navigation">
  <div class="topnav-inner">
    <a href="index.html" class="nav-logo" aria-label="Elden Ring Tracker Home">
      <div class="nav-logo-icon">⚔</div>
      <span class="nav-logo-text">ELDEN RING</span>
    </a>
    <div class="nav-links">${linksHtml}</div>
    <div class="nav-right">
      <div class="nav-progress" title="${found} / ${total} ${t('nav_progress')}">
        <div class="progress-track nav-progress-bar">
          <div class="progress-fill" id="navProgressFill" style="width:${pct}%"></div>
        </div>
        <span id="navProgressLabel">${found}/${total}</span>
      </div>
      <div class="lang-toggle" role="group" aria-label="Language">
        <button class="lang-btn${lang==='it'?' active':''}" data-lang="it" aria-label="Italiano">IT</button>
        <button class="lang-btn${lang==='en'?' active':''}" data-lang="en" aria-label="English">EN</button>
      </div>
    </div>
  </div>
</nav>`;

  // Inject into body start
  const existing = document.getElementById('topnav-mount');
  if (existing) {
    existing.innerHTML = navHtml;
  } else {
    const mount = document.createElement('div');
    mount.id = 'topnav-mount';
    mount.innerHTML = navHtml;
    document.body.insertBefore(mount, document.body.firstChild);
  }

  // Re-bind lang buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      setLang(btn.dataset.lang);
      buildNav(activePageId); // re-render nav with new lang
    });
  });
}

function updateNavProgress() {
  const found = getFoundCount();
  const total = getTotalItems();
  const pct   = total ? Math.round(found / total * 100) : 0;
  const fill  = document.getElementById('navProgressFill');
  const label = document.getElementById('navProgressLabel');
  if (fill)  fill.style.width  = pct + '%';
  if (label) label.textContent = `${found}/${total}`;
}

// Listen for found-item changes from tracker
window.addEventListener('foundchange', updateNavProgress);
