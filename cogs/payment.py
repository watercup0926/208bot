import json

import discord
from discord import app_commands
from discord.ext import commands


def load():
    with open("shops.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def save(data):
    with open("shops.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready.")

    @app_commands.command(name="查詢餘額", description="讓我看看你的餘額吧")
    async def pay(self, interaction: discord.Interaction):
        await interaction.response(self.data[str(interaction.user.id)]["balance"])


def setup(bot):
    bot.add_cog(Payment(bot))
