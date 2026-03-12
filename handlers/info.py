from telegram import Update
from telegram.ext import ContextTypes

# Fungsi untuk /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    pesan = (
        f"👋 Halo {user_name}!\n\n"
        "Selamat datang di **Fishing Bot World**! 🎣\n"
        "Di sini kamu bisa mancing, kumpulin ikan, dan jadi pemancing legendaris.\n\n"
        "Ketik `/help` untuk melihat daftar perintah."
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")

# Fungsi untuk /help
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "📖 **DAFTAR PERINTAH BOT**\n\n"
        "🎣 `/fishing` - Mulai memancing ikan\n"
        "🎒 `/bag` - Cek isi tas dan saldo koin\n"
        "💰 `/jual` - Jual semua ikan di tas jadi koin\n"
        "🛒 `/shop` - Beli joran yang lebih sakti\n"
        "👤 `/profil` - Lihat status joran dan saldo kamu\n"
        "❓ `/help` - Nampilin bantuan ini"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")

# Fungsi untuk /profil
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # Ambil data player (kasih nilai default kalau kosong)
    joran = player.get('rod', 'Bambu')
    saldo = player.get('balance', 0)
    total_ikan = len(player.get('inventory', []))
    
    pesan = (
        f"👤 **PROFIL PEMANCING**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"🎣 **Joran:** {joran}\n"
        f"💰 **Saldo:** {saldo} koin\n"
        f"🎒 **Isi Tas:** {total_ikan} ekor ikan\n"
        f"━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")
