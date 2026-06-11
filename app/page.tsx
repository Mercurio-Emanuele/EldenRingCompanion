"use client";

import { useState, useEffect, useMemo } from "react";
import { ITEMS, CATEGORIES, Item, Category, imgUrl } from "./data/items";

const STORAGE_KEY = "er-companion-v2";

function loadDiscovered(): Set<string> {
  if (typeof window === "undefined") return new Set();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? new Set(JSON.parse(raw) as string[]) : new Set();
  } catch { return new Set(); }
}
function saveDiscovered(ids: Set<string>) {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...ids]));
}

// ─── Image with fallback ──────────────────────────────────────────────────────
function ItemImage({ file, name, size = 56 }: { file: string; name: string; size?: number }) {
  const [failed, setFailed] = useState(false);
  if (failed) {
    return (
      <div style={{
        width: size, height: size, minWidth: size, background: "var(--bg-dark)",
        display: "flex", alignItems: "center", justifyContent: "center",
        color: "var(--text-muted)", fontSize: size * 0.22, flexShrink: 0,
        letterSpacing: "0.08em", textTransform: "uppercase", fontFamily: "monospace"
      }}>
        {name.slice(0, 2)}
      </div>
    );
  }
  return (
    <img
      src={imgUrl(file)}
      alt={name}
      width={size}
      height={size}
      style={{ objectFit: "contain", flexShrink: 0 }}
      onError={() => setFailed(true)}
    />
  );
}

