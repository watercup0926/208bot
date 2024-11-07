import json

import discord
from discord import app_commands
from discord.ext import commands

# 定義全域變數
ice_level = []
sugar_level = []


def get_drink_hot_available(menu_data: dict, drink_name: str) -> bool:
    # 遍歷所有分類
    for category in menu_data.values():
        # 在每個分類中尋找指定飲料
        for drink in category:
            if drink["name"] == drink_name:
                return drink["options"]["hot_available"]
    return False

# 讀取菜單
def set_menu(shop_name):
    with open(f"shops/{shop_name}_menu.json", "r", encoding="UTF-8") as f:
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
        try:
            if not drink_list:
                options = [discord.SelectOption(label="無可用飲料")]
            else:
                options = [
                    discord.SelectOption(label=drink, value=drink)
                    for drink in drink_list
                ]
            super().__init__(
                placeholder="選擇飲料", min_values=1, max_values=1, options=options
            )
        except Exception as e:
            print(f"DrinkDropdown 初始化錯誤: {e}")
            super().__init__(
                placeholder="選單載入失敗", options=[discord.SelectOption(label="錯誤")]
            )

    async def callback(self, interaction: discord.Interaction):
        try:
            # 獲取 Cog 實例
            cog = interaction.client.get_cog("Slash")

            # 獲取當前店家的冰塊和甜度選項
            ice_options = cog.shops[cog.shop_name]["ice_level"]
            sugar_options = cog.shops[cog.shop_name]["sugar_level"]
            hot_available = get_drink_hot_available(cog.shop_menu, self.values[0])
            sizes_and_prices = cog.get_drink_sizes_and_prices(cog.shop_name, self.values[0])

            cog.user_data[interaction.user.id] = {
                "drink_name": self.values[0],
                "ice": None,
                "sugar": None,
                "size": None,
                "price": None
            }

            # 創建自訂視窗
            custom_view = CustomView(cog, ice_options, sugar_options, hot_available, sizes_and_prices)

            # 發送選項
            await interaction.response.send_message(
                f"你選擇了: {self.values[0]}\n請選擇甜度和冰塊：",
                view=custom_view,
                ephemeral=True,
            )
        except Exception as e:
            print(f"Callback 錯誤: {e}")
            await interaction.response.send_message("選擇處理發生錯誤", ephemeral=True)


class IceDropdown(discord.ui.Select):
    def __init__(self, ice_level, hot_available, cog):
        self.cog = cog  # Store cog as an instance variable
        # 從ice level裡面自動上選項
        options = [discord.SelectOption(label=ice) for ice in ice_level]
        if hot_available:
            options.append(discord.SelectOption(label="熱飲"))
        super().__init__(
            placeholder="冰塊", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.cog.user_data[interaction.user.id]['ice'] = self.values[0]
        await interaction.response.send_message(
            f"你選擇了: {self.values[0]}", ephemeral=True
        )


class SugarDropdown(discord.ui.Select):
    def __init__(self, sugar_level, cog):
        self.cog = cog  # Store cog as an instance variable
        options = [discord.SelectOption(label=sugar) for sugar in sugar_level]
        super().__init__(
            placeholder="甜度", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.cog.user_data[interaction.user.id]['sugar'] = self.values[0]
        await interaction.response.send_message(
            f"你選擇了: {self.values[0]}", ephemeral=True
        )


class SizeDropdown(discord.ui.Select):
    def __init__(self, sizes_and_prices, cog):
        self.cog = cog  # Store cog as an instance variable
        self.data = sizes_and_prices
        options = [
            discord.SelectOption(label=size, description=f"Price: {price}")
            for size, price in sizes_and_prices.items()
        ]
        super().__init__(placeholder="Choose a size...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_size = self.values[0]
        self.cog.user_data[interaction.user.id]['size'] = selected_size
        self.cog.user_data[interaction.user.id]['price'] = self.data[self.values[0]]
        await interaction.response.send_message(f"You selected {selected_size},{self.cog.user_data}", ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, drink_list):
        super().__init__()
        self.add_item(DrinkDropdown(drink_list))


class CustomView(discord.ui.View):
    def __init__(self, cog, ice_level, sugar_level, hot_available, sizes_and_prices):
        super().__init__()
        self.cog = cog
        if ice_level:
            self.add_item(IceDropdown(ice_level, hot_available, cog))
        if sugar_level:
            self.add_item(SugarDropdown(sugar_level, cog))
        if sizes_and_prices:
            self.add_item(SizeDropdown(sizes_and_prices, cog))


class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_name = ""
        self.shop_menu = {}
        self.categories = []
        self.shops = set_shop()
        self.shop_names = list(self.shops.keys())
        self.user_data = {}

    def get_drink_sizes(self, shop_name, drink_name):
        menu_data = set_menu(shop_name)
        for category in menu_data.values():
            for drink in category:
                if drink["name"] == drink_name:
                    sizes = []
                    if drink["medium_price"] is not None:
                        sizes.append("medium")
                    if drink["large_price"] is not None:
                        sizes.append("large")
                    if drink["bottle_price"] is not None:
                        sizes.append("bottle")
                    return sizes
        return

    def get_drink_sizes_and_prices(self, shop_name, drink_name):
        menu_data = set_menu(shop_name)
        for category in menu_data.values():
            for drink in category:
                if drink["name"] == drink_name:
                    sizes_and_prices = {}
                    if drink["medium_price"] is not None:
                        sizes_and_prices["medium"] = drink["medium_price"]
                    if drink["large_price"] is not None:
                        sizes_and_prices["large"] = drink["large_price"]
                    if drink["bottle_price"] is not None:
                        sizes_and_prices["bottle"] = drink["bottle_price"]
                    return sizes_and_prices
        return {}

    @app_commands.command(name="菜單", description="給出今天的菜單")
    async def menu(self, interaction: discord.Interaction):
        if self.shop_name:
            url = self.shops[self.shop_name]["menu_url"]
            embed = discord.Embed(title=f"{self.shop_name} 的菜單")
            embed.set_image(url=url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("還沒決定哪間", ephemeral=True)

    @app_commands.command(name="今日店家", description="今天要喝哪家呢?")
    @app_commands.describe(店家="選擇今天的店家")
    async def store(self, interaction: discord.Interaction, 店家: str):
        global ice_level, sugar_level
        self.shop_name = 店家
        self.shop_menu = set_menu(店家)
        self.categories = list(self.shop_menu.keys())
        print(self.categories)
        ice_level = self.shops[店家]["ice_level"]
        sugar_level = self.shops[店家]["sugar_level"]
        url = self.shops[店家]["menu_url"]
        embed = discord.Embed(title=f"各位，今天喝{店家}喔")
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    # Autocomplete for selecting a shop in the `store` command
    @store.autocomplete("店家")
    async def shop_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=shop, value=shop)
            for shop in self.shop_names
            if current.lower() in shop.lower()
        ]

    @app_commands.command(name="點餐", description="想喝什麼")
    @app_commands.describe(分類="選擇飲料分類")
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
        if not self.categories:
            return []
        return [
            app_commands.Choice(name=category, value=category)
            for category in self.categories
            if current.lower() in category.lower()
        ]

# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
