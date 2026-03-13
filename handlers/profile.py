from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database import Database

db = Database()

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    saldo = user_data.get('balance', 0)
    joran = user_data.get('joran', 'Bambu Biasa')
    umpan = user_data.get('umpan', 'Cacing')

    text = (
        f"👤 *PROFIL PEMANCING*\n"
        f"════════════════════\n"
        f"📝 Nama: {user.first_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"💰 Saldo: {saldo} Coins\n\n"
        f"🎣 *Peralatan Saat Ini:*\n"
        f"├ Joran: {joran}\n"
        f"└ Umpan: {umpan}\n"
        f"════════════════════"
    )
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
