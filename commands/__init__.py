import discord
from discord.ext import commands
import asyncio

from source.embed import Embed
from scripts.youtube import YouTube
from scripts.youtubemusic import YouTubeMusic


class Lifecycle:

    @staticmethod
    async def update():
        for server in Commands.recognisedServers:
            ''' Empty Queue '''
            if not server.queue:
                continue
            ''' Not In Voice Channel '''
            if not server.voiceConnection:
                continue
            if not server.voiceConnection.is_playing() and type(server.modifiedQueueIndex) is int:
                ''' Jump on the completion of queue. '''
                if server.modifiedQueueIndex >= len(server.queue) or server.modifiedQueueIndex < 0:
                    await Embed().exception(
                        server.context,
                        'Invalid Jump',
                        f'No track is present at that index. 👀',
                        '❌'
                    )
                    server.modifiedQueueIndex = None
                    continue
                else:
                    server.queueIndex = server.modifiedQueueIndex
                    server.modifiedQueueIndex = None
            elif not server.voiceConnection.is_playing():
                ''' Track Completed '''
                if server.queueIndex >= len(server.queue):
                    continue
                else:
                    server.queueIndex += 1
            elif type(server.modifiedQueueIndex) is int:
                ''' Jump '''
                if server.modifiedQueueIndex >= len(server.queue) or server.modifiedQueueIndex < 0:
                    await Embed().exception(
                        server.context,
                        'Invalid Jump',
                        f'No track is present at that index. 👀',
                        '❌'
                    )
                    server.modifiedQueueIndex = None
                    continue
                else:
                    server.queueIndex = server.modifiedQueueIndex
                    server.modifiedQueueIndex = None
            else:
                ''' No Change '''
                continue
            ''' Track Playback '''
            track = server.queue[server.queueIndex]
            if 'trackId' in server.queue[server.queueIndex].keys():
                ''' Queue item is track. '''
                trackFile = f'{server.queue[server.queueIndex]["trackId"]}.webm'
            else:
                ''' Queue item is video. '''
                trackFile = f'{server.queue[server.queueIndex]["id"]}.webm'
            FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            url = await YouTube().fetchURL(server.queue[server.queueIndex], 251)
            try:
                server.voiceConnection.play(
                    discord.FFmpegOpusAudio(url, **FFMPEG_OPTS),
                    after = lambda exception: asyncio.run_coroutine_threadsafe(
                        Commands.listenUpdates(), Commands.bot.loop
                    ),
                )
                ''' Run mainloop after playback completion. '''
            except:
                try:
                    server.stop()
                    server.voiceConnection.play(
                        discord.FFmpegOpusAudio(url, **FFMPEG_OPTS),
                        after = lambda exception: asyncio.run_coroutine_threadsafe(
                            Commands.listenUpdates(), Commands.bot.loop
                        ),
                    )
                    ''' Run mainloop after playback completion. '''
                except:
                    await Embed().exception(
                        server.context,
                        'Internal Error',
                        f'Could not start player. 📻',
                        '❌'
                    )
            ''' Displaying Metadata '''
            try:
                await Embed().nowPlaying(server.context, track)
            except:
                await Embed().exception(
                    server.context,
                    'Now Playing',
                    'Could not send track information.\nMusic is still playing. 😅',
                    '🎶'
                )



class Commands(commands.Cog):
    ''' Static Members '''
    bot = None
    recognisedServers = []

    @staticmethod
    async def listenUpdates():
        await Lifecycle.update()

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed()
        self.youtubeMusic = YouTubeMusic()
        self.youtube = YouTube()


class Server:

    def __init__(self, context, serverId, textChannel, voiceChannel, voiceChannelName):
        self.context = context
        self.serverId = serverId
        self.textChannel = textChannel
        self.voiceChannel = voiceChannel
        self.voiceChannelName = voiceChannelName
        self.voiceConnection = None
        self.queueIndex = -1
        self.modifiedQueueIndex = None
        self.queue = []

    async def connect(self):
        if not self.voiceConnection:
            self.voiceConnection = await self.voiceChannel.connect()

    async def disconnect(self):
        await self.voiceConnection.disconnect()
        self.voiceConnection = None
        self.queueIndex = -1
        self.modifiedQueueIndex = None
    
    def resume(self):
        self.voiceConnection.resume()

    def pause(self):
        self.voiceConnection.pause()

    def stop(self):
        self.voiceConnection.stop()

    async def changeChannel(self, context, voiceChannelName):
        voiceChannel = Commands.bot.get_channel(discord.utils.get(context.guild.channels, name = voiceChannelName).id)
        if not voiceChannel:
            await Embed().exception(
                context,
                'Information',
                f'Please make a voice channel with name "{voiceChannelName}" first. 🔧',
                '❌'
            )
            return None
        if self.voiceChannelName != voiceChannelName and voiceChannel:
            self.voiceChannel = voiceChannel
            self.voiceChannelName = voiceChannelName
            if self.voiceConnection:
                await self.disconnect()
                await self.connect()
            else:
                await self.connect()


    @staticmethod
    async def get(context):
        asyncio.ensure_future(context.message.add_reaction('👀'))
        for server in Commands.recognisedServers:
            if server.serverId == context.message.guild.id:
                ''' Update textChannel where the newest command is detected. '''
                server.textChannel = Commands.bot.get_channel(context.message.channel.id)
                return server
        voiceChannelKey = discord.utils.get(context.guild.channels, name = 'Music')
        if voiceChannelKey:
            serverId = context.message.guild.id
            textChannel = Commands.bot.get_channel(context.message.channel.id)
            voiceChannel = Commands.bot.get_channel(voiceChannelKey.id)
            Commands.recognisedServers.append(
                Server(
                    context,
                    serverId,
                    textChannel,
                    voiceChannel,
                    'Music',
                )
            )
            return Commands.recognisedServers[-1]
        else:
            await Embed().exception(
                context,
                'Information',
                f'Please make a voice channel with name "Music" first or use -changeChannel command. 🔧',
                '❌'
            )
            return None
