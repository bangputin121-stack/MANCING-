from telegram import Update
from telegram.ext import ContextTypes

# --- MASUKKAN ID ADMIN DI SINI ---
ADMIN_IDS = [12345678, 87654321] # Ganti dengan ID lo dan ID temen lo

async def add_coin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    try:
        target_id, amount = str(context.args[0]), int(context.args[1])
        db = context.bot_data['db']
        player = db.get_player(target_id)
        player['balance'] += amount
        db.update_player(target_id, player)
        await update.message.reply_text(f"✅ {amount} koin dikirim ke `{target_id}`")
    except:
        await update.message.reply_text("❌ Gunakan: `/addcoin [id] [jumlah]`")

async def gift_fish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    try:
        target_id, ikan = str(context.args[0]), context.args[1].title()
        db = context.bot_data['db']
        player = db.get_player(target_id)
        player['inventory'].append(ikan)
        db.update_player(target_id, player)
        await update.message.reply_text(f"🎁 {ikan} dikirim ke `{target_id}`")
    except:
        await update.message.reply_text("❌ Gunakan: `/giftfish [id] [ikan]`")

async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    msg = " ".join(context.args)
    if not msg: return
    db = context.bot_data['db']
    for uid in db.data.keys():
        try: await context.bot.send_message(chat_id=uid, text=f"📢 **INFO:**\n{msg}")
        except: continue
    await update.message.reply_text("🚀 Broadcast terkirim.")

async def reset_player_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    try:
        target_id = str(context.args[0])
        db = context.bot_data['db']
        new_data = {"user_id": target_id, "inventory": [], "balance": 0, "rod": "Bambu", "bait": 0, "xp": 0, "level": 1}
        db.update_player(target_id, new_data)
        await update.message.reply_text(f"⚠️ ID `{target_id}` di-reset.")
    except: pass

async def event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    status = context.args[0].lower() == "on" if context.args else False
    context.bot_data['event_status'] = status
    await update.message.reply_text(f"📢 Event 2x XP: **{'ON' if status else 'OFF'}**")

async def check_player_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    target_id = str(context.args[0])
    db = context.bot_data['db']
    p = db.get_player(target_id)
    await update.message.reply_text(f"🔍 ID: {target_id}\n💰 Bal: {p['balance']}\n🎣 Rod: {p['rod']}")
