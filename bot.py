import logging
import os
from telegram.ext import Application, CommandHandler
from database import Database
from handlers.info import start_handler, help_handler, profile_handler
from handlers.fishing import fishing_handler
from handlers.inventory import bag_handler
from handlers.shop import sell_handler, shop_handler

# 1. Konfigurasi Logging agar aktivitas bot terlihat di Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. Ambil Token Bot dari Environment Variables Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # 3. Inisialisasi Database
    db = Database()
    
    # 4. Membangun Aplikasi Bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 5. Menyimpan database ke bot_data agar bisa diakses di semua file handlers
    app.bot_data['db'] = db

    # 6. DAFTAR SEMUA PERINTAH (HANDLERS)
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    app.add_handler(CommandHandler("fishing", fishing_handler))
    app.add_handler(CommandHandler("bag", bag_handler))
    app.add_handler(CommandHandler("jual", sell_handler))
    app.add_handler(CommandHandler("shop", shop_handler))

    # 7. Pesan Start di Console
    print("---------------------------------------")
    print("🎣 Fishing Bot World v2.0 is RUNNING!")
    print("Fitur Aktif: Start, Help, Profil, Fishing, Bag, Jual, Shop")
    print("---------------------------------------")
    
    # 8. Jalankan Bot
    app.run_polling()

if __name__ == "__main__":
    main()
