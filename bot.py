import os
from telegram.ext import Application, CommandHandler
from database import load_data, save_data
from handlers.info import start_handler, help_handler, profile_handler
from handlers.fishing import fishing_handler
from handlers.inventory import bag_handler
from handlers.shop import sell_handler, shop_handler, daily_handler
from handlers.admin import *

def main():
    db = Database()
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.bot_data['db'] = db

    # Handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("profil", profile_handler))
    app.add_handler(CommandHandler("fishing", fishing_handler))
    app.add_handler(CommandHandler("bag", bag_handler))
    app.add_handler(CommandHandler("jual", sell_handler))
    app.add_handler(CommandHandler("shop", shop_handler))
    app.add_handler(CommandHandler("daily", daily_handler))
    
    # Admin Handlers
    app.add_handler(CommandHandler("addcoin", add_coin_handler))
    app.add_handler(CommandHandler("giftfish", gift_fish_handler))
    app.add_handler(CommandHandler("broadcast", broadcast_handler))
    app.add_handler(CommandHandler("reset_player", reset_player_handler))
    app.add_handler(CommandHandler("event", event_handler))
    app.add_handler(CommandHandler("check", check_player_handler))

    print("🚀 BOT READY WITH ADMIN FEATURES!")
    app.run_polling()

if __name__ == "__main__":
    main()
