import os
from telegram.ext import ApplicationBuilder, CommandHandler
from database import Database
from handlers.fishing import fishing_handler
from handlers.profile import profile_handler
from handlers.shop import shop_handler

db = Database()

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    # Daftar Perintah
    app.add_handler(CommandHandler("start", profile_handler)) # Start langsung liat profil
    app.add_handler(CommandHandler("mancing", fishing_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    app.add_handler(CommandHandler("shop", shop_handler))
    app.add_handler(CommandHandler("buy", shop_handler)) # Biar bisa /buy [nomor]

    print("🚀 BOT JALAN! Semua fitur (Mancing, Profil, Toko) Aktif.")
    app.run_polling()

if __name__ == '__main__':
    main()
