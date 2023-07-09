import os
import asyncio
import sqlite3
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from mutagen.mp3 import MP3
import discord
from discord.ext import commands
from utils.helpers import initialize_db
from meditation import Meditation

DATABASE_PATH = r"C:\Users\lukeb\Desktop\Projects\Goenka-Bot\GoenkaBot\data\meditation.db" # If running localy change this to your path
logging.basicConfig(level=logging.INFO)


# Load environment variables
load_dotenv()
token = os.getenv('APITOKEN') # Make sure your token is stored in the .env file

# Initialize bot with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize database
initialize_db()

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
# Ping command

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# --------------------------------------------

# Meditation session class
class MeditationSession:
    def __init__(self) -> None:
        self.duration = None
        self.intro_chant_bool = None
        self.outro_chant_bool = None
        self.intro_chant_path = None
        self.outro_chant_path = None
        self.intro_chant_duration = None
        self.outro_chant_duration = None
        # what should a meditation session have?
        # how long it is
        # if it has an intro chant and outro chant and if so what are their paths
        # how long the intro chant and outro chant are

        # a function to run the meditation session.. which is the following psudocode:
        #   play intro chant if there is one..  sleep for the duration of the meditation session minus the intro chant duration and outro chant duration (if there is one).. play outro chant if there is one
        # if metta meditation is on, play the metta meditation audio file after the outro.. session and account for the duration of the metta meditation audio file
        # a sub function to play an audio file


        # function to configure the default meditation session with the following parameters:
        # default intro-chant .. default outro-chant .. default duration .. default metta meditation audio file .. default metta meditation duration .. default metta meditation bool
        # also allow it to be configured within the command itself

        # changing the default may need DB..?
        # actually if deployed then would need server config DB to store the default meditation session settings
        # bc then the defaults would be the same for every server
        # if not deployed then can just store the default meditation session settings in a config file

        #  

        pass




# Start meditation command
@bot.command()
async def old_meditate(ctx, duration: int):
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} minutes")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    members = voice_channel.members
    print("Loading users in current voice channels...")

    start_member_list = [member.id for member in members]
    
    
    
    # Play intro audio
    vc.play(intro_chant)
    
    # Wait for the meditation duration minus the intro audio duration
    await asyncio.sleep((duration * 60) - (intro_chant_duration + outro_chant_duration))
    
    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end.")
    
    # Play outro audio
    vc.play(outro_chant)

    members = voice_channel.members
    print("Loading users in current voice channels...")

    end_member_list = [member.id for member in members]    
    
    #compare start_member_list and end_member_list and if the user is in both lists, add 1 to their streak in the database
    for member in start_member_list:
        if member in end_member_list:
            print("{} meditated the entire time!".format(member))
            #add 1 to their streak in the database
        else:
            # print("member is not in both lists")
            print("{} did not meditate the entire time!".format(member))

            #do nothing

    #Wait a little so it feels more natural before leaving

    
    await asyncio.sleep(15)
    
    # Disconnect from the voice channel
    await vc.disconnect()



# Start meditation command
@bot.command()
async def start_meditation_debug(ctx, duration: int):
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    members = voice_channel.members
    #     await ctx.send(member.mention)


    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} minutes")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    
    # Play intro audio
    vc.play(intro_chant)
    
    # Wait for the meditation duration minus the intro audio duration
    await asyncio.sleep((duration * 60) - intro_chant_duration)
    
    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end.")
    
    # Play outro audio
    vc.play(outro_chant)
    
    #Wait a little so it feels more natural before leaving
    await asyncio.sleep(15)

    # Disconnect from the voice channel
    await vc.disconnect()








# --------------------------------------------

