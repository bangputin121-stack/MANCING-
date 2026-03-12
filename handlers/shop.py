import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISHING_RODS, BAITS, FISH_DATA

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
        await update.message.reply_text(pesan + "\nBeli: `/shop [nama]`\nContoh: `/shop Cacing`", parse_mode="Markdown")
        return

    item = " ".join(args).title()
    
    if item in FISHING_RODS:
        price = FISHING_RODS[item]['price']
        if player.get('balance', 0) >= price:
            player['balance'] -= price
            player['rod'] = item
            db.update_player(user_id, player)
            await update.message.reply_text(f"✅ Berhasil beli Joran **{item}**!")
        else:
            await update.message.reply_text("❌ Koin tidak cukup!")
    
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
        await update.message.reply_text("❌ Barang tidak ada.")

async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    inventory = player.get('inventory', [])

    if not inventory:
        await update.message.reply_text("🎒 Tas kamu kosong.")
        return

    total = sum(FISH_DATA.get(ikan, {}).get('price', 5) for ikan in inventory)
    player['balance'] += total
    player['inventory'] = []
    db.update_player(user_id, player)
    await update.message.reply_text(f"💰 Ikan terjual! Dapat **{total} koin**.")

async def daily_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    now = time.time()

    if now - player.get('last_daily', 0) < 86400:
        await update.message.reply_text("⏳ Hadiah harian sudah diambil.")
        return

    player['balance'] += 500
    player['last_daily'] = now
    db.update_player(user_id, player)
    await update.message.reply_text("🎁 Kamu dapat 500 koin harian!")
