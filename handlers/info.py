from telegram import Update
from telegram.ext import ContextTypes

# --- FUNGSI START ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    pesan = (
        f"👋 Halo {user_name}!\n\n"
        "Selamat datang di **Fishing Bot World**! 🎣\n"
        "Mancing, naikkan level, dan beli joran terbaik!\n\n"
        "Ketik `/help` untuk melihat daftar perintah."
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")

# --- FUNGSI HELP ---
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "📖 **DAFTAR PERINTAH BOT**\n\n"
        "🎣 `/mancing` - Mulai memancing ikan\n"
        "🎒 `/bag` - Cek isi tas & saldo koin\n"
        "💰 `/jual` - Jual ikan di tas jadi koin\n"
        "🛒 `/shop` - Beli joran yang lebih sakti\n"
        "👤 `/profil` - Lihat Level, XP, dan status kamu\n"
        "❓ `/help` - Nampilin bantuan ini"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")

# --- FUNGSI PROFIL ---
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # Ambil data player
    lvl = player.get('level', 1)
    xp = player.get('xp', 0)
    target_xp = lvl * 100
    joran = player.get('rod', 'Bambu')
    saldo = player.get('balance', 0)
    total_ikan = len(player.get('inventory', []))
    
    # Membuat tampilan progres bar sederhana (opsional tapi keren)
    progres = int((xp / target_xp) * 10)
    bar = "🟩" * progres + "⬜" * (10 - progres)
    
    pesan = (
        f"👤 **PROFIL PEMANCING**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⭐ **Level:** {lvl}\n"
        f"📈 **XP:** `{xp}/{target_xp}`\n"
        f"[{bar}]\n\n"
        f"🎣 **Joran:** {joran}\n"
        f"💰 **Saldo:** {saldo} koin\n"
        f"🎒 **Isi Tas:** {total_ikan} ekor ikan\n"
        f"━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")
