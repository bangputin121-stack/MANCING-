async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db']
    player = db.get_player(user_id)
    
    current_time = time.time()
    last_fishing = player.get('last_fishing', 0)
    if current_time - last_fishing < 30:
        sisa = int(30 - (current_time - last_fishing))
        await update.message.reply_text(f"⏳ Tunggu {sisa} detik lagi!")
        return

    nama_joran = player.get('rod', 'Bambu')
    bonus = FISHING_RODS.get(nama_joran, {}).get('bonus', 0)
    luck = random.randint(1, 100) + bonus
    
    # Penentuan Ikan
    if luck >= 95: dapat = "Nemo"
    elif luck >= 85: dapat = "Paus"
    elif luck >= 70: dapat = "Nila"
    elif luck >= 40: dapat = "Lele"
    else: dapat = "Teri"

    # LOGIKA XP & EVENT
    base_xp = random.randint(15, 30)
    is_event = context.bot_data.get('event_status', False)
    xp_gain = base_xp * 2 if is_event else base_xp
    
    current_xp = player.get('xp', 0) + xp_gain
    lvl = player.get('level', 1)
    target = lvl * 100
    
    msg_lvl = ""
    if current_xp >= target:
        lvl += 1
        current_xp = 0
        msg_lvl = f"\n🎊 **LEVEL UP ke {lvl}!**"

    # Simpan
    player.update({"inventory": player.get('inventory', []) + [dapat], "last_fishing": current_time, "xp": current_xp, "level": lvl})
    db.update_player(user_id, player)
    
    status_event = " [EVENT 2x XP]" if is_event else ""
    await update.message.reply_text(f"🎣 Pakai **{nama_joran}**\n✨ Dapat: **{dapat}** (+{xp_gain} XP){status_event}{msg_lvl}")
