import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS, BAITS

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # 1. CEK UMPAN
    stok_umpan = player.get('bait', 0)
    if stok_umpan <= 0:
        await update.message.reply_text("❌ Umpan habis! Beli dulu di `/shop`.")
        return

    # 2. CEK COOLDOWN
    current_time = time.time()
    if current_time - player.get('last_fishing', 0) < 30:
        sisa = int(30 - (current_time - player.get('last_fishing', 0)))
        await update.message.reply_text(f"⏳ Tunggu {sisa} detik lagi!")
        return

    # 3. PROSES MANCING
    umpan_nama = player.get('current_bait', 'Cacing')
    bonus_umpan = BAITS.get(umpan_nama, {}).get('bonus', 0)
    bonus_joran = FISHING_RODS.get(player.get('rod', 'Bambu'), {}).get('bonus', 0)
    
    luck = random.randint(1, 100) + bonus_joran + bonus_umpan
    
    if luck >= 100: dapat = "Nemo"
    elif luck >= 85: dapat = "Paus"
    elif luck >= 70: dapat = "Nila"
    elif luck >= 40: dapat = "Lele"
    else: dapat = "Teri"

    # XP & Event
    base_xp = random.randint(15, 30)
    xp_gain = base_xp * 2 if context.bot_data.get('event_status') else base_xp
    
    # Simpan Perubahan
    player['bait'] = stok_umpan - 1
    player['inventory'] = player.get('inventory', []) + [dapat]
    player['last_fishing'] = current_time
    player['xp'] = player.get('xp', 0) + xp_gain
    
    # Level Up
    lvl = player.get('level', 1)
    if player['xp'] >= (lvl * 100):
        player['level'] += 1
        player['xp'] = 0
        msg_lvl = f"\n🎊 **LEVEL UP KE {player['level']}!**"
    else: msg_lvl = ""

    db.update_player(user_id, player)
    await update.message.reply_text(
        f"🎣 Mancing pake **{umpan_nama}**...\n"
        f"✨ Dapat: **{dapat}** (+{xp_gain} XP)\n"
        f"🪱 Sisa Umpan: {player['bait']}{msg_lvl}"
    )