# Start meditation command
@bot.command()
async def full_time_test(ctx):
    duration = 10
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} seconds")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    members = voice_channel.members
    print("Loading users in current voice channels...")

    start_member_list = [member.id for member in members]
    print("start_member_list: {}".format(start_member_list))

    # Send message indicating session is ending soon
    await asyncio.sleep(duration)
    await ctx.send("Meditation session is coming to an end.")
    


    members = voice_channel.members
    print("Loading users in current voice channels...")

    end_member_list = [member.id for member in members]    
    
    print("end_member_list: {}".format(end_member_list))
    #compare start_member_list and end_member_list and if the user is in both lists, add 1 to their streak in the database
    for member in start_member_list:
        if member in end_member_list:
            print("{} meditated the entire time!".format(member))
            #add 1 to their streak in the database
        else:
            # print("member is not in both lists")
            print("{} did not meditate the entire time!".format(member))

            #do nothing

    #Wait a little so it feels more natural before leaving

    
    await asyncio.sleep(15)
    
    # Disconnect from the voice channel
    await vc.disconnect()








# ----------------------------------------------



def execute_sql(sql, parameters=()):
    try:
        logging.info(f"Trying to connect to database at {DATABASE_PATH}")
        connection = sqlite3.connect(DATABASE_PATH)
        logging.info("Connected to database.")
    except sqlite3.OperationalError as e:
        logging.error(f"Failed to connect to database: {e}")
        return
    # cursor = connection.cursor()
    cursor = connection.cursor()
    try:
        logging.info(f"Executing SQL: {sql} with parameters {parameters}")
        cursor.execute(sql, parameters)
        connection.commit()
        logging.info("SQL executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute SQL: {e}")
    finally:
        connection.close()


