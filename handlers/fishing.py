import random
from telegram import Update
from telegram.ext import ContextTypes
from game_data import FISH_DATA, FISHING_RODS

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    # 1. Cek Joran yang dipakai & ambil Bonusnya
    nama_joran = player.get('rod', 'Bambu')
    bonus_hoki = FISHING_RODS.get(nama_joran, {}).get('bonus', 0)
    
    # 2. Logika acak (Angka keberuntungan)
    # Semakin bagus joran, angka keberuntungan makin tinggi
    luck_roll = random.randint(1, 100) + bonus_hoki
    
    dapat_ikan = None
    
    # 3. Urutkan ikan dari yang tersulit (Peluang terkecil)
    # Kita balik: Kalau roll tinggi, dapet yang langka
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

    # Simpan ke tas
    player['inventory'].append(dapat_ikan)
    db.update_player(user_id, player)
    
    await update.message.reply_text(
        f"🎣 Kamu memancing menggunakan **Joran {nama_joran}** (Bonus: +{bonus_hoki}%)\n\n"
        f"✨ *Sret!* Kamu berhasil mendapatkan ikan **{dapat_ikan}**!"
    )
