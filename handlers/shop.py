from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA

async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    inventory = player.get('inventory', [])
    
    if not inventory:
        await update.message.reply_text("❌ Tas kamu kosong, gak ada ikan yang bisa dijual!")
        return

    total_hasil = 0
    jumlah_ikan = len(inventory)
    
    # Hitung harga setiap ikan di tas
    for item in inventory:
        # Ambil harga dari game_data, kalau gak ada kasih harga 0
        harga = FISH_DATA.get(item, {}).get('price', 0)
        total_hasil += harga
    
    # Update saldo dan kosongkan tas
    player['balance'] = player.get('balance', 0) + total_hasil
    player['inventory'] = [] # Tas kosong setelah dijual
    
    db.update_player(user_id, player)
    
    await update.message.reply_text(
        f"💰 **BERHASIL JUAL!**\n\n"
        f"📦 Kamu menjual **{jumlah_ikan}** ekor ikan.\n"
        f"💵 Dapat: **{total_hasil}** koin.\n"
        f"💳 Saldo sekarang: **{player['balance']}** koin."
    )
