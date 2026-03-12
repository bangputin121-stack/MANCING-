import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # --- SISTEM COOLDOWN ---
    current_time = time.time()
    last_fishing = player.get('last_fishing', 0)
    cooldown_time = 0  # Jeda waktu dalam detik (silakan ubah sesuai selera)
    
    if current_time - last_fishing < cooldown_time:
        sisa_waktu = int(cooldown_time - (current_time - last_fishing))
        await update.message.reply_text(f"⏳ Sabar bro! Kamu baru bisa mancing lagi dalam **{sisa_waktu} detik**.")
        return
    # -----------------------

    # 1. Cek Joran & Bonus
    nama_joran = player.get('rod', 'Bambu')
    bonus_hoki = FISHING_RODS.get(nama_joran, {}).get('bonus', 0)
    
    # 2. Logika Luck
    luck_roll = random.randint(1, 100) + bonus_hoki
    
    if luck_roll >= 95:
        dapat_ikan = "Nemo"
    elif luck_roll >= 85:
        dapat_ikan = "Paus"
    elif luck_roll >= 70:
        dapat_ikan = "Nila"
    elif luck_roll >= 40:
        dapat_ikan = "Lele"
    else:
        dapat_ikan = "Teri"

    # 3. Update Data Player
    player['inventory'].append(dapat_ikan)
    player['last_fishing'] = current_time  # Simpan waktu terakhir mancing
    db.update_player(user_id, player)
    
    await update.message.reply_text(
        f"🎣 Kamu mancing pakai **Joran {nama_joran}** (+{bonus_hoki}% Hoki)\n\n"
        f"✨ *Sret!* Kamu dapet ikan **{dapat_ikan}**!\n"
        f"Cek tas kamu pakai `/bag`."
    )
