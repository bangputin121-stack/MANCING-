import random
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # Logika acak mendapatkan ikan
    rand_val = random.randint(1, 100)
    dapat_ikan = None
    
    # Cek dari yang paling langka
    sorted_fish = sorted(FISH_DATA.items(), key=lambda x: x[1]['chance'])
    
    current_chance = 0
    for name, info in sorted_fish:
        current_chance += info['chance']
        if rand_val <= current_chance:
            dapat_ikan = name
            break
            
    if dapat_ikan:
        player['inventory'].append(dapat_ikan)
        db.update_player(user_id, player)
        await update.message.reply_text(f"🎣 *Sret!* Kamu mendapatkan ikan **{dapat_ikan}**!")
    else:
        await update.message.reply_text("🌊 Yah... ikannya lepas. Coba lagi!")
