@bot.command()
async def meditation_start(ctx, duration: int = -1):
    logging.info("meditation_start command invoked.")

    if duration == -1:
        await ctx.send("You must specify a duration for the meditation session.")
        return
    elif duration < 6:
        await ctx.send("The duration of the meditation session must be at least 6 minutes (needs to have time to play an intro and outro).")
        return

    #These paths should be able to be modified by the user.. so TODO: make them configurable
    intro_chanting_path, outro_chanting_path = "data/audio/intro-chanting.mp3", "data/audio/outro-chanting.mp3"
    intro_chant, outro_chant = discord.FFmpegPCMAudio(intro_chanting_path), discord.FFmpegPCMAudio(outro_chanting_path)


    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Starting meditation session for {duration} minutes.")
    
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    start_members = voice_channel.members
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for member in start_members:
        if member != bot.user:
            await member.edit(mute=True)
    
    start_member_list = [str(member.id) for member in start_members]
    
    # Wait for duration of session

    intro_duration = MP3(intro_chanting_path).info.length
    outro_duration = MP3(outro_chanting_path).info.length

    # Play intro audio
    # sleep for duration of session minus intro audio duration and outro audio duration
    await ctx.send(f"....DEBUG....")
    await ctx.send(f"intro_duration: {intro_duration}")
    await ctx.send(f"outro_duration: {outro_duration}")
    await ctx.send(f"duration: {duration}")
    await ctx.send(f"duration in mins: {duration * 60}")
    await ctx.send(f"sleeping for: {(duration * 60) - (intro_duration)}")
    await ctx.send(f"EST TIME OF COMPLETION: {datetime.now() + timedelta(seconds=(duration * 60))}")


    await ctx.send("Meditation session is starting... intro now playing")
    vc.play(intro_chant)
    while vc.is_playing():
        await asyncio.sleep(1) # sleeping until the intro is done playing


    await asyncio.sleep((duration * 60) - intro_duration - outro_duration)  # sleep for duration..

    # Send message indicating session is ending soon
    
    await ctx.send("Meditation session is ending... outro now playing")
    vc.play(outro_chant)
    while vc.is_playing():
        await asyncio.sleep(1) # sleeping until the intro is done playing
    # Get members at end


    await ctx.send("Meditation session has ended.")
    
    members = voice_channel.members
    end_member_list = [str(member.id) for member in members]
    
    # Unmute members and update database
    for member in start_members:
        await member.edit(mute=False)
        
    completed_members = [member_id for member_id in start_member_list if member_id in end_member_list]
    
    await ctx.send(f"Completed members: {completed_members}")

    add_to_session_history(timestamp, duration, ",".join(start_member_list), ",".join(end_member_list), ",".join(completed_members))

    # check if the user exists in the user_stats table
    for member_id in completed_members:
        ensure_user_exists(member_id)
        add_streaks(member_id)
        check_streak_and_update(member_id)
        add_last_meditation_date(member_id)
        add_duration_to_total_time(member_id, duration)
        update_average_time(member_id)

    await asyncio.sleep(5)
    await vc.disconnect()
    logging.info("test_meditation command execution completed.")
