import discord
from discord.ext import commands

from source.embed import Embed
from scripts.youtube import YouTube
from scripts.youtubemusic import YouTubeMusic


class Commands(commands.Cog):
    ''' Static Members '''
    recognisedServers = []
    botStatic = None

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.youtubeMusic = YouTubeMusic()
        self.youtube = YouTube()


class Server:
    def __init__(self, context, serverId, voiceChannelId, textChannelId):
        self.context = context
        self.serverId = serverId
        self.voiceChannelId = voiceChannelId
        self.textChannelId = textChannelId
        self.voiceChannel = None
        self.voiceConnection = None
        self.isPaused = True
        self.isStopped = True
        self.queue = []

    async def getVoiceChannel(self, context, bot):
        if not self.voiceConnection:
            self.voiceChannel = bot.get_channel(discord.utils.get(context.guild.channels, name='Music').id)
            await self.connect()
        return self.voiceConnection

    async def connect(self):
        self.isPaused = False
        self.isStopped = False
        self.voiceConnection = await self.voiceChannel.connect()

    async def disconnect(self):
        self.isPaused = True
        self.isStopped = True
        await self.voiceChannel.disconnect()
        self.voiceConnection = None

    def resume(self):
        self.isPaused = False
        self.voiceConnection.resume()

    def pause(self):
        self.isPaused = True
        self.voiceConnection.pause()

    def stop(self):
        self.isStopped = True
        self.voiceConnection.stop()

    @staticmethod
    async def get(context, embed):
        for server in Commands.recognisedServers:
            if server.serverId == context.message.guild.id:
                return server
        try:
            voiceChannelId = discord.utils.get(context.guild.channels, name='Music').id
        except:
            await embed.exception(
                context,
                'Information',
                'Please make a voice channel with name "Music" first. 🔧',
                '❌'
            )
            return None
        Commands.recognisedServers.append(
            Server(
                context,
                context.message.guild.id,
                voiceChannelId,
                context.message.channel.id,
            )
        )
        return Commands.recognisedServers[-1]
