FISHING_RODS = {
    "Bambu"       : {"price":       0, "luck":   0},   # Starter gratis
    "Kayu"        : {"price":    1_000, "luck":   8},
    "Besi"        : {"price":    5_000, "luck":  18},
    "Karbon"      : {"price":   15_000, "luck":  30},
    "Emas"        : {"price":   40_000, "luck":  45},
    "Titanium"    : {"price":  100_000, "luck":  62},
    "Berlian"     : {"price":  250_000, "luck":  80},
    "Kristal"     : {"price":  600_000, "luck": 100},
    "Mitril"      : {"price":1_500_000, "luck": 125},
    "Legendaris"  : {"price":5_000_000, "luck": 160},
}

FISH_DATA = {
    # ── Ikan Kecil ──────────────────────────
    "Teri"        : {"price_per_kg":    500, "weight_kg": 0.05,  "rarity": "common"},
    "Wader"       : {"price_per_kg":  1_000, "weight_kg": 0.1,   "rarity": "common"},
    "Lele"        : {"price_per_kg":  2_500, "weight_kg": 0.3,   "rarity": "common"},
    "Nila"        : {"price_per_kg":  4_000, "weight_kg": 0.5,   "rarity": "common"},

    # ── Ikan Sedang ─────────────────────────
    "Mas"         : {"price_per_kg":  7_000, "weight_kg": 1.0,   "rarity": "uncommon"},
    "Gurame"      : {"price_per_kg": 12_000, "weight_kg": 1.5,   "rarity": "uncommon"},
    "Bawal"       : {"price_per_kg": 18_000, "weight_kg": 2.0,   "rarity": "uncommon"},
    "Kakap"       : {"price_per_kg": 25_000, "weight_kg": 3.0,   "rarity": "rare"},

    # ── Ikan Besar ──────────────────────────
    "Tuna"        : {"price_per_kg": 45_000, "weight_kg": 30.0,  "rarity": "rare"},
    "Marlin"      : {"price_per_kg": 65_000, "weight_kg": 80.0,  "rarity": "epic"},
    "Hiu"         : {"price_per_kg": 90_000, "weight_kg": 150.0, "rarity": "epic"},
    "Nemo"        : {"price_per_kg":150_000, "weight_kg": 0.2,   "rarity": "epic"},   # Langka & unik

    # ── Ikan Raksasa / Legendaris ────────────
    "Paus Biru"   : {"price_per_kg":300_000, "weight_kg": 500.0, "rarity": "legendary"},
    "Kraken"      : {"price_per_kg":999_999, "weight_kg":1000.0, "rarity": "mythic"},
}

# DAFTAR UMPAN BARU
BAITS = {
    "Roti"        : {"price":    30, "luck":  3},   # Umpan paling murah
    "Cacing"      : {"price":    80, "luck":  8},
    "Pelet"       : {"price":   200, "luck": 15},
    "Jangkrik"    : {"price":   350, "luck": 22},
    "Udang"       : {"price":   600, "luck": 32},
    "Cumi"        : {"price": 1_200, "luck": 45},
    "Ikan Kecil"  : {"price": 2_500, "luck": 60},
    "Telur Emas"  : {"price": 8_000, "luck": 85},
    "Umpan Ajaib" : {"price":25_000, "luck":120},   # Umpan terbaik
}
