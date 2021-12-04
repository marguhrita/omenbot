# Comment out lines 2 and 7 if you are not using replit.
#from keepalive import keep_alive
import discord, os, requests
from discord.ext import commands
import schedule, time, asyncio
from datetime import datetime
#from replit import database
from dateutil import parser as dateparser
# SELF HOST:

import aiofiles


musiclist = []
isplaying = False



intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.voice_states = True


client = commands.Bot(command_prefix='-', intents = intents, activity=discord.Game(" with your emotions"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def startup():
    await client.wait_until_ready()

client.loop.create_task(startup())


@client.command(name = "reminder")
@commands.has_any_role("botdev", "Admin")
async def manual_reminder(ctx, work, time_due, day_due="today"):
    reminderChannel = client.get_channel(898163614312181761)
    await reminderChannel.send("<@&898942341405106258> Don't forget the {0} due {1} at {2}!".format(work, day_due, time_due))
    await ctx.send("Reminder sent")

 

#<----------------------------------------------------->

def inspiroquote():
  response = requests.get("https://inspirobot.me/api?generate=true")
  quote = response.text
  return quote

@client.command(name = "inspiration", aliases=["inspire", "motivation"])
async def inspiration(ctx):
  await ctx.send(str(inspiroquote()))








extensions = ["cogs.Music"]

if __name__ =='__main__':
  print("loading cogs...")
  for e in extensions:
    client.load_extension(e)
    
#<----------------------------------------------------->
keep_alive()

client.run(os.getenv("TOKEN"))

