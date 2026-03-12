import logging
import os
from telegram.ext import Application, CommandHandler
from database import Database

# Import Handlers dari folder handlers
from handlers.info import start_handler, help_handler, profile_handler
from handlers.fishing import fishing_handler
from handlers.inventory import bag_handler
from handlers.shop import sell_handler, shop_handler, daily_handler
from handlers.admin import add_coin_handler, gift_fish_handler, broadcast_handler

# 1. Konfigurasi Logging (Biar bisa pantau error di Railway Logs)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. Ambil Token Bot dari Environment Variable Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # 3. Inisialisasi Database
    db = Database()
    
    # 4. Membangun Aplikasi Bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 5. Simpan database ke bot_data agar bisa diakses di semua handler
    app.bot_data['db'] = db

    # ==========================================
    # 6. DAFTAR SEMUA PERINTAH (HANDLERS)
    # ==========================================
    
    # --- Menu Utama & Profil ---
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    
    # --- Fitur Game (Mancing & Tas) ---
    app.add_handler(CommandHandler("fishing", fishing_handler))
    app.add_handler(CommandHandler("bag", bag_handler))
    
    # --- Fitur Ekonomi (Jual, Toko, Hadiah) ---
    app.add_handler(CommandHandler("jual", sell_handler))
    app.add_handler(CommandHandler("shop", shop_handler))
    app.add_handler(CommandHandler("daily", daily_handler))

    # --- Fitur KHUSUS ADMIN ---
    app.add_handler(CommandHandler("addcoin", add_coin_handler))
    app.add_handler(CommandHandler("giftfish", gift_fish_handler))
    app.add_handler(CommandHandler("broadcast", broadcast_handler))

    # 7. Pesan Log di Console Railway saat Bot Aktif
    print("---------------------------------------")
    print("🎣 FISHING BOT GLOBAL v3.0 - STATUS: ONLINE")
    print("Admin Commands: Active")
    print("---------------------------------------")
    
    # 8. Jalankan Bot (Polling Mode)
    app.run_polling()

if __name__ == "__main__":
    main()
