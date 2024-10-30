import discord
import os
import json
from discord.ext import commands
from discord import app_commands
from typing import Literal

# Reading JSON
def set_menu(shop_name):
    with open(f"{shop_name}_menu.json", "r") as f:
        data = json.load(f)
    return data

class DrinkDropdown(discord.ui.Select):
    def __init__(self, drink_list):
        # Create options dynamically from the fruit list
        options = [discord.SelectOption(label="drink", description=f"Choose {fruit}") for fruit in drink_list]
        
        # Initialize the dropdown
        super().__init__(placeholder="Choose a drink...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected: {self.values[0]}")

class DropdownView(discord.ui.View):
    def __init__(self, drink_list):
        super().__init__()
        # Add a FruitDropdown instance to the view, populated with fruit_list
        self.add_item(DrinkDropdown(drink_list))

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_name = ''
        self.shop_menu = {}
        self.categories = []

    @app_commands.command(name="菜單", description="給出今天的菜單")
    async def menu(self, interaction: discord.Interaction):
        if self.shop_name:
            await interaction.response.send_message(self.shop_menu, ephemeral=True)
        else:
            await interaction.response.send_message("還沒決定哪間")

    @app_commands.command(name="今日店家", description="今天要喝哪家呢?")
    async def store(self, interaction: discord.Interaction, 店家: str):
        self.shop_name = 店家
        self.shop_menu = set_menu(店家)
        self.categories = list(self.shop_menu.keys())
        await interaction.response.send_message(f"各位，今天喝{店家}喔")

    @app_commands.command(name="點餐", description="想喝什麼")
    @app_commands.describe(分類="你要喝什麼種類的飲料")
    async def order(self, interaction: discord.Interaction, 分類: str):
        if self.shop_name:
            await interaction.response.send_messageZ(f"您選擇了: {分類}")
            await interaction.response.send_message("Please choose a drink:", view=DropdownView())
        else:
            await interaction.response.send_message("尚未選擇店家。")


    # Autocomplete function for dynamic category choices
    @order.autocomplete("分類")
    async def category_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=category, value=category)
            for category in self.categories if current.lower() in category.lower()
        ]
    @commands.command(name="choose_drink", description="Choose a drink from the dropdown")

        

    
# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))