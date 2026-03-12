import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

# ============================================================
#  DATA IKAN — rarity, berat, xp, emoji
# ============================================================
FISH_CATALOG = {
    "Teri": {
        "rarity": "Common", "emoji": "🐟",
        "weight_range": (0.1, 0.5), "xp": 5,
        "base_chance": 40
    },
    "Lele": {
        "rarity": "Common", "emoji": "🐠",
        "weight_range": (0.5, 2.0), "xp": 10,
        "base_chance": 25
    },
    "Nila": {
        "rarity": "Uncommon", "emoji": "🐡",
        "weight_range": (1.0, 4.0), "xp": 25,
        "base_chance": 15
    },
    "Kakap": {
        "rarity": "Rare", "emoji": "🎣",
        "weight_range": (2.0, 8.0), "xp": 60,
        "base_chance": 10
    },
    "Tuna": {
        "rarity": "Epic", "emoji": "🦈",
        "weight_range": (5.0, 20.0), "xp": 150,
        "base_chance": 6
    },
    "Paus": {
        "rarity": "Legendary", "emoji": "🐋",
        "weight_range": (50.0, 200.0), "xp": 500,
        "base_chance": 3
    },
    "Nemo": {
        "rarity": "Mythic", "emoji": "🌟",
        "weight_range": (0.3, 1.5), "xp": 999,
        "base_chance": 1
    },
}

# ============================================================
#  DATA JORAN (ROD)
# ============================================================
ROD_DATA = {
    "Bambu":      {"bonus": 0,  "emoji": "🎋"},
    "Fiberglass": {"bonus": 3,  "emoji": "🟫"},
    "Carbon":     {"bonus": 7,  "emoji": "⚫"},
    "Pro Angler": {"bonus": 12, "emoji": "🔵"},
    "Legendaris": {"bonus": 18, "emoji": "🌟"},
    "Dewa Laut":  {"bonus": 25, "emoji": "🔱"},
}

# ============================================================
#  DATA UMPAN (BAIT)
# ============================================================
BAIT_DATA = {
    "Cacing":       {"bonus": 0,  "emoji": "🪱"},
    "Udang":        {"bonus": 4,  "emoji": "🦐"},
    "Ikan Kecil":   {"bonus": 8,  "emoji": "🐟"},
    "Umpan Emas":   {"bonus": 14, "emoji": "✨"},
    "Umpan Mistis": {"bonus": 20, "emoji": "🔮"},
}

# ============================================================
#  KONFIGURASI FISHING BERDASARKAN ROLE
# ============================================================
FISHING_CONFIG = {
    "member": {
        "duration": 120,       # 2 menit
        "interval_min": 5,
        "interval_max": 8,
        "catch_min": 10,
        "catch_max": 20,
        "label": "Member",
        "emoji": "👤",
    },
    "vip": {
        "duration": 300,       # 5 menit
        "interval_min": 4,
        "interval_max": 6,
        "catch_min": 20,
        "catch_max": 40,
        "label": "VIP",
        "emoji": "💎",
    },
    "admin": {
        "duration": 300,       # 5 menit
        "interval_min": 2,
        "interval_max": 2,
        "catch_min": 60,
        "catch_max": 60,
        "label": "Admin",
        "emoji": "👑",
    },
}

# Rarity badge display
RARITY_BADGE = {
    "Common":    "◻️ COMMON",
    "Uncommon":  "🟩 UNCOMMON",
    "Rare":      "🟦 RARE",
    "Epic":      "🟪 EPIC",
    "Legendary": "🟨 LEGENDARY",
    "Mythic":    "🔴 MYTHIC",
}

# ============================================================
#  HELPER: Tentukan role player
# ============================================================
def get_player_role(player: dict) -> str:
    role = str(player.get("role", "member")).lower()
    return role if role in FISHING_CONFIG else "member"

# ============================================================
#  HELPER: Pilih ikan — luck hanya membantu sedikit ke rarity tinggi
# ============================================================
def pick_fish(total_luck: int) -> str:
    weights = {name: data["base_chance"] for name, data in FISH_CATALOG.items()}

    # Cap luck agar rarity tinggi tetap sangat sulit
    luck_factor = min(total_luck, 30)

    weights["Teri"]  = max(5.0, weights["Teri"]  - luck_factor * 0.60)
    weights["Lele"]  = max(5.0, weights["Lele"]  - luck_factor * 0.30)
    weights["Nila"]  = weights["Nila"]  + luck_factor * 0.15
    weights["Kakap"] = weights["Kakap"] + luck_factor * 0.08
    weights["Tuna"]  = weights["Tuna"]  + luck_factor * 0.04
    weights["Paus"]  = weights["Paus"]  + luck_factor * 0.015
    weights["Nemo"]  = weights["Nemo"]  + luck_factor * 0.005

    fish_names   = list(weights.keys())
    fish_weights = [weights[n] for n in fish_names]
    return random.choices(fish_names, weights=fish_weights, k=1)[0]

