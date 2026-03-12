from telegram import Update
from telegram.ext import ContextTypes

# --- KONFIGURASI ADMIN ---
ADMIN_ID = 7573097201 # <--- GANTI JADI ID LO!

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

# 4. RESET PLAYER (Bagian yang tadi error)
async def reset_player_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    args = context.args
    if not args: return
    target_id = str(args[0])
    db = context.bot_data['db']
    # Pastikan baris di bawah ini tertulis lengkap sampai tanda kurung tutup }
    new_data = {"user_id": target_id, "inventory": [], "balance": 0, "rod": "Bambu", "xp": 0, "level": 1, "last_fishing": 0}
    db.update_player(target_id, new_data)
    await update.message.reply_text(f"⚠️ Data ID `{target_id}` di-reset!")

# 5. EVENT CONTROL
async def event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    args = context.args
    if not args:
        status = context.bot_data.get('event_status', False)
        await update.message.reply_text(f"📢 Event: **{'AKTIF' if status else 'MATI'}**")
        return
    cmd = args[0].lower()
    context.bot_data['event_status'] = (cmd == "on")
    teks = "🎊 **EVENT 2x XP AKTIF!**" if cmd == "on" else "🛑 **EVENT MATI!**"
    await update.message.reply_text(teks)

# 6. CHECK PLAYER
async def check_player_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args: return
    target_id = str(context.args[0])
    db = context.bot_data['db']
    p = db.get_player(target_id)
    pesan = f"🔍 **INSPEKSI: {target_id}**\n⭐ Lvl: {p.get('level')}\n💰 Saldo: {p.get('balance')}\n🎣 Joran: {p.get('rod')}\n🎒 Tas: {len(p.get('inventory'))} ikan"
    await update.message.reply_text(pesan)
