import os
from telegram.ext import ApplicationBuilder, CommandHandler
from database import Database
from handlers.info import start_handler, help_handler, profile_handler
from handlers.fishing import fishing_handler
from handlers.shop import shop_handler, sell_handler, daily_handler
from handlers.admin import (
    add_coin_handler, gift_fish_handler, broadcast_handler, 
    reset_player_handler, event_handler, check_player_handler
)

def main():
    # Ambil Token dari Environment Variable Railway
    TOKEN = os.getenv("BOT_TOKEN")
    db = Database()

    app = ApplicationBuilder().token(TOKEN).build()
    
    # Simpan database di bot_data agar bisa diakses semua handler
    app.bot_data['db'] = db
    app.bot_data['event_status'] = False # Default event mati

    # --- REGISTER COMMANDS ---
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    app.add_handler(CommandHandler("fishing", fishing_handler))
    app.add_handler(CommandHandler("mancing", fishing_handler))
    app.add_handler(CommandHandler("shop", shop_handler))
    app.add_handler(CommandHandler("jual", sell_handler))
    app.add_handler(CommandHandler("daily", daily_handler))

    # --- ADMIN COMMANDS ---
    app.add_handler(CommandHandler("addcoin", add_coin_handler))
    app.add_handler(CommandHandler("giftfish", gift_fish_handler))
    app.add_handler(CommandHandler("bc", broadcast_handler))
    app.add_handler(CommandHandler("reset", reset_player_handler))
    app.add_handler(CommandHandler("event", event_handler))
    app.add_handler(CommandHandler("check", check_player_handler))

    print("🚀 BOT READY WITH ALL FEATURES!")
    app.run_polling()

if __name__ == '__main__':
    main()
