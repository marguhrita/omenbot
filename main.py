from keepalive import keep_alive
import discord, os, requests
from discord.ext import commands




intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents = intents, activity=discord.Game("doing something.. probably"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 

#<----------------------------------------------------->





@client.event
async def on_message(message):
  return







#<----------------------------------------------------->

client.run(os.getenv('TOKEN'))

keep_alive()
