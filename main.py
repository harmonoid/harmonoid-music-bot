# bot.py
import os

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
import harmonoidservice as hs
import logging

logging.basicConfig(level=logging.DEBUG, filename='harmonoid-bot.log')

TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.AutoShardedBot(command_prefix='!')

harmonoid = hs.HarmonoidService()

vc = []
vc_id = []

error = 0

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#@bot.command()
#async def download(ctx, *, arg):
#    if ctx.author == bot.user:
#        return
#
#    await ctx.message.channel.send(file = discord.File(fp = await harmonoid.trackDownload(trackName = arg, trackId=None, albumId=None)))

@bot.command()
async def play(ctx, *, arg):
    global vc
    global vc_id
    global error
    
    if ctx.author == bot.user:
        return
    
    try:
        filename = await harmonoid.trackDownload(trackName = arg, trackId=None, albumId=None)
        if not filename:
            await ctx.send("Sorry, but we couldn't retrieve data for track")
            return
    except:
        await ctx.send(f"Sorry, but there was an Internal Server Error :cry: ! Please report it to our maintainers! Unique error code: {error}")
        logging.exception("\n\n--------\n\nException number "+str(error)+": ")
        error += 1
        print(f"[track-download] {e}")
        return 500

    try:
        channel = discord.utils.get(ctx.guild.channels, name="Music")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
    except:
        await ctx.send("No voice channel called Music! Please create one!")
        return 
    
    server_id = ctx.message.guild.id
    
    if server_id not in vc_id:
        print("[server-append] Server was not appended!")
        vc1 = await channel.connect()
        vc.append(vc1)
        vc_id.append(server_id)
    
    vcid = vc_id.index(server_id)
    
    try:
        vc[vcid].play(discord.FFmpegPCMAudio(filename["trackId"]+".ogg"), after=lambda e: print('[ffmpeg-player] Successfully summoned FFMPEG player!', e))
    except:
        try:
            vc[vcid].stop()
            vc[vcid].play(discord.FFmpegPCMAudio(filename["trackId"]+".ogg"), after=lambda e: print('[ffmpeg-player] Successfully summoned FFMPEG player!', e))
        except:
            print(f"Failed to summon FFMPEG player - Exception: ", e)
            logging.exception("\n\n--------\n\nException number "+str(error)+": ")
            ctx.send(f"Failed to summon a player :cry: ! Please report a problem to our maintainers! Unique error code {error-1}")
            error += 1
            return
    
    if (len(channel.members) == 1):
        await ctx.send("Come and join me in the voice channel")
    try:
        await embedNow(music = filename, ctx = ctx)
    except Exception as e:
        print(f"[embed-exception] Exception: {e}")
        await ctx.send("Failed to summon an embed :sad: ! Well, the song is still playing :wink: ")

@bot.command()
async def play_yt(ctx, *, arg):
    global vc
    global vc_id
    
    try:
        await harmonoid.youtube.getJS()
    except:
        print(f"Failed to get JS: {e}")
        logging.exception("\n\n--------\n\nException number "+str(error)+": ")
        error += 1
        await ctx.send(f"Failed to get JS from player :sad: ! Trying to continue! Code to report to maintainers: {error-1}")
    
    
    if ctx.author == bot.user:
        return
    
    try:
        filename = await harmonoid.YTdownload(trackName = arg)
    except:
        await ctx.send(f"Sorry, but there was an Internal Server Error! Please report it to our maintainers! Unique error ID: {error}")
        logging.exception("\n\n--------\n\nException number "+str(error)+": ")
        error += 1
        print(f"[track-download] {e}")
        return 

    try:
        channel = discord.utils.get(ctx.guild.channels, name="Music")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
    except:
        await ctx.send("No voice channel called Music! Please create one!")
        return 
    
    server_id = ctx.message.guild.id
    
    if server_id not in vc_id:
        try:
            print("[server-append] Server was not appended!")
            vc1 = await channel.connect()
            vc.append(vc1)
            vc_id.append(server_id)
        except:
            await ctx.send("Failed to join a voice channel :cry: ! Our developers would have to reboot the server now! Please try to use command !refresh")
            return 
    
    vcid = vc_id.index(server_id)
    
    try:
        vc[vcid].play(discord.FFmpegPCMAudio(filename["trackId"]+".ogg"), after=lambda e: print('[ffmpeg-player] Successfully summoned FFMPEG player!', e))
    except:
        try:
            vc[vcid].stop()
            vc[vcid].play(discord.FFmpegPCMAudio(filename["trackId"]+".ogg"), after=lambda e: print('[ffmpeg-player] Successfully summoned FFMPEG player!', e))
        except:
            print(f"Failed to summon FFMPEG player - Exception: ", e)
            logging.exception("\n\n--------\n\nException number "+str(error)+": ")
            error += 1
            ctx.send(f"Failed to summon a player :cry: ! Please report a problem to our maintainers! Unique error code {error-1}")
            return 
    
    if (len(channel.members) == 1):
        await ctx.send("Come and join me in the voice channel")
    try:
        await embedNowYT(music = filename, ctx = ctx)
    except Exception as e:
        print(f"[embed-exception] Exception: {e}")
        await ctx.send("Failed to summon an embed :sad: ! But the song is still playing :wink: ")

