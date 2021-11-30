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

# REPL.IT:
'''
db = database.AsyncDatabase(os.getenv("REPLIT_DB_URL"))
'''

async def quizReminders():
  reminderChannel = client.get_channel(898163614312181761)  # DEV 897945396167467098

  #await reminderChannel.send("~ RESTARTED ~")

  
  #os.environ["LAST_REMINDER"] = "0001-01-01 00:00:00.000000"
  #await db.set("last_reminder", datetime.min.isoformat())

  while not client.is_closed():
      now = datetime.now()
      weekday = now.weekday()
      
      # SELF HOST:
      
      async with aiofiles.open("last_reminder.txt", "r") as f:
          last_reminder = dateparser.isoparse((await f.readline()).strip())
      
      
      # REPL.IT:
      '''
      last_reminder = dateparser.isoparse(await db.get("last_reminder")) 
      '''

      if now.date() > last_reminder.date() and now.hour >= 8: # Don't remind multiple times per day, don't remind in the middle of the night or early morning.
          if weekday == 1: # Tuesday Tutorials
              await reminderChannel.send("<@&898942341405106258> Don't forget the tutorial assingments due today at 4pm!")
              last_reminder=now
          if weekday == 2: # Wednesday FP
              await reminderChannel.send("<@&898942341405106258> Don't forget the FP quiz due today at 4pm!")
              last_reminder=now
          if weekday == 3: # Thursday ILA
              await reminderChannel.send("<@&898942341405106258> Don't forget the ILA quiz due today at 12 noon!")
              last_reminder=now
          elif weekday == 5: # Saturday CL
             await reminderChannel.send("<@&898942341405106258> Don't forget the CL quiz due today at 4pm!")
             last_reminder=now
      else:
          pass #await reminderChannel.send("Not sending reminder. now={}; last_remider={}".format(now, last_reminder))
      #os.environ["LAST_REMINDER"] = str(last_reminder)

      # SELF HOST:
      #'''
      async with aiofiles.open("last_reminder.txt", "w") as f:
          await f.write(last_reminder.isoformat())
      #'''
      
      # REPL.IT:
      '''
      await db.set("last_reminder", last_reminder.isoformat())
      '''

      await asyncio.sleep(3600) # 1 hour = 3600

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def startup():
    await client.wait_until_ready()
    await quizReminders()

client.loop.create_task(startup())

@client.command(name = "resetreminder")
@commands.has_any_role("botdev", "Admin")
async def resetreminder(ctx):
    await db.set("last_reminder", datetime.min.isoformat())
    await ctx.send("Reminder reset")


@client.command(name = "reminder")
@commands.has_any_role("botdev", "Admin")
async def manual_reminder(ctx, work, time_due, day_due="today" ):
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

