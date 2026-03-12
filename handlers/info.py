from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = context.bot_data['db']
    
    # Daftarkan pemain ke database kalau belum ada
    db.get_player(user.id)
    
    pesan = (
        f"👋 *Halo {user.first_name}!*\n\n"
        "Selamat datang di *Fishing World RPG v2.0*.\n"
        "Gunakan perintah `/help` untuk melihat daftar fitur."
    )
    await update.message.reply_text(pesan, parse_mode='Markdown')

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tabel fitur sesuai permintaanmu
    help_text = (
        "📋 *DAFTAR FITUR FISHING RPG*\n\n"
        "| Perintah | Fungsi |\n"
        "| :--- | :--- |\n"
        "| `/start` | 📩 Daftar Akun |\n"
        "| `/profil` | 👤 Informasi Pemain |\n"
        "| `/fishing` | 🎣 Mulai Memancing |\n"
        "| `/bag` | 🎒 Lihat Ikan di Tas |\n"
        "| `/shop` | 🛒 Beli Peralatan |\n"
        "| `/jual` | 💰 Jual Ikan |\n"
        "| `/help` | ❓ Bantuan |\n\n"
        "💡 *Tips:* Kumpulkan koin untuk beli Joran yang lebih sakti!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')
