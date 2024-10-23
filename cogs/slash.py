import discord
from discord.ext import commands
from discord import app_commands

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Define a slash command
    @app_commands.command(name="hello", description="Responds with 'Hello, world!'")
    async def hello(self, interaction: discord.Interaction):
        """Responds with 'Hello, world!' when invoked by a slash command."""
        await interaction.response.send_message("Hello, world!")

# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