# ============================================================
#  HELPER: Format notifikasi tangkapan
# ============================================================
def format_catch_msg(fish_name: str, bait_name: str, rod_name: str,
                     xp_gain: int, is_event: bool, catch_number: int) -> str:
    fish      = FISH_CATALOG[fish_name]
    weight    = round(random.uniform(*fish["weight_range"]), 2)
    badge     = RARITY_BADGE[fish["rarity"]]
    bait_info = BAIT_DATA.get(bait_name,  {"emoji": "🪱"})
    rod_info  = ROD_DATA.get(rod_name,   {"emoji": "🎋"})
    event_tag = " 🎉 ×2 XP" if is_event else ""

    return (
        f"┌─────────────────────────\n"
        f"│ 🎣 Tangkapan #{catch_number}\n"
        f"├─────────────────────────\n"
        f"│ {fish['emoji']}  Nama   : {fish_name}\n"
        f"│ {badge}\n"
        f"│ ⚖️  Berat  : {weight} kg\n"
        f"│ 🪱 Umpan  : {bait_info['emoji']} {bait_name}\n"
        f"│ 🎋 Joran  : {rod_info['emoji']} {rod_name}\n"
        f"│ ✨ XP     : +{xp_gain}{event_tag}\n"
        f"└─────────────────────────"
    )

# ============================================================
#  HELPER: Format panel equipment
# ============================================================
def format_equipment_panel(player: dict, cfg: dict) -> str:
    rod   = player.get("rod",   "Bambu")
    bait  = player.get("bait",  "Cacing")
    boat  = player.get("boat",  "Tidak ada")
    boost = player.get("boost", "Tidak ada")

    rod_emoji  = ROD_DATA.get(rod,   {"emoji": "🎋"})["emoji"]
    bait_emoji = BAIT_DATA.get(bait, {"emoji": "🪱"})["emoji"]

    duration_str = f"{cfg['duration'] // 60} menit"
    interval_str = (
        f"{cfg['interval_min']} detik"
        if cfg["interval_min"] == cfg["interval_max"]
        else f"{cfg['interval_min']}-{cfg['interval_max']} detik"
    )
    catch_str = (
        f"{cfg['catch_min']} ikan"
        if cfg["catch_min"] == cfg["catch_max"]
        else f"{cfg['catch_min']}-{cfg['catch_max']} ikan"
    )
    role_badge = f"{cfg['emoji']} {cfg['label']}"

    return (
        f"╔══════════════════════════╗\n"
        f"║   🌊 SESI MEMANCING 🌊   ║\n"
        f"╠══════════════════════════╣\n"
        f"║ 🏷  Role    : {role_badge:<12}║\n"
        f"║ ⏱  Durasi  : {duration_str:<12}║\n"
        f"║ 🔄 Interval: {interval_str:<12}║\n"
        f"║ 🎯 Kuota   : {catch_str:<12}║\n"
        f"╠══════════════════════════╣\n"
        f"║       🎒 EQUIPMENT        ║\n"
        f"╠══════════════════════════╣\n"
        f"║ 🎋 Joran  : {rod_emoji} {rod:<12}║\n"
        f"║ 🪱 Umpan  : {bait_emoji} {bait:<12}║\n"
        f"║ ⛵ Kapal  : {boat:<14}║\n"
        f"║ ⚡ Boost  : {boost:<14}║\n"
        f"╚══════════════════════════╝"
    )

