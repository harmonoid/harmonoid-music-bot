from commands import *
from commands.playback import Playback
from commands.controls import Controls
from commands.lyrics import Lyrics
from commands.about import About
import logging

logging.basicConfig(level=logging.INFO, filename="harmonoid-log.log")

def updateStatus(percentage: int):
    import sys

    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*percentage, percentage))
    sys.stdout.flush()

if __name__ == '__main__':
    print("Harmonoid Music Bot starting...")
    print("Please wait. This can take up to 30 seconds...")
    updateStatus(0)

    Commands.bot = commands.AutoShardedBot(
        command_prefix='-',
        help_command=None,
    )
    updateStatus(20)

    Commands.bot.add_cog(Playback())
    updateStatus(35)

    Commands.bot.add_cog(Controls())
    updateStatus(50)

    Commands.bot.add_cog(Lyrics())
    updateStatus(65)

    Commands.bot.add_cog(About())
    updateStatus(80)

    @Commands.bot.event
    async def on_ready():
        await Commands.bot.change_presence(
            activity=discord.Activity(
                name='-help 👀',
                type=3,
            ),
        )
        updateStatus(100)
        print("\nHarmonoid Music Bot is running...")
    import os
    TOKEN = os.environ.get('DISCORD_TOKEN')
    updateStatus(90)
    Commands.bot.run(TOKEN)