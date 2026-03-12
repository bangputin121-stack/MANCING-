import logging
import os
from telegram.ext import Application, CommandHandler
from database import Database
from handlers.info import start_handler, help_handler

# Aktifkan logging agar kita tahu kalau ada error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token kamu (Nanti diisi di Railway Environment Variable)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # Inisialisasi Database
    db = Database()
    
    # Bangun Aplikasi
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Simpan DB di bot_data agar bisa diakses di handler mana pun
    app.bot_data['db'] = db

    # Daftar Perintah (Handlers)
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))

    print("🎣 Fishing Bot World v2.0 is RUNNING!")
    app.run_polling()

if __name__ == "__main__":
    main()
