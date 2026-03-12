import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISHING_RODS, BAITS, FISH_DATA

# 🛒 1. TOKO JORAN & UMPAN
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

# 💰 2. JUAL IKAN
async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    inventory = player.get('inventory', [])

    if not inventory:
        await update.message.reply_text("🎒 Tas kamu kosong, belum ada ikan buat dijual.")
        return

    total_hasil = 0
    for ikan in inventory:
        total_hasil += FISH_DATA.get(ikan, {}).get('price', 5)

    player['balance'] += total_hasil
    player['inventory'] = [] # Kosongkan tas
    db.update_player(user_id, player)

    await update.message.reply_text(f"💰 Semua ikan terjual! Kamu dapat **{total_hasil} koin**.")

# 🎁 3. HADIAH HARIAN
async def daily_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    current_time = time.time()
    last_daily = player.get('last_daily', 0)

    # Cooldown 24 jam (86400 detik)
    if current_time - last_daily < 86400:
        sisa_detik = int(86400 - (current_time - last_daily))
        jam = sisa_detik // 3600
        menit = (sisa_detik % 3600) // 60
        await update.message.reply_text(f"⏳ Kamu sudah ambil hadiah hari ini. Balik lagi dalam {jam} jam {menit} menit.")
        return

    bonus = 500
    player['balance'] += bonus
    player['last_daily'] = current_time
    db.update_player(user_id, player)

    await update.message.reply_text(f"🎁 Hadiah harian diklaim! Kamu dapat **{bonus} koin**.")
