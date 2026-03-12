from telegram import Update
from telegram.ext import ContextTypes

# --- KONFIGURASI ADMIN ---
ADMIN_ID = 12345678  # <--- GANTI JADI ID LO!

# 1. TAMBAH KOIN
async def add_coin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Gunakan: `/addcoin [id] [jumlah]`")
        return
    target_id, amount = str(args[0]), int(args[1])
    db = context.bot_data['db']
    player = db.get_player(target_id)
    player['balance'] += amount
    db.update_player(target_id, player)
    await update.message.reply_text(f"✅ Saldo ID `{target_id}` ditambah {amount} koin.")

# 2. HADIAH IKAN
async def gift_fish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Gunakan: `/giftfish [id] [NamaIkan]`")
        return
    target_id, ikan = str(args[0]), args[1].title()
    db = context.bot_data['db']
    player = db.get_player(target_id)
    player['inventory'].append(ikan)
    db.update_player(target_id, player)
    await update.message.reply_text(f"🎁 Ikan **{ikan}** dikirim ke ID `{target_id}`.")

# 3. BROADCAST
async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    pesan_broadcast = " ".join(context.args)
    if not pesan_broadcast:
        await update.message.reply_text("❌ Ketik pesannya!")
        return
    db = context.bot_data['db']
    all_users = list(db.data.keys())
    count = 0
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 **PENGUMUMAN ADMIN**\n\n{pesan_broadcast}", parse_mode="Markdown")
            count += 1
        except: continue
    await update.message.reply_text(f"🚀 Terkirim ke {count} user.")

# 4. RESET PLAYER
async def reset_player_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    args = context.args
    if not args: return
    target_id = str(args[0])
    db = context.bot_data['db']
    new_data = {"user_id": target_id, "inventory": [], "balance": 0, "rod": "Bambu", "xp": 0, "
