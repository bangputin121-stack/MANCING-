import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from database import Database

# IMPORT HANDLERS (Pastikan nama file dan fungsinya sesuai di folder handlers)
from handlers.fishing import fishing_handler
# Buka tanda pagar (#) di bawah ini kalau filenya sudah ada:
# from handlers.shop import shop_handler 
# from handlers.profile import profile_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

db = Database()

async def start(update, context):
    user = update.effective_user
    db.get_user(user.id)
    await update.message.reply_text(
        f"Halo {user.first_name}! 🎣\n\n"
        "Perintah yang tersedia:\n"
        "/mancing - Mulai memancing\n"
        "/profil - Cek saldo & joran\n"
        "/shop - Toko peralatan"
    )

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # DAFTAR COMMAND DI SINI
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mancing", fishing_handler))
    
    # Tambahkan baris di bawah ini sesuai perintah yang lo mau aktifin:
    # app.add_handler(CommandHandler("shop", shop_handler))
    # app.add_handler(CommandHandler("profil", profile_handler))

    print("🚀 BOT JALAN! Semua perintah terdaftar.")
    app.run_polling()

if __name__ == '__main__':
    main()