// ─── Modal ────────────────────────────────────────────────────────────────────
function ItemModal({ item, discovered, onClose, onToggle }: {
  item: Item; discovered: boolean; onClose: () => void; onToggle: () => void;
}) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const cat = CATEGORIES.find(c => c.id === item.category);

  return (
    <div className="modal-overlay fade-in" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{ padding: "28px 28px 20px", borderBottom: "1px solid var(--border)" }}>
          <div style={{ display: "flex", alignItems: "flex-start", gap: 20 }}>
            <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: 10, flexShrink: 0 }}>
              <ItemImage file={item.imageFile} name={item.name} size={80} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, color: cat?.color || "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 6 }}>
                {cat?.icon} {cat?.label}{item.subcategory ? ` · ${item.subcategory}` : ""}
              </div>
              <h2 className="font-cinzel" style={{ fontSize: "1.3rem", color: "var(--text-primary)", lineHeight: 1.2, marginBottom: 8 }}>
                {item.name}
              </h2>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                {item.legendary && <span className="badge badge-legendary">★ Legendary</span>}
                {item.dlc && <span className="badge badge-dlc">Shadow of the Erdtree</span>}
                {discovered && <span className="badge badge-discovered">✓ Discovered</span>}
              </div>
            </div>
            <button onClick={onClose} style={{ background: "none", border: "none", color: "var(--text-muted)", fontSize: 22, cursor: "pointer", lineHeight: 1, padding: "0 4px", flexShrink: 0 }}>×</button>
          </div>
        </div>

        <div style={{ padding: "22px 28px", display: "flex", flexDirection: "column", gap: 18 }}>
          {/* Description */}
          <div>
            <div className="rune-divider" style={{ marginBottom: 10 }}><span>Description</span></div>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.88rem", lineHeight: 1.7, fontStyle: "italic" }}>{item.description}</p>
          </div>

          {/* Effect */}
          {item.effect && (
            <div>
              <div className="rune-divider" style={{ marginBottom: 10 }}><span>Effect</span></div>
              <p style={{ color: "var(--gold-light)", fontSize: "0.88rem", lineHeight: 1.6 }}>{item.effect}</p>
            </div>
          )}

          {/* Stats */}
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            {item.requirements && (
              <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: "10px 14px", flex: 1, minWidth: 160 }}>
                <div style={{ fontSize: 10, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 4 }}>Requirements</div>
                <div style={{ fontSize: "0.82rem", color: "var(--text-primary)" }}>{item.requirements}</div>
              </div>
            )}
            {item.fp !== undefined && (
              <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                <div style={{ fontSize: 10, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 4 }}>FP Cost</div>
                <div style={{ fontSize: "0.82rem", color: "#6E9AC8" }}>{item.fp}</div>
              </div>
            )}
            {item.slots !== undefined && (
              <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                <div style={{ fontSize: 10, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 4 }}>Memory Slots</div>
                <div style={{ fontSize: "0.82rem", color: "var(--gold)" }}>{item.slots}</div>
              </div>
            )}
            {item.weight !== undefined && (
              <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                <div style={{ fontSize: 10, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 4 }}>Weight</div>
                <div style={{ fontSize: "0.82rem", color: "var(--text-primary)" }}>{item.weight}</div>
              </div>
            )}
          </div>

          {/* Location */}
          <div>
            <div className="rune-divider" style={{ marginBottom: 10 }}><span>How to Obtain</span></div>
            <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span style={{ color: "var(--gold)", fontSize: 14, marginTop: 1 }}>📍</span>
              <p style={{ color: "var(--text-secondary)", fontSize: "0.88rem", lineHeight: 1.6 }}>{item.location}</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{ padding: "16px 28px", borderTop: "1px solid var(--border)", display: "flex", justifyContent: "flex-end" }}>
          <button
            onClick={onToggle}
            style={{
              background: discovered ? "rgba(200,169,110,0.12)" : "rgba(200,169,110,0.06)",
              border: `1px solid ${discovered ? "var(--gold)" : "var(--border)"}`,
              color: discovered ? "var(--gold)" : "var(--text-secondary)",
              padding: "10px 22px", cursor: "pointer", fontSize: "0.82rem",
              letterSpacing: "0.08em", textTransform: "uppercase", transition: "all 0.2s", fontFamily: "inherit",
            }}
          >
            {discovered ? "✓ Mark as Undiscovered" : "◯ Mark as Discovered"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Item Card ────────────────────────────────────────────────────────────────
function ItemCard({ item, discovered, onClick }: { item: Item; discovered: boolean; onClick: () => void }) {
  return (
    <div className={`item-card fade-in ${discovered ? "discovered" : ""}`} onClick={onClick}
      style={{ padding: "14px", display: "flex", alignItems: "center", gap: 14 }}>
      <div style={{ background: "var(--bg-dark)", border: "1px solid var(--border)", padding: 6, flexShrink: 0 }}>
        <ItemImage file={item.imageFile} name={item.name} size={48} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
          <span className="font-cinzel" style={{
            fontSize: "0.82rem", color: discovered ? "var(--gold-light)" : "var(--text-primary)",
            lineHeight: 1.3, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis"
          }}>{item.name}</span>
          {item.legendary && <span style={{ color: "var(--gold)", fontSize: 10, flexShrink: 0 }}>★</span>}
          {item.dlc && <span style={{ color: "#9B6FD4", fontSize: 9, flexShrink: 0 }}>DLC</span>}
        </div>
        <p style={{
          fontSize: "0.72rem", color: "var(--text-muted)", lineHeight: 1.4,
          display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden"
        }}>
          {item.effect || item.description}
        </p>
      </div>
      {discovered && <div style={{ width: 8, height: 8, borderRadius: "50%", background: "var(--gold)", flexShrink: 0, boxShadow: "0 0 6px var(--gold)" }} />}
    </div>
  );
}

// ─── Progress ────────────────────────────────────────────────────────────────
function ProgressSection({ discovered }: { discovered: Set<string> }) {
  const total = ITEMS.length;
  const found = discovered.size;
  const pct = total > 0 ? Math.round((found / total) * 100) : 0;
  const byCat = CATEGORIES.map(cat => {
    const catItems = ITEMS.filter(i => i.category === cat.id);
    const catFound = catItems.filter(i => discovered.has(i.id)).length;
    return { ...cat, total: catItems.length, found: catFound };
  });

  return (
    <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "22px 28px", marginBottom: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <div>
          <div className="font-cinzel" style={{ fontSize: "0.85rem", color: "var(--text-muted)", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 4 }}>Collection Progress</div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
            <span className="gold-gradient font-cinzel" style={{ fontSize: "2rem", fontWeight: 700 }}>{found}</span>
            <span style={{ color: "var(--text-muted)", fontSize: "1rem" }}>/ {total}</span>
            <span style={{ color: "var(--gold-dark)", fontSize: "0.8rem" }}>items discovered</span>
          </div>
        </div>
        <div className="font-cinzel gold-gradient" style={{ fontSize: "2.5rem", fontWeight: 700 }}>{pct}%</div>
      </div>
      <div className="stats-bar" style={{ marginBottom: 18 }}>
        <div className="stats-bar-fill" style={{ width: `${pct}%` }} />
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 10 }}>
        {byCat.filter(c => c.total > 0).map(cat => (
          <div key={cat.id} style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontSize: "0.68rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>{cat.icon} {cat.label}</span>
              <span style={{ fontSize: "0.68rem", color: cat.found === cat.total ? "var(--gold)" : "var(--text-muted)" }}>{cat.found}/{cat.total}</span>
            </div>
            <div className="stats-bar">
              <div className="stats-bar-fill" style={{ width: `${cat.total > 0 ? (cat.found / cat.total) * 100 : 0}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main App ─────────────────────────────────────────────────────────────────
export default function Home() {
  const [discovered, setDiscovered] = useState<Set<string>>(new Set());
  const [activeCategory, setActiveCategory] = useState<Category | "all">("all");
  const [search, setSearch] = useState("");
  const [filterMode, setFilterMode] = useState<"all" | "found" | "missing">("all");
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);
  const [showLegendaryOnly, setShowLegendaryOnly] = useState(false);
  const [showDlcOnly, setShowDlcOnly] = useState(false);

  useEffect(() => { setDiscovered(loadDiscovered()); }, []);

  const toggleDiscovered = (id: string) => {
    setDiscovered(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      saveDiscovered(next);
      return next;
    });
  };

  const filtered = useMemo(() => ITEMS.filter(item => {
    if (activeCategory !== "all" && item.category !== activeCategory) return false;
    const q = search.toLowerCase();
    if (q && !item.name.toLowerCase().includes(q) && !item.description.toLowerCase().includes(q)) return false;
    if (filterMode === "found" && !discovered.has(item.id)) return false;
    if (filterMode === "missing" && discovered.has(item.id)) return false;
    if (showLegendaryOnly && !item.legendary) return false;
    if (showDlcOnly && !item.dlc) return false;
    return true;
  }), [activeCategory, search, filterMode, discovered, showLegendaryOnly, showDlcOnly]);

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg-dark)" }}>
      {/* Header */}
      <header style={{ borderBottom: "1px solid var(--border)", background: "rgba(10,8,6,0.97)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(8px)" }}>
        <div style={{ height: 2, background: "linear-gradient(90deg, transparent, var(--gold-dark), var(--gold), var(--gold-dark), transparent)" }} />
        <div style={{ maxWidth: 1400, margin: "0 auto", padding: "0 24px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 0 12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div style={{ fontSize: 28, lineHeight: 1 }}>⚔️</div>
              <div>
                <h1 className="font-cinzel gold-gradient" style={{ fontSize: "1.1rem", fontWeight: 700, letterSpacing: "0.15em" }}>ELDEN RING</h1>
                <div style={{ fontSize: "0.62rem", color: "var(--text-muted)", letterSpacing: "0.2em", textTransform: "uppercase" }}>Tarnished's Compendium</div>
              </div>
            </div>
            <div style={{ position: "relative", flex: "0 1 360px" }}>
              <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "var(--text-muted)", fontSize: 13 }}>⌕</span>
              <input className="search-input" type="text" placeholder="Search items..." value={search}
                onChange={e => setSearch(e.target.value)}
                style={{ width: "100%", padding: "8px 12px 8px 32px", fontSize: "0.83rem" }} />
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textAlign: "right" }}>
              <span style={{ color: "var(--gold)" }}>{discovered.size}</span><span> / {ITEMS.length} discovered</span>
            </div>
          </div>
          {/* Category tabs */}
          <div style={{ display: "flex", overflowX: "auto", scrollbarWidth: "none" }}>
            <button className={`tab-btn ${activeCategory === "all" ? "active" : ""}`} onClick={() => setActiveCategory("all")}>All Items</button>
            {CATEGORIES.map(cat => (
              <button key={cat.id} className={`tab-btn ${activeCategory === cat.id ? "active" : ""}`} onClick={() => setActiveCategory(cat.id)}>
                {cat.icon} {cat.label}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Main */}
      <main style={{ maxWidth: 1400, margin: "0 auto", padding: "28px 24px" }}>
        <ProgressSection discovered={discovered} />

        {/* Filters */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
          {(["all", "found", "missing"] as const).map(f => (
            <button key={f} className={`filter-btn ${filterMode === f ? "active" : ""}`} onClick={() => setFilterMode(f)}>
              {f === "all" ? "All" : f === "found" ? "✓ Found" : "◯ Missing"}
            </button>
          ))}
          <div style={{ width: 1, height: 20, background: "var(--border)" }} />
          <button className={`filter-btn ${showLegendaryOnly ? "active" : ""}`} onClick={() => setShowLegendaryOnly(v => !v)}>★ Legendary</button>
          <button className={`filter-btn ${showDlcOnly ? "active" : ""}`} onClick={() => setShowDlcOnly(v => !v)}>◈ DLC Only</button>
          <div style={{ marginLeft: "auto", fontSize: "0.75rem", color: "var(--text-muted)" }}>{filtered.length} items</div>
        </div>

        {/* Grid */}
        {filtered.length === 0 ? (
          <div style={{ textAlign: "center", padding: "80px 0", color: "var(--text-muted)" }}>
            <div style={{ fontSize: 40, marginBottom: 16 }}>🕯️</div>
            <div className="font-cinzel" style={{ fontSize: "1rem", letterSpacing: "0.1em" }}>No items found</div>
            <div style={{ fontSize: "0.8rem", marginTop: 8 }}>Try adjusting your filters</div>
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 8 }}>
            {filtered.map(item => (
              <ItemCard key={item.id} item={item} discovered={discovered.has(item.id)} onClick={() => setSelectedItem(item)} />
            ))}
          </div>
        )}
      </main>

      <footer style={{ borderTop: "1px solid var(--border)", padding: "20px 24px", textAlign: "center", color: "var(--text-muted)", fontSize: "0.72rem", letterSpacing: "0.08em" }}>
        <div style={{ height: 1, background: "linear-gradient(90deg, transparent, var(--border), transparent)", marginBottom: 16 }} />
        ELDEN RING COMPANION · Tarnished's Compendium · Fan-made tracker · Not affiliated with FromSoftware or Bandai Namco
      </footer>

      {selectedItem && (
        <ItemModal item={selectedItem} discovered={discovered.has(selectedItem.id)}
          onClose={() => setSelectedItem(null)}
          onToggle={() => toggleDiscovered(selectedItem.id)} />
      )}
    </div>
  );
}
