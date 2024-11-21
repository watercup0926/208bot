import json

import discord
from discord import app_commands
from discord.ext import commands
from drink import share_user_data  # noqa: F401


# Function to read user data from JSON file
def read():
    try:
        with open("user_data.json", "r", encoding="UTF-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if the file is missing or corrupt
        return {}


# Function to write user data to JSON file
def write(data):
    with open("user_data.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="檢查存款", description="檢查餘額")
    async def pay(self, interaction: discord.Interaction):
        data = read()
        user = str(interaction.user.id)  # Convert user ID to a string for JSON

        # Check if the user exists in data; if not, set their balance to 0
        if user not in data:
            data[user] = 0
            write(data)  # Save the new user with a balance of 0

        # Send the balance as a response
        await interaction.response.send_message(f"你剩 {data[user]} 元", ephemeral=True)

    @app_commands.command(name="存款", description="存款")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        data = read()
        user = str(interaction.user.id)  # Convert user ID to a string for JSON

        # Check if the user exists in data; if not, set their balance to 0
        if user not in data:
            data[user] = 0

        # Deposit the specified amount
        data[user] += amount
        write(data)  # Save the updated balance

        # Send a confirmation message
        await interaction.response.send_message(
            f"你存了 {amount} 元，現在剩 {data[user]} 元", ephemeral=True
        )

    @app_commands.command(name="全部存款", description="所有人的存款")
    async def bank(self, interaction: discord.Interaction):
        data = read()
        await interaction.response.send_message(f"大家的存款是{data}")
        for user in data.values():
            await interaction.followup.send()

    # Setup function to add the cog to the bot


async def setup(bot):
    await bot.add_cog(Payment(bot))
