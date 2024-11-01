import json

import discord
from discord import app_commands
from discord.ext import commands


# 讀取菜單
def set_menu(shop_name):
    with open(f"{shop_name}_menu.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


# 讀取shop_json的資料
def set_shop():
    with open("shops.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


# 飲料選單
class DrinkDropdown(discord.ui.Select):
    def __init__(self, drink_list):
        # 從drink list裡面自動上選項
        options = [discord.SelectOption(label=drink) for drink in drink_list]
        super().__init__(
            placeholder="選杯飲料", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        # 把點的餐回送給使用者
        await interaction.response.send_message(
            f"You selected: {self.values[0]}", ephemeral=True
        )
				

class SugarDropdown(discord.ui.Select):
		def __init__(self, sugar_level):
				options = [discord.SelectOption(label=sugar) for sugar in sugar_level]
				super().__init__(
						placeholder="甜度",min_value=1, max_value=1,options=options
				)
		async def callback(self, interaction: discord.Interaction):

class DropdownView(discord.ui.View):
    def __init__(self, drink_list):
        super().__init__()
        self.add_item(DrinkDropdown(drink_list))

class CustomView(discord.ui.View):
		def __init__(self, sugar_level, ice_level):
				self.add_item(SugarDropdown(sugar_level))

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_name = ""
        self.shop_menu = {}
        self.categories = []
        self.shops = set_shop()
        self.shop_names = list(self.shops.keys())

    @app_commands.command(name="菜單", description="給出今天的菜單")
    async def menu(self, interaction: discord.Interaction):
        if self.shop_name:
            await interaction.response.send_message(
                self.shops[self.shop_name]["menu_url"], ephemeral=True
            )
        else:
            await interaction.response.send_message("還沒決定哪間", ephemeral=True)

    @app_commands.command(name="今日店家", description="今天要喝哪家呢?")
    @app_commands.describe(店家="選擇今天的店家")
    async def store(self, interaction: discord.Interaction, 店家: str):
        self.shop_name = 店家
        self.shop_menu = set_menu(店家)
        self.categories = list(self.shop_menu.keys())
        url = self.shops[店家]["menu_url"]
        await interaction.response.send_message(
            f"各位，今天喝{店家}喔{url}",
        )

    # Autocomplete for selecting a shop in the `store` command
    @store.autocomplete("店家")
    async def shop_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=shop, value=shop)
            for shop in self.shop_names
            if current.lower() in shop.lower()
        ]

    @app_commands.command(name="點餐", description="想喝什麼")
    @app_commands.describe(分類="你要喝什麼種類的飲料")
    async def order(self, interaction: discord.Interaction, 分類: str):
        if not self.shop_name:
            await interaction.response.send_message("尚未選擇店家。", ephemeral=True)
            return

        # Defer the interaction response to allow more time to process
        await interaction.response.defer()

        # Check if the selected category exists and fetch the drinks
        if 分類 in self.shop_menu:
            drink_names = [drink["name"] for drink in self.shop_menu[分類]]
            await interaction.followup.send(
                "請選擇你要的飲料:", view=DropdownView(drink_names)
            )
        else:
            await interaction.followup.send("該分類不存在，請重新選擇。")

    # Autocomplete function for dynamic category choices in `order`
    @order.autocomplete("分類")
    async def category_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        return [
            app_commands.Choice(name=category, value=category)
            for category in self.categories
            if current.lower() in category.lower()
        ]


# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
