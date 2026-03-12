# Ganti bagian isi profil di profile_handler:
    pesan = (
        f"👤 **PROFIL PEMANCING**\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⭐ **Level:** {lvl} | 📈 **XP:** {xp}/{lvl*100}\n"
        f"💰 **Saldo:** {saldo} koin\n"
        f"🎣 **Joran:** {joran}\n"
        f"🪱 **Umpan:** {player.get('bait', 0)} ({player.get('current_bait', '-')})\n"
        f"🎒 **Isi Tas:** {len(player.get('inventory', []))} ekor\n"
        f"━━━━━━━━━━━━━━━"
    )
