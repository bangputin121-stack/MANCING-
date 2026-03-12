import logging
import os
from telegram.ext import Application, CommandHandler
from database import Database
from handlers.info import start_handler, help_handler
from handlers.fishing import fishing_handler

# 1. Konfigurasi Logging (Biar muncul di Deploy Logs Railway)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. Ambil Token dari Variables Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # 3. Inisialisasi Database
    db = Database()
    
    # 4. Bangun Aplikasi Bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 5. Simpan Database ke dalam Bot Data (Biar bisa diakses semua handler)
    app.bot_data['db'] = db

    # 6. DAFTAR PERINTAH (HANDLERS)
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("fishing", fishing_handler))

    # 7. Nyalakan Mesin!
    print("---------------------------------------")
    print("🎣 Fishing Bot World v2.0 is RUNNING!")
    print("---------------------------------------")
    
    app.run_polling()

if __name__ == "__main__":
    main()
