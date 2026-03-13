import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Data variasi ikan biar nggak bosen
    ikan_list = [
        {"nama": "Udang", "emoji": "🦐", "min_berat": 0.1, "max_berat": 0.5},
        {"nama": "Ikan Mas", "emoji": "🐟", "min_berat": 1.2, "max_berat": 3.5},
        {"nama": "Nila", "emoji": "🐟", "min_berat": 0.5, "max_berat": 1.5},
        {"nama": "Kepiting", "emoji": "🦀", "min_berat": 0.3, "max_berat": 0.8}
    ]
    
    # Acak ikan dan hitung berat/harga
    ikan = random.choice(ikan_list)
    berat = round(random.uniform(ikan["min_berat"], ikan["max_berat"]), 2)
    nilai = int(berat * 100) # Contoh: berat 0.24kg jadi 24 Coins
    
    # Susun tampilan persis seperti contoh lo
    caption_text = (
        f"{ikan['emoji']} ═════════════════\n"
        f"⚪️ {ikan['nama']}\n"
        f"├ Berat: {berat}kg\n"
        f"└ Nilai: 🪙 {nilai} Coins\n"
        f"═════════════════ {ikan['emoji']}\n\n"
        f"⚙️ Peralatan:\n"
        f"├ ☠️ JORAN LEGENDARIS\n"
        f"└ 💫 Umpan telur emas"
    )

    # Kirim pesan teks
    await update.message.reply_text(
        text=caption_text,
        parse_mode=ParseMode.MARKDOWN
    )
