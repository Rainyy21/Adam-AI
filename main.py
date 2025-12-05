import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import infractionCont

# load the .env file
load_dotenv()

# get the discord token from the env
TOKEN = os.getenv("DISCORD_API")

# We need Message Content Intent to read the content of user commands
intents = discord.Intents.default()
intents.message_content = True

# bot will list to the command start with '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# =====================================================================
# test event to see if the bot is working
# =====================================================================

# test bot event
@bot.event
async def on_ready():
    # load in the database
    infractionCont.initialize_db()
    print("Database initialized and connected.")
    
    # log in check
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# ==========================================================
# a ping command on the discord part to see if it connected
# ==========================================================
#ping 
@bot.command(name='ping')
async def ping(ctx):
    """Checks the bot's latency and responds 'Pong!'"""
    await ctx.send('Pong!') 
    
# ======================================================
# quote
# it used random to choose a quote and print it out 
# it trigger with !adam
# ======================================================

# import random to select random quote
import random

# quote
QUOTE = [
    "Don't be rude"
]

# command adam
@bot.command(name='adam')
async def get_quote(ctx):
    """sends a random quote by adam"""
    selected_quote = random.choice(QUOTE)
    await ctx.send(selected_quote)

# ======================================================
# you have a list of bad word 
# if the bot detect the bad word than it will say
    # "dont be rude"
# than it go into a hour long cool down

# input the discord text

# check if the word contain the bad_word

# if there a bad word, "say dont be rude"
# than it go through a timer 
# ======================================================
# all the bad word to rigger on message
BAD_WORD = [
    "rape", "bitch",
    "fuck", "shut up",
    "stupid", "rude",
    "dumb", "molest",
    "idiot", "moron",
    "retard", "damn",
    "hell", "asshole",
    "kys", "kill yourself",
    "grape", "negative",
    "hate"
    ]

# bot cool down time
import time
COOLDOWN_SECONDS = 3600
# user cool down

cooldown_per_user = {}

#  check if people send adam
@bot.listen()
async def on_message(message):
    
    if message.author.bot:
        await bot.process_commands(message)
        return
    
    # the current time and user id
    current_time = time.time()
    user_id = message.author.id
        
    # get message and lower case them and checker for profanity
    message_content_lower = message.content.lower()
    profanity_detected = any(word in message_content_lower for word in BAD_WORD)
    
    # if there not profanity than skip
    if not profanity_detected:
        await bot.process_commands(message)
        return
    
    if user_id in cooldown_per_user:
        last_used = cooldown_per_user[user_id]
        time_elapsed = current_time - last_used
        
    # check if it pass the cooldown 
        if time_elapsed > COOLDOWN_SECONDS:
            await message.channel.send("Don't be rude!!")
            infractionCont.add_infractions(user_id, message.author.name)
            # set the new time 
            cooldown_per_user[user_id] = current_time
    else:
        if profanity_detected:
            await message.channel.send("Don't be rude!!") 
            cooldown_per_user[user_id] = current_time
            infractionCont.add_infractions(user_id, message.author.name)
                # set the new time 
    # return a message if it not
    await bot.process_commands(message)

# =========================================================
# top 5 people that curse
# =========================================================
@bot.event(name = "mostwanted")
async def top_rude_people(ctx):
    pass


# ====================================================
# running command 
bot.run(TOKEN)