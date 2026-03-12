import logging
import os
from telegram.ext import Application, CommandHandler
from database import Database
from handlers.info import start_handler, help_handler, profile_handler
from handlers.fishing import fishing_handler
from handlers.inventory import bag_handler
from handlers.shop import sell_handler, shop_handler, daily_handler

# 1. Konfigurasi Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. Ambil Token Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # 3. Inisialisasi Database
    db = Database()
    
    # 4. Membangun Aplikasi Bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 5. Simpan database ke bot_data
    app.bot_data['db'] = db

    # 6. DAFTAR SEMUA PERINTAH (HANDLERS)
    # Fitur Informasi & Profil
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    
    # Fitur Utama Game
    app.add_handler(CommandHandler("fishing", fishing_handler))
    app.add_handler(CommandHandler("bag", bag_handler))
    
    # Fitur Ekonomi & Hadiah
    app.add_handler(CommandHandler("jual", sell_handler))
    app.add_handler(CommandHandler("shop", shop_handler))
    app.add_handler(CommandHandler("daily", daily_handler))

    # 7. Pesan Log di Console Railway
    print("---------------------------------------")
    print("🎣 Fishing Bot World v2.5 is RUNNING!")
    print("Fitur Lengkap: Profil, Fishing, Shop, Daily")
    print("---------------------------------------")
    
    # 8. Jalankan Bot
    app.run_polling()

if __name__ == "__main__":
    main()
