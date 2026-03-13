import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database import get_user_data, update_user_data

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # AMBIL DATA ASLI DARI DATABASE
    user_data = get_user_data(user_id)
    joran_sekarang = user_data['joran']
    umpan_sekarang = user_data['umpan']

    # Logika Ikan
    ikan_list = [
        {"nama": "Udang", "emoji": "🦐", "min_berat": 0.1, "max_berat": 0.5},
        {"nama": "Ikan Mas", "emoji": "🐟", "min_berat": 1.2, "max_berat": 3.5},
        {"nama": "Nila", "emoji": "🐟", "min_berat": 0.5, "max_berat": 1.5}
    ]
    
    ikan = random.choice(ikan_list)
    berat = round(random.uniform(ikan["min_berat"], ikan["max_berat"]), 2)
    nilai_dapat = int(berat * 100)

    # UPDATE KOIN USER DI DATABASE
    new_balance = user_data['balance'] + nilai_dapat
    update_user_data(user_id, "balance", new_balance)

    # TAMPILAN
    caption_text = (
        f"{ikan['emoji']} ═════════════════\n"
        f"⚪️ {ikan['nama']}\n"
        f"├ Berat: {berat}kg\n"
        f"└ Nilai: 🪙 {nilai_dapat} Coins\n"
        f"═════════════════ {ikan['emoji']}\n\n"
        f"⚙️ Peralatan:\n"
        f"├ ☠️ {joran_sekarang}\n"
        f"└ 💫 {umpan_sekarang}\n\n"
        f"💰 Saldo Sekarang: {new_balance} Coins"
    )

    await update.message.reply_text(text=caption_text, parse_mode=ParseMode.MARKDOWN)
