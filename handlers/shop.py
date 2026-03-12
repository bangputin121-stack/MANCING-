from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISHING_RODS, BAITS

async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    args = context.args

    if not args:
        pesan = "🛒 **TOKO PERALATAN MANCING**\n\n"
        pesan += "🎣 **JORAN:**\n"
        for k, v in FISHING_RODS.items():
            if k != "Bambu": pesan += f"• {k}: {v['price']} koin\n"
        pesan += "\n🪱 **UMPAN (Isi 10):**\n"
        for k, v in BAITS.items():
            pesan += f"• {k}: {v['price']} koin\n"
        await update.message.reply_text(pesan + "\nBeli: `/shop [nama]`\nContoh: `/shop Cacing`")
        return

    item = " ".join(args).title()
    
    # Beli Joran
    if item in FISHING_RODS:
        price = FISHING_RODS[item]['price']
        if player.get('balance', 0) >= price:
            player['balance'] -= price
            player['rod'] = item
            db.update_player(user_id, player)
            await update.message.reply_text(f"✅ Berhasil beli Joran **{item}**!")
        else:
            await update.message.reply_text("❌ Koin tidak cukup!")
    
    # Beli Umpan
    elif item in BAITS:
        price = BAITS[item]['price']
        if player.get('balance', 0) >= price:
            player['balance'] -= price
            player['bait'] = player.get('bait', 0) + 10
            player['current_bait'] = item
            db.update_player(user_id, player)
            await update.message.reply_text(f"✅ Beli 10 **{item}** berhasil! Stok: {player['bait']}")
        else:
            await update.message.reply_text("❌ Koin tidak cukup!")
    else:
        await update.message.reply_text("❌ Barang tidak ada di toko.")

# (Tetap sertakan sell_handler dan daily_handler di bawahnya seperti biasa)