def ensure_user_exists(user_id):
    logging.info(f"Ensuring user {user_id} exists in user_stats table...")
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    # Check if the user exists
    cursor.execute("SELECT user_id FROM user_stats WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        # If the user doesn't exist, insert them into the user_stats table
        cursor.execute("INSERT INTO user_stats (user_id) VALUES (?)", (user_id,))
        logging.info(f"User {user_id} added to user_stats table.")
    connection.commit()
    connection.close()

# New function to update user stats
# Bot command to get meditation stats

def update_user_stats(user_id, duration_minutes):
    # Query to get existing user stats
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    ensure_user_exists(user_id)
    cursor.execute("SELECT total_sessions, total_time FROM user_stats WHERE user_id=?",                   (user_id,))
    result = cursor.fetchone()
    conn.close()

    # Calculate new stats
    if result:
        total_sessions, total_time = result
        total_sessions += 1
        total_time += duration_minutes
        average_time = total_time / total_sessions

        # Update existing user
        execute_sql("UPDATE user_stats SET total_sessions = ?, total_time = ?, average_time = ?, last_meditation_date = ? WHERE user_id = ?",
                    (total_sessions, total_time, average_time, datetime.date.today().isoformat(), user_id))
    else:
        # Insert new user
        execute_sql("INSERT INTO user_stats (user_id, total_sessions, total_time, average_time, last_meditation_date) VALUES (?, ?, ?, ?, ?)",
                    (user_id, 1, duration_minutes, duration_minutes, datetime.date.today().isoformat()))


def check_streak_and_update(user_id):
    logging.info(f"Checking streak for member_id: {user_id}")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # Reset the current_streak if the user has missed a day or more, including today
    cursor.execute("""
        UPDATE user_stats
            SET current_streak = 0
             WHERE user_id = ? 
             AND last_meditation_date < ?;
    """, (user_id, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')))
    print("**************************")
    print("date time now: {}".format(datetime.now().strftime('%Y-%m-%d')))
    print("date time now - 1: {}".format((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')))
    print("**************************")
     # Update longest_streak if current_streak is greater
    cursor.execute("""
        UPDATE user_stats
            SET longest_streak = current_streak
             WHERE user_id = ? AND current_streak > longest_streak;
    """, (user_id,))
    
    conn.commit()
    conn.close()


def add_streaks(user_id):
    logging.info(f"Adding to streak for member_id: {user_id}")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE user_stats
            SET current_streak = current_streak + 1
             WHERE user_id = ? 
             AND last_meditation_date < ? AND last_meditation_date >= ?;
    """, (user_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')))


    conn.commit()
    conn.close()

def add_last_meditation_date(member_id):
    logging.info(f"Adding last meditation date for member_id: {member_id}")
    ensure_user_exists(member_id)
    print("Before executing the SQL query...")
    execute_sql('''
        UPDATE user_stats
        SET last_meditation_date = ?
        WHERE user_id = ?;
    ''', (datetime.now().strftime('%Y-%m-%d'), member_id))
    print("After executing the SQL query...")


def add_duration_to_total_time(member_id, duration):
    logging.info(f"Adding duration {duration} to total time for member_id: {member_id}")
    ensure_user_exists(member_id)
    print("Before executing the SQL query...")
    execute_sql('''
        UPDATE user_stats
        SET total_time = total_time + ?
        WHERE user_id = ?;
    ''', (duration, member_id))
    print("After executing the SQL query...")

    # add to total_sessions
    execute_sql('''
        UPDATE user_stats
        SET total_sessions = total_sessions + 1
        WHERE user_id = ?;
    ''', (member_id,))

    print("After executing the SQL query...")


def add_to_session_history(timestamp, duration, start_member_list, end_member_list, completed_members):
    logging.info(f"Adding to session history: timestamp={timestamp}, duration={duration}, start_members={start_member_list}, end_members={end_member_list}, completed_members={completed_members}")
    print("Before executing the SQL query...")
    execute_sql('''
        INSERT INTO session_history (timestamp, duration, start_members, end_members, completed_members)
        VALUES (?, ?, ?, ?, ?);
    ''', (timestamp, duration, start_member_list, end_member_list, completed_members))
    print("After executing the SQL query...")


def update_average_time(member_id):
    logging.info(f"Updating average time for member_id: {member_id}")
    ensure_user_exists(member_id)
    print("Before executing the SQL query...")

    execute_sql('''
        UPDATE user_stats
        SET average_time = (SELECT total_time / CAST(COUNT(*) AS REAL) FROM session_history WHERE user_id = ?)
        WHERE user_id = ?;
    ''', (member_id, member_id))

    print("After executing the SQL query...")





# ---------------------------------- #
#     ------ Bot commands ------     #
# Move these to become cogs later... #
# ---------------------------------- #

@bot.command()
async def meditation_start(ctx, duration = -1):
    logging.info("meditation_start command invoked.")
# if not args or args[0] != 'start':
#     await ctx.send("To start the meditation session type !test_meditation start.")
#     return
# if args[1]:

#   
    
    if duration == -1:
        await ctx.send("You must specify a duration of the meditation session.")
        return
    elif duration < 6:
        await ctx.send("The duration of the meditation session must be at least 6 minutes.")
        return
    
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)

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
    
    # duration is in minutes, so convert
    vc.play(intro_chant)
    # await asyncio.sleep((duration * 60))
    # await asyncio.sleep((duration * 60) - (intro_duration))
    # await asyncio.sleep((duration * 60) - (outro_duration))
    await asyncio.sleep((duration * 60) - intro_duration - outro_duration)

    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end soon kinda...")
    
    vc.play(outro_chant)

    # Get members at end
    members = voice_channel.members
    end_member_list = [str(member.id) for member in members]
    
    # Unmute members and update database
    for member in start_members:
        await member.edit(mute=False)
        
    completed_members = [member_id for member_id in start_member_list if member_id in end_member_list]
    
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


@bot.command()
async def meditation_stats(ctx, member: discord.Member):
    # Query to get user stats
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    check_streak_and_update(member.id)

    cursor.execute("SELECT total_sessions, total_time, average_time, current_streak, longest_streak FROM user_stats WHERE user_id=?",                   (str(member.id),))
    result = cursor.fetchone()
    conn.close()

    # Display stats
    if result:
        total_sessions, total_time, average_time, current_streak, longest_streak = result
        await ctx.send(f"📈☸️🧘 Meditation Stats for {member.mention} 🧘☸️📈\n"
                       f"--------------------------------------------\n"
                       f"🔥 Current Streak: {current_streak} days\n"
                       f"⭐ Longest Streak: {longest_streak} days\n"
                       f"📆 Total Sessions: {total_sessions}\n"
                       f"💧 Total Time Meditated: {total_time} minutes\n"
                       f"🕒 Average Session Length: {average_time:.2f} minutes")
    else:
        await ctx.send(f"No meditation stats found for {member.mention}. 😢")


# ------------------------------------
bot.run(token)