@bot.command()
async def stop(ctx):
    server_id = ctx.message.guild.id
    vcid = vc_id.index(server_id)
    if vcid != None:
        if vc[vcid].is_playing():
            vc[vcid].stop()
            await ctx.send("Okay")
        else:
            await ctx.send("Cannot stop! No song is playing!")

@bot.command()
async def pause(ctx):
    server_id = ctx.message.guild.id
    vcid = vc_id.index(server_id)
    if vcid != None:
        if vc[vcid].is_playing():
            vc[vcid].pause()
            await ctx.send("Okay")
        else:
            await ctx.send("Cannot pause! No song is playing!")

@bot.command()
async def resume(ctx):
    server_id = ctx.message.guild.id
    vcid = vc_id.index(server_id)
    if vcid != None:
        vc[vcid].resume()
        await ctx.send("Okay")
        
@bot.command()
async def refresh(ctx):
    global vc
    global vc_id
    vcid = vc_id.index(ctx.message.guild.id)
    
    try:
        vc_id.remove(ctx.message.guild.id)
    except:
        print("Server wasn't in list of servers, so it can't be refreshed!")
    
    try:
        vc[vcid].stop()
    except:
        print("Couldn't stop!")
    
    try:
        vc[vcid].disconnect()
    except:
        print("Couldn't disconnect from a voice channel!")
    
    #try:
    #    np[vcid] = None
    #except Exception as e:
    #    print(e)
        
    
    try:
        del vc[vcid]
    except:
        print("Server wasn't in list of servers, so it can't be refreshed!")
    
    await ctx.send("Succesfully refreshed server with ID: "+str(ctx.message.guild.id))
    
async def embedNowYT(music, ctx):
    embed=discord.Embed(title="Now playing:", description=f"**[{music['title']}]({music['url']})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music["thumbnail"])
    embed.add_field(name="Requested by:", value=f"`{ctx.author.name}`", inline=True)
    embed.add_field(name="Duration:", value=f"`{music['duration']}`", inline=True)
    await ctx.send(embed=embed)

async def embedNow(music, ctx):
    trackDur = music["trackDuration"]
    url = "https://music.youtube.com/watch?v="+music["trackId"]
                    
    embed=discord.Embed(title="Now playing :", description=f"**[{music['trackName']}]({url})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music["albumArtHigh"])
    embed.add_field(name="Requested by :", value=f"`{ctx.author.name}`", inline=True)
    embed.add_field(name="Duration :", value=f"`{trackDur//60}:{trackDur%60}`", inline=True)
    
    embed.add_field(name="Album name :", value=f"`{music['albumName']}`", inline=True)
    embed.add_field(name="Year :", value=f"`{music['year']}`", inline=True)
    
    embed.add_field(name="Artists :", value=f"`{', '.join(music['trackArtistNames'])}`", inline=True)
    
    
    await ctx.send(embed=embed)

@bot.command()
async def lyrics(ctx, *, arg):
    lyrics = await harmonoid.getLyrics(trackName = arg, trackId = None)
    if lyrics["lyricsFound"] == True:
        lyrics = lyrics["lyrics"]
        if (len(lyrics) > 1999):
            await ctx.send("Lyrics are longer than 2000 characters... Please use !lyricsSend to send lyrics in .txt file")
        else:
            await ctx.send(lyrics)

@bot.command()
async def lyricsSend(ctx, *, arg):
    lyrics = await harmonoid.getLyrics(trackName = arg, trackId = None)
    trackId = await harmonoid.searchYoutube(keyword = arg, mode="track")
    print(trackId)
    trackId = trackId["result"][0]["trackId"]
    if os.path.isfile(f"{trackId}.txt"):
        print(
            f"[lyrics] Lyrics already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
        )
        await ctx.send(file=discord.File(trackId+".txt"))
        return
    if lyrics["lyricsFound"] == True:
        lyrics = lyrics["lyrics"]
        f = open(trackId+".txt", "w")
        f.write(lyrics)
        f.close()
        await ctx.send(file=discord.File(trackId+".txt"))
        return
                
    


bot.run(TOKEN)
