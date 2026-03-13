import random
from telegram import Update
from telegram.ext import ContextTypes

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Daftar ikan dan harganya (Contoh dasar)
    ikan_list = ["Lele", "Nila", "Gabus", "Sepat", "Mas"]
    ikan_didapat = random.choice(ikan_list)
    harga = random.randint(10, 50)

    # Menampilkan pesan ke user
    await update.message.reply_text(
        f"🎣 Kamu melemparkan kail...\n"
        f"🐟 Hap! Kamu mendapatkan ikan **{ikan_didapat}**!\n"
        f"💰 Ikan ini bisa dijual seharga {harga} koin."
    )

    # Catatan: Di sini lo bisa tambahin kode buat masukin ke database/tas nanti
