import json

import discord
from discord import app_commands
from discord.ext import commands

# 定義全域變數
ice_level = []
sugar_level = []

def get_drink_sizes_and_prices(menu_data: dict, drink_name):
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
    print("can't find a data")
    return {}


def get_drink_data(menu_data: dict, drink_name: str) -> bool:
    # 遍歷所有分類
    for category in menu_data.values():
        # 在每個分類中尋找指定飲料
        for drink in category:
            if drink["name"] == drink_name:
                return drink["options"]
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
def get_drink_addons(menu_data: dict) -> dict:
    addons = {}
    for i in range(0,21,5):
        addons[f"add_{i}"] = menu_data[f"add_{i}"]
    return addons

# 飲料選單
class DrinkDropdown(discord.ui.Select):
    def __init__(self, drink_list, cog):
        self.cog = cog
        options = [discord.SelectOption(label=drink) for drink in drink_list]
        super().__init__(
            placeholder="選擇飲料", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            # 獲取當前店家的冰塊和甜度選項
            ice_options = self.cog.shops[self.cog.shop_name]["ice_level"]
            sugar_options = self.cog.shops[self.cog.shop_name]["sugar_level"]
            drink_data = get_drink_data(self.cog.shop_menu, self.values[0])
            size_and_price = get_drink_sizes_and_prices(
                self.cog.shop_menu, self.values[0]
            )

            self.cog.user_data[interaction.user.id] = {
                "drink_name": self.values[0],
                "ice": None,
                "sugar": None,
                "size": None,
                "price": None,
                "addon": [],
            }

            if drink_data["custom_ice"] is False:
                self.cog.user_data[interaction.user.id]["ice"] = "不可調"
            if drink_data["custom_sugar"] is False:
                self.cog.user_data[interaction.user.id]["sugar"] = "不可調"
            if size_and_price and len(size_and_price) == 1:
                size = list(size_and_price.keys())[0]
                price = list(size_and_price.values())[0]
                self.cog.user_data[interaction.user.id]["size"] = size
                self.cog.user_data[interaction.user.id]["price"] = price

            # 創建自訂視窗，確保傳遞所有必要參數
            custom_view = CustomView(
                ice_options, sugar_options, drink_data, size_and_price, self.cog
            )

            # 發送選項
            await interaction.response.send_message(
                f"你選擇了: {self.values[0]}\n請選擇甜度和冰塊：",
                view=custom_view,
                ephemeral=True,
            )
        except Exception as e:
            print(f"Drink callback 錯誤: {e}")
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
        self.cog.user_data[interaction.user.id]["ice"] = self.values[0]
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
        self.cog.user_data[interaction.user.id]["sugar"] = self.values[0]
        await interaction.response.send_message(
            f"你選擇了: {self.values[0]}", ephemeral=True
        )


class SizeDropdown(discord.ui.Select):
    def __init__(self, sizes_and_prices: dict, cog):
        self.cog = cog
        self.data = sizes_and_prices if sizes_and_prices else {}  # 防止None
        options = []

        try:
            options = [
                discord.SelectOption(label=size, description=f"Price: {price}")
                for size, price in self.data.items()
            ]
        except Exception as e:
            print(f"建立size選項時發生錯誤: {e}")
            options = [discord.SelectOption(label="錯誤", description="無法載入選項")]

        super().__init__(
            placeholder="選擇大小",
            min_values=1,
            max_values=1,
            options=options
            or [
                discord.SelectOption(label="預設", description="Price: 0")
            ],  # 防止空選項
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            selected_size = self.values[0]
            if selected_size == "錯誤" or selected_size == "預設":
                await interaction.response.send_message(
                    "選項載入錯誤，請重試", ephemeral=True
                )
                return

            self.cog.user_data[interaction.user.id]["size"] = selected_size
            self.cog.user_data[interaction.user.id]["price"] = self.data[selected_size]
            await interaction.response.send_message(
                f"你選擇了 {selected_size}, 價格: {self.data[selected_size]}",
                ephemeral=True,
            )
        except Exception as e:
            print(f"Size callback錯誤: {e}")
            await interaction.response.send_message(
                "處理選擇時發生錯誤", ephemeral=True
            )


class DropdownView(discord.ui.View):
    def __init__(self, drink_list, cog):
        super().__init__()
        self.add_item(DrinkDropdown(drink_list, cog))


class CustomView(discord.ui.View):
    def __init__(self, ice_level, sugar_level, drink_data, sizes_and_prices, cog):
        super().__init__()
        self.cog = cog
        sizes = sizes_and_prices
        # 只在需要時添加選項
        if drink_data.get("custom_ice", True):
            self.add_item(
                IceDropdown(ice_level, drink_data.get("hot_available", False), cog)
            )
        if drink_data.get("custom_sugar", True):
            self.add_item(SugarDropdown(sugar_level, cog))
        if len(sizes) > 1:
            self.add_item(SizeDropdown(sizes, cog))
        for i in range(0, 21, 5):
            if self.cog.addons[f"add_{i}"] is not None:
                for addon in self.cog.addons[f"add_{i}"]:
                    self.add_item(AddonButton(addon, i, self.cog))
                    print(addon)

        self.timeout = 120  # 設置視窗超時時間

class AddonButton(discord.ui.Button):
    def __init__(self, addon, price, cog):
        super().__init__(label=f"+{price}{addon}", style=discord.ButtonStyle.primary)
        self.addon = addon
        self.cog = cog
        self.price = price

    async def callback(self, interaction: discord.Interaction):
        self.cog.user_data[interaction.user.id]["addon"].append(self.addon)
        self.cog.user_data[interaction.user.id]["price"] += self.price
        await interaction.response.send_message(f'你加了 {self.addon}', ephemeral=True)


class Drink_order(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_name = ""
        self.addons = {}
        self.shop_menu = {}
        self.categories = []
        self.shops = set_shop()
        self.shop_names = list(self.shops.keys())
        self.user_data = {}

    @app_commands.command(name="菜單", description="給出今天的菜單")
    async def menu(self, interaction: discord.Interaction):
        if self.shop_name:
            url = self.shops[self.shop_name]["menu_url"]
            embed = discord.Embed(title=f"{self.shop_name} 的菜單")
            embed.set_image(url=url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("還沒決定哪間", ephemeral=True)

    @app_commands.command(name="顯示點單", description="顯示大家點的東西")
    async def show_user_data(self, interaction: discord.Interaction):
        print(self.user_data)
        if self.user_data:
            for user_id, user_data in self.user_data.items():
                member = interaction.guild.get_member(user_id)
                if member:
                    await interaction.response.send_message(
                        f"姓名: {member.mention}\n"
                        f"飲料: {user_data['drink_name']}\n"
                        f"冰塊: {user_data['ice']}\n"
                        f"甜度: {user_data['sugar']}\n"
                        f"大小: {user_data['size']}\n"
                        f"價格: {user_data['price']}\n"
                        f"加料: {user_data['addon']}",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"無法找到用戶 ID: {user_id}", ephemeral=True
                    )
        else:
            await interaction.response.send_message("目前沒有用戶資料")

    @app_commands.command(name="今日店家", description="今天要喝哪家呢?")
    @app_commands.describe(店家="選擇今天的店家")
    async def store(self, interaction: discord.Interaction, 店家: str):
        global ice_level, sugar_level
        self.shop_name = 店家
        self.shop_menu = set_menu(店家)
        self.categories = list(self.shop_menu.keys())
        self.addons = get_drink_addons(self.shops[店家])
        print(店家)
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
        await interaction.response.defer(ephemeral=True)

        # Check if the selected category exists and fetch the drinks
        if 分類 in self.shop_menu:
            drink_names = [drink["name"] for drink in self.shop_menu[分類]]
            await interaction.followup.send(
                "請選擇你要的飲料:",
                view=DropdownView(drink_names, self),
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                "該分類不存在，請重新選擇。", ephemeral=True
            )

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
    await bot.add_cog(Drink_order(bot))
