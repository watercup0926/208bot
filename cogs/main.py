import discord
from discord.ext import commands
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def Hello(self, ctx: commands.Context):
        await ctx.send("Hello, world!")



async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))