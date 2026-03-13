import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from database import Database
from handlers.fishing import fishing_handler

# 1. Setting Log (Biar lo bisa liat error di Railway Log kalau ada masalah)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Inisialisasi Database
db = Database()

async def start(update, context):
    """Perintah /start buat nyapa member baru"""
    user = update.effective_user
    db.get_user(user.id) # Otomatis daftarin ke database
    await update.message.reply_text(
        f"Halo {user.first_name}! Selamat datang di Bot Mancing Mania. 🎣\n"
        "Gunakan perintah /mancing untuk mulai menangkap ikan!"
    )

def main():
    # 3. Ambil Token dari Environment Variable Railway
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN tidak ditemukan di Variable Railway!")
        return

    # 4. Bangun Aplikasi Bot
    app = ApplicationBuilder().token(TOKEN).build()

    # 5. Daftar Perintah (Handlers)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mancing", fishing_handler))

    # 6. Jalankan Bot
    print("🚀 BOT JALAN! Silakan tes /mancing di Telegram.")
    app.run_polling()

if __name__ == '__main__':
    main()
