import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
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

    # LOGIKA XP & EVENT
    base_xp = random.randint(15, 30)
    is_event = context.bot_data.get('event_status', False)
    xp_gain = base_xp * 2 if is_event else base_xp
    
    current_xp = player.get('xp', 0) + xp_gain
    lvl = player.get('level', 1)
    target = lvl * 100
    
    msg_lvl = ""
    if current_xp >= target:
        lvl += 1
        current_xp = 0
        msg_lvl = f"\n🎊 **LEVEL UP ke {lvl}!**"

    # Simpan
    player.update({"inventory": player.get('inventory', []) + [dapat], "last_fishing": current_time, "xp": current_xp, "level": lvl})
    db.update_player(user_id, player)
    
    status_event = " [EVENT 2x XP]" if is_event else ""
    await update.message.reply_text(f"🎣 Pakai **{nama_joran}**\n✨ Dapat: **{dapat}** (+{xp_gain} XP){status_event}{msg_lvl}")