# ============================================================
#  MAIN HANDLER: /fishing
# ============================================================
async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    username = update.effective_user.first_name or "Pemancing"
    db       = context.bot_data["db"]
    player   = db.get_player(user_id)

    # --- Validasi role & config ---
    role = get_player_role(player)
    cfg  = FISHING_CONFIG[role]

    # --- Cek cooldown ---
    current_time = time.time()
    last_fishing = player.get("last_fishing", 0)
    cooldown     = cfg["duration"] + 30  # sesi + 30 detik istirahat

    if current_time - last_fishing < cooldown:
        sisa      = int(cooldown - (current_time - last_fishing))
        menit     = sisa // 60
        detik     = sisa % 60
        waktu_str = f"{menit}m {detik}s" if menit else f"{detik}s"
        await update.message.reply_text(
            f"⏳ *Kamu masih kelelahan!*\n"
            f"Tunggu **{waktu_str}** lagi sebelum memancing.\n"
            f"_Gunakan waktu ini untuk cek inventaris!_",
            parse_mode="Markdown"
        )
        return

    # --- Data equipment ---
    rod_name   = player.get("rod",  "Bambu")
    bait_name  = player.get("bait", "Cacing")
    rod_bonus  = ROD_DATA.get(rod_name,   {"bonus": 0})["bonus"]
    bait_bonus = BAIT_DATA.get(bait_name, {"bonus": 0}).get("bonus", 0)
    is_event   = context.bot_data.get("event_status", False)

    # --- Tampilkan panel equipment ---
    panel = format_equipment_panel(player, cfg)
    await update.message.reply_text(
        f"*Hei, {username}\\!* Bersiap memancing\\.\\.\\. 🎣\n\n"
        f"```\n{panel}\n```",
        parse_mode="MarkdownV2"
    )
    await asyncio.sleep(2)

    # --- Tentukan total tangkapan sesi ini ---
    total_target = random.randint(cfg["catch_min"], cfg["catch_max"])
    sesi_start   = time.time()
    total_caught = 0
    total_xp     = 0
    tangkapan    = []

    await update.message.reply_text(
        f"🌊 *Sesi memancing dimulai\\!*\n"
        f"🎯 Target: **{total_target} ikan**\n"
        f"⏱️ Durasi: **{cfg['duration'] // 60} menit**\n\n"
        f"_Menunggu ikan menggigit umpan\\.\\.\\._",
        parse_mode="MarkdownV2"
    )

    # --- Loop memancing ---
    while total_caught < total_target:
        elapsed = time.time() - sesi_start
        if elapsed >= cfg["duration"]:
            break

        interval = random.randint(cfg["interval_min"], cfg["interval_max"])
        await asyncio.sleep(interval)

        # Pilih ikan
        luck      = rod_bonus + bait_bonus
        fish_name = pick_fish(luck)
        fish_data = FISH_CATALOG[fish_name]

        # Hitung XP & level up
        base_xp    = fish_data["xp"]
        xp_gain    = base_xp * 2 if is_event else base_xp
        current_xp = player.get("xp", 0) + xp_gain
        lvl        = player.get("level", 1)
        target_xp  = lvl * 100
        msg_lvl    = ""
        if current_xp >= target_xp:
            lvl        += 1
            current_xp  = current_xp - target_xp
            msg_lvl     = f"\n\n🎊 *LEVEL UP\\!* Kamu sekarang Level **{lvl}**\\! 🎉"

        total_caught += 1
        total_xp     += xp_gain
        tangkapan.append(fish_name)

        # Update player in-memory
        player["xp"]        = current_xp
        player["level"]     = lvl
        player["inventory"] = player.get("inventory", []) + [fish_name]

        # Kirim notif tangkapan
        catch_text = format_catch_msg(
            fish_name, bait_name, rod_name, xp_gain, is_event, total_caught
        )
        await update.message.reply_text(
            f"```\n{catch_text}\n```{msg_lvl}",
            parse_mode="MarkdownV2"
        )

    # --- Simpan ke database ---
    player["last_fishing"] = time.time()
    db.update_player(user_id, player)

    # --- Rekap akhir sesi ---
    fish_count = {}
    for f in tangkapan:
        fish_count[f] = fish_count.get(f, 0) + 1

    rekap_lines = ["📊 *Rekap Sesi Memancing*\n"]
    # Sort dari rarity tertinggi
    sorted_fish = sorted(
        fish_count.items(),
        key=lambda x: FISH_CATALOG[x[0]]["xp"],
        reverse=True
    )
    for fname, count in sorted_fish:
        fd    = FISH_CATALOG[fname]
        badge = RARITY_BADGE[fd["rarity"]]
        rekap_lines.append(f"  {fd['emoji']} {fname} \\| {badge} \\| ×{count}")

    rekap_lines.append(f"\n🎣 Total Ikan    : *{total_caught}*")
    rekap_lines.append(f"✨ Total XP      : *\\+{total_xp}*")
    rekap_lines.append(f"📈 Level         : *{player.get('level', 1)}*")
    rekap_lines.append(f"🔢 XP Progress   : *{player.get('xp', 0)} / {player.get('level', 1) * 100}*")

    if is_event:
        rekap_lines.append(f"\n🎉 _Event aktif — semua XP ×2\\!_")

    await update.message.reply_text(
        "\n".join(rekap_lines),
        parse_mode="MarkdownV2"
