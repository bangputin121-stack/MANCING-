from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

# Fitur Jual Ikan
async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    inventory = player.get('inventory', [])
    
    if not inventory:
        await update.message.reply_text("❌ Tas kamu kosong!")
        return

    total_hasil = 0
    for item in inventory:
        harga = FISH_DATA.get(item, {}).get('price', 0)
        total_hasil += harga
    
    player['balance'] = player.get('balance', 0) + total_hasil
    player['inventory'] = [] 
    db.update_player(user_id, player)
    
    await update.message.reply_text(f"💰 Berhasil jual semua ikan! Dapat **{total_hasil}** koin.")

# Fitur Lihat Toko & Beli Joran
async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    args = context.args # Untuk menangkap input setelah /shop (misal: /shop berlian)

    # Kalau cuma ketik /shop (nampilin menu)
    if not args:
        pesan = "🛒 **TOKO JORAN SAKTI**\n\n"
        for name, info in FISHING_RODS.items():
            pesan += f"🎣 **Joran {name}**\n"
            pesan += f"   - Harga: {info['price']} koin\n"
            pesan += f"   - Bonus hoki: +{info['bonus']}%\n\n"
        pesan += "\nCara beli: Ketik `/shop [nama_joran]`\nContoh: `/shop Berlian`"
        await update.message.reply_text(pesan, parse_mode="Markdown")
        return

    # Kalau mau beli (misal: /shop Berlian)
    item_name = " ".join(args).title()
    if item_name in FISHING_RODS:
        price = FISHING_RODS[item_name]['price']
        if player.get('balance', 0) >= price:
            player['balance'] -= price
            player['rod'] = item_name
            db.update_player(user_id, player)
            await update.message.reply_text(f"✅ Selamat! Kamu berhasil membeli **Joran {item_name}**!")
        else:
            await update.message.reply_text("❌ Duit kamu nggak cukup, bos!")
    else:
        await update.message.reply_text("❌ Joran itu nggak ada di toko.")
