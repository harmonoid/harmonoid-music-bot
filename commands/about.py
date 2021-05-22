from commands import *


class About(Commands):
    def __init__(self):
        super().__init__(Commands.bot)
        
    @commands.command()
    async def about(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.about(ctx)

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.help(ctx)

    @commands.command()
    async def status(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        await self.embed.status(ctx, Commands)
