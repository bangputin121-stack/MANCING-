import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database import Database

# Panggil database
db = Database()

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    
    # Ambil peralatan asli dari database user
    joran_user = user_data.get('joran', 'Bambu Biasa')
    umpan_user = user_data.get('umpan', 'Cacing')

    # Daftar Ikan
    ikan_list = [
        {"nama": "Udang", "emoji": "🦐", "min": 0.1, "max": 0.5},
        {"nama": "Ikan Mas", "emoji": "🐟", "min": 1.2, "max": 3.5},
        {"nama": "Nila", "emoji": "🐟", "min": 0.5, "max": 1.5}
    ]
    
    ikan = random.choice(ikan_list)
    berat = round(random.uniform(ikan["min"], ikan["max"]), 2)
    koin_dapat = int(berat * 100)

    # Simpan hasil ke koin user
    new_balance = user_data['balance'] + koin_dapat
    db.update_user(user_id, "balance", new_balance)

    # Tampilan Detail (Tinggal Tempel)
    caption_text = (
        f"{ikan['emoji']} ═════════════════\n"
        f"⚪️ {ikan['nama']}\n"
        f"├ Berat: {berat}kg\n"
        f"└ Nilai: 🪙 {koin_dapat} Coins\n"
        f"═════════════════ {ikan['emoji']}\n\n"
        f"⚙️ Peralatan:\n"
        f"├ {joran_user}\n"
        f"└ {umpan_user}\n\n"
        f"💰 Saldo: {new_balance} Coins"
    )

    await update.message.reply_text(text=caption_text, parse_mode=ParseMode.MARKDOWN)
