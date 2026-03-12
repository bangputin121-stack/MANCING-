import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # --- 1. SISTEM COOLDOWN (30 DETIK) ---
    current_time = time.time()
    last_fishing = player.get('last_fishing', 0)
    cooldown_time = 8 
    
    if current_time - last_fishing < cooldown_time:
        sisa_waktu = int(cooldown_time - (current_time - last_fishing))
        await update.message.reply_text(f"⏳ Sabar bro! Kamu baru bisa mancing lagi dalam **{sisa_waktu} detik**.")
        return

    # --- 2. LOGIKA MANCING & BONUS JORAN ---
    nama_joran = player.get('rod', 'Bambu')
    bonus_hoki = FISHING_RODS.get(nama_joran, {}).get('bonus', 0)
    
    # Nilai acak ditambah bonus dari joran (misal joran Berlian +15)
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

    # --- 3. SISTEM XP & LEVEL UP ---
    xp_gain = random.randint(15, 30) # Tiap mancing dapet 15-30 XP acak
    current_xp = player.get('xp', 0) + xp_gain
    current_level = player.get('level', 1)
    
    # Rumus Target XP: Level saat ini dikali 100
    target_xp = current_level * 100
    
    pesan_level_up = ""
    if current_xp >= target_xp:
        current_level += 1
        current_xp = 0 # Reset XP setelah naik level
        pesan_level_up = f"\n\n🎊 **LEVEL UP!**\nSelamat! Kamu naik ke **Level {current_level}**!"

    # --- 4. SIMPAN DATA KE DATABASE ---
    player['inventory'].append(dapat_ikan)
    player['last_fishing'] = current_time
    player['xp'] = current_xp
    player['level'] = current_level
    db.update_player(user_id, player)
    
    # Balasan ke user
    await update.message.reply_text(
        f"🎣 Kamu mancing pakai **Joran {nama_joran}**\n"
        f"✨ Dapat: **{dapat_ikan}** (+{xp_gain} XP){pesan_level_up}\n"
        f"📊 Progress: `{current_xp}/{target_xp} XP`",
        parse_mode="Markdown"
    )
