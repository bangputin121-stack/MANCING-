from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Halo {user.first_name}!\n\n"
        "Selamat datang di **Fishing RPG Bot**.\n"
        "Gunakan `/fishing` untuk mulai memancing dan `/help` untuk melihat daftar perintah.\n\n"
        "Jangan lupa beli umpan dulu di `/shop` ya!"
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🎮 **DAFTAR PERINTAH BOT**\n\n"
        "🎣 /fishing - Mulai memancing\n"
        "👤 /profil - Cek level, koin, dan joran\n"
        "🎒 /bag - Lihat ikan yang kamu punya\n"
        "🛒 /shop - Beli joran atau umpan baru\n"
        "💰 /jual - Jual semua ikan di tas\n"
        "🎁 /daily - Klaim koin harian\n"
        "🏆 /top - Leaderboard (Coming Soon)"
    )
    await update.message.reply_text(help_text)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)

    lvl = player.get('level', 1)
    xp = player.get('xp', 0)
    saldo = player.get('balance', 0)
    joran = player.get('rod', 'Bambu')
    stok_umpan = player.get('bait', 0)
    tipe_umpan = player.get('current_bait', '-')
    isi_tas = len(player.get('inventory', []))

    pesan = (
        f"👤 **PROFIL PEMANCING**\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⭐ **Level:** {lvl} | 📈 **XP:** {xp}/{lvl*100}\n"
        f"💰 **Saldo:** {saldo} koin\n"
        f"🎣 **Joran:** {joran}\n"
        f"🪱 **Umpan:** {stok_umpan} ({tipe_umpan})\n"
        f"🎒 **Isi Tas:** {isi_tas} ekor\n"
        f"━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")
