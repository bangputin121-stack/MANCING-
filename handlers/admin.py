from telegram import Update
from telegram.ext import ContextTypes

# --- KONFIGURASI ADMIN ---
ADMIN_IDS = [7573097201, 577381]  # <--- MASUKKIN SEMUA ID ADMIN DI SINI

# 1. TAMBAH KOIN
async def add_coin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user ada di dalam daftar admin
    if update.effective_user.id not in ADMIN_IDS: 
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Gunakan: `/addcoin [id] [jumlah]`")
        return
    try:
        target_id, amount = str(args[0]), int(args[1])
        db = context.bot_data['db']
        player = db.get_player(target_id)
        player['balance'] += amount
        db.update_player(target_id, player)
        await update.message.reply_text(f"✅ Saldo ID `{target_id}` ditambah {amount} koin.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# 2. BROADCAST (Contoh update kedua)
async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: # <--- PAKE 'not in'
        return
    
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

# Lakukan hal yang sama (ganti ke 'not in ADMIN_IDS') untuk fungsi reset, event, dan check.
