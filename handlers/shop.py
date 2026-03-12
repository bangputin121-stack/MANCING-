import time
import random
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

# --- FITUR JUAL ---
async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    inventory = player.get('inventory', [])
    if not inventory:
        await update.message.reply_text("❌ Tas kamu kosong!")
        return
    total = sum(FISH_DATA.get(item, {}).get('price', 0) for item in inventory)
    player['balance'] = player.get('balance', 0) + total
    player['inventory'] = []
    db.update_player(user_id, player)
    await update.message.reply_text(f"💰 Berhasil jual semua ikan! Dapat **{total}** koin.")

# --- FITUR TOKO ---
async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    args = context.args
    if not args:
        pesan = "🛒 **TOKO JORAN SAKTI**\n\n"
        for k, v in FISHING_RODS.items():
            pesan += f"🎣 **Joran {k}** - {v['price']} koin\n"
        await update.message.reply_text(pesan + "\nCara beli: `/shop [nama]`")
        return
    item = " ".join(args).title()
    if item in FISHING_RODS:
        price = FISHING_RODS[item]['price']
        if player.get('balance', 0) >= price:
            player['balance'] -= price
            player['rod'] = item
            db.update_player(user_id, player)
            await update.message.reply_text(f"✅ Selamat! Kamu berhasil membeli **Joran {item}**!")
        else:
            await update.message.reply_text("❌ Koin kamu nggak cukup!")

# --- FITUR DAILY (BARU) ---
async def daily_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    current_time = time.time()
    last_daily = player.get('last_daily', 0)
    wait_time = 86400 # 24 jam dalam detik
    
    if current_time - last_daily < wait_time:
        sisa_detik = int(wait_time - (current_time - last_daily))
        jam = sisa_detik // 3600
        menit = (sisa_detik % 3600) // 60
        await update.message.reply_text(f"🎁 Kamu sudah ambil hadiah hari ini.\nBalik lagi dalam **{jam} jam {menit} menit** ya!")
        return
        
    hadiah = random.randint(200, 500) # Hadiah acak 200-500 koin
    player['balance'] = player.get('balance', 0) + hadiah
    player['last_daily'] = current_time
    db.update_player(user_id, player)
    
    await update.message.reply_text(f"🎁 **DAILY REWARDS!**\nSelamat! Kamu mendapatkan **{hadiah} koin** gratis hari ini. Jangan lupa balik besok!")
