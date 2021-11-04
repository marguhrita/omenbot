from discord.ext import commands, tasks
import asyncio
import discord, time
from discord.ext.commands.errors import CommandRegistrationError
from youtubesearchpython import VideosSearch
from pytube import YouTube
import DiscordUtils



music = DiscordUtils.Music()


musiclist = []
isplaying = False
musicChannel = None
musicTextChannel = None




def YTVideoSearch(searchterm):
  #searches for video url on yt
    videosSearch = VideosSearch(searchterm, limit = 2)
    
    videoUrl = videosSearch.result()['result'][0]['link']
    print(videoUrl)
    return videoUrl

   

    

def YTVideoDuration(searchterm):
  #searches for video url on yt
    videosSearch = VideosSearch(searchterm, limit = 2)
    time = videosSearch.result()['result'][0]['duration']
    splitTime=time.split(":")
    duration = 60*(splitTime[0]) + splitTime[1]

    return duration


def takeANap(duration):

    global isplaying
    global musiclist

    print("Song timer started")
    isplaying = True
    time.sleep(duration)
    print("song timer ended")
    print(musiclist.pop(0))
    isplaying=False
    
    print(musiclist)

class Music(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  async def sendEmbed(self, channel, whoJoined, colour, joinstate):
    vclogchannel = self.client.get_channel(channel)
    achannel = joinstate + " " + str(channel)
    whoJoined = str(whoJoined)
    embedVar = discord.Embed(title=achannel, description=whoJoined, color=colour)
    embedVar.set_footer(text="omenbot logging")
    await vclogchannel.send(embed=embedVar)

  @commands.Cog.listener()
  async def on_ready(self):
    return
    #self.musicPlayer.start()


  @commands.command()
  async def diagnostics(self,ctx):
    global isplaying
    global musicChannel
    await ctx.send(isplaying)
    await ctx.send(musicChannel)

    

  @commands.command(name = "play", aliases=  ["p", "Play", "P"])
  async def play(self, ctx, *, url):

    voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)


    if voice == None:
      await ctx.author.voice.channel.connect()
    """"
    argsplit = arg.split(":")
    
    if argsplit[0] != "https":
      url = YTVideoSearch(arg)
    else:
      arg = url
    """

    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
      player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
      await player.queue(url, search=True)
      song = await player.play()
      await ctx.send("Now playing " + url)
    else:
      await player.queue(url, search=True)
      await ctx.send("Added " + url + " to the queue")
      
    

  @commands.command(name = "queue", aliases = ["q", "Q", "Queue"])
  async def musicQueue(self,ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    print(player.current_queue()[0])
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")
  
  @commands.command()
  async def skip(self, ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")
      
  @commands.command(name="disconnect", aliases = ["dc", "fuckoff", "leave"])
  async def leaveCall(self,ctx):
    await ctx.voice_client.disconnect()

  @commands.command()
  async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")

  @commands.command()
  async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

  @tasks.loop(seconds=5.0)
  async def musicPlayer(self):
    global musiclist
    global isplaying
    global musicChannel

    if isplaying == False and len(musiclist) != 0:

      try:
        print("Playing song")
        print(musicChannel)
        YTVideoSearch(musiclist[0])
        print(musiclist)
        musicChannel.play(discord.FFmpegPCMAudio("ytdl/download.mp3"))
        takeANap(YTVideoDuration(musiclist[0]))

        
        

       
      except:
        #print("error playing...")
        return
      
      

def setup(client):
  client.add_cog(Music(client))


    
  

    
   




