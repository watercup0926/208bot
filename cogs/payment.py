import json

import discord
from discord import app_commands
from discord.ext import commands


def read():
    with open("user_data.json", "r", encoding="UTF-8") as file:
        return json.load(file)


def write(data):
    with open("user_data.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)
    return


class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="檢查存款", description="檢查餘額")
    async def pay(self, interaction: discord.Interaction):
        data = read()
        user = interaction.user.id
        if user not in data:
            await interaction.response.send_message("你還沒有帳戶，創建一個", ephemeral=True)
            data[user] = 0
            write(data)
        await interaction.response.send_message(f"你剩 {data[user]} 元", ephemeral=True)    

async def setup(bot):
    await bot.add_cog(Payment(bot))
