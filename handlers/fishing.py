import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. DATA IKAN
    ikan_list = [
        {"nama": "Udang", "emoji": "🦐", "min_berat": 0.1, "max_berat": 0.5},
        {"nama": "Ikan Mas", "emoji": "🐟", "min_berat": 1.2, "max_berat": 3.5},
        {"nama": "Kepiting", "emoji": "🦀", "min_berat": 0.3, "max_berat": 0.8}
    ]
    
    # 2. DATA PERALATAN (Nanti ini diambil dari Database/Profile User)
    joran_inventory = ["Bambu Biasa", "Joran Carbon", "☠️ JORAN LEGENDARIS", "Joran Pro"]
    umpan_inventory = ["Cacing", "Pelet", "💫 Umpan telur emas", "Udang Kecil"]

    # Simulasi: Bot milih joran/umpan yang "lagi dipakai" secara acak
    # (Nanti kalau database sudah ada, ini diganti jadi: joran_dipakai = user_data['joran'])
    joran_sekarang = random.choice(joran_inventory)
    umpan_sekarang = random.choice(umpan_inventory)

    # 3. LOGIKA TANGKAPAN
    ikan = random.choice(ikan_list)
    berat = round(random.uniform(ikan["min_berat"], ikan["max_berat"]), 2)
    nilai = int(berat * 100)

    # 4. TAMPILAN SESUAI PERALATAN USER
    caption_text = (
        f"{ikan['emoji']} ═════════════════\n"
        f"⚪️ {ikan['nama']}\n"
        f"├ Berat: {berat}kg\n"
        f"└ Nilai: 🪙 {nilai} Coins\n"
        f"═════════════════ {ikan['emoji']}\n\n"
        f"⚙️ Peralatan:\n"
        f"├ {joran_sekarang}\n"
        f"└ {umpan_sekarang}"
    )

    await update.message.reply_text(
        text=caption_text,
        parse_mode=ParseMode.MARKDOWN
    )
