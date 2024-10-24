import discord
from discord.ext import commands
from discord import app_commands
list = []
class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Define a slash command
    @app_commands.command(name="點餐", description="點餐且列出來所有的項目")
    async def order(self, interaction: discord.Interaction,name:str):
        list.append(name)
        await interaction.response.send_message(list)

# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
