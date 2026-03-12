from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📋 *DAFTAR FITUR FISHING WORLD*\n\n"
        "| Perintah | Fungsi |\n"
        "| :--- | :--- |\n"
        "| `/start` | 📩 Daftar Akun |\n"
        "| `/profil` | 👤 Informasi Pemain |\n"
        "| `/fishing` | 🎣 Mulai Memancing |\n"
        "| `/bag` | 🎒 Lihat Ikan di Tas |\n"
        "| `/shop` | 🛒 Beli Peralatan |\n"
        "| `/jual` | 💰 Jual Hasil Tangkapan |\n"
        "| `/leaderboard` | 🏆 Peringkat Pemain |\n"
        "| `/help` | ❓ Bantuan |\n\n"
        "💡 _Kumpulkan ikan langka dan upgrade joranmu!_"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = context.bot_data['db']
    db.get_player(user.id) # Pastikan user terdaftar
    
    await update.message.reply_text(
        f"👋 Halo *{user.first_name}*!\n\n"
        "Selamat datang di *Fishing World v2.0*.\n"
        "Gunakan perintah `/help` untuk melihat fitur lengkap.",
        parse_mode='Markdown'
    )
