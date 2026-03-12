from telegram import Update
from telegram.ext import ContextTypes
from collections import Counter

async def bag_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    inventory = player.get('inventory', [])
    
    if not inventory:
        await update.message.reply_text("🎒 Tas kamu kosong melompong. Yuk mancing dulu pakai /fishing!")
        return

    # Menghitung jumlah ikan yang sama agar tampilan rapi
    fish_count = Counter(inventory)
    
    pesan = "🎒 **ISI TAS KAMU**\n\n"
    for fish, count in fish_count.items():
        pesan += f"🐟 {fish}: {count} ekor\n"
    
    # Ambil saldo, kalau belum ada set ke 0
    balance = player.get('balance', 0)
    pesan += f"\n💰 Saldo: {balance} koin"
    
    await update.message.reply_text(pesan, parse_mode="Markdown")
