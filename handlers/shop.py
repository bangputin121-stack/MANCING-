from telegram import Update
from telegram.ext import ContextTypes
from database import Database

db = Database()

async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    args = context.args # Buat nangkep perintah /buy 1

    # Daftar Barang Toko
    items = {
        "1": {"nama": "Joran Carbon", "harga": 500},
        "2": {"nama": "☠️ JORAN LEGENDARIS", "harga": 5000}
    }

    if not args:
        # Tampilan Menu Toko
        pesan = "🛒 *TOKO ALAT PANCING*\n\n"
        for k, v in items.items():
            pesan += f"{k}. {v['nama']} — 💰 {v['harga']} Coins\n"
        pesan += "\nKetik `/buy [nomor]` untuk membeli."
        return await update.message.reply_text(pesan, parse_mode='Markdown')

    pilihan = args[0]
    if pilihan in items:
        item = items[pilihan]
        if user_data['balance'] >= item['harga']:
            # Potong saldo & update joran
            new_balance = user_data['balance'] - item['harga']
            db.update_user(user_id, "balance", new_balance)
            db.update_user(user_id, "joran", item['nama'])
            
            await update.message.reply_text(f"✅ Berhasil membeli *{item['nama']}*!\nSaldo sisa: {new_balance} koin.")
        else:
            await update.message.reply_text("❌ Koin lo nggak cukup, Bang! Mancing lagi gih.")
    else:
        await update.message.reply_text("❌ Nomor barang nggak ada.")
