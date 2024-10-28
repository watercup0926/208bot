import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from discord.app_commands import Choice
"""
名字
中杯
大杯
不可調甜度 做熱飲 不可調冰塊
"""

import os
def set_shop(name:str):
    file = open("{}.txt".format(name),'r',encoding="utf-8")
    lines = file.readlines()
    ls = []
    for i in range(1,len(lines),4):
        ls.append([lines[i],int(lines[i+1]),int(lines[i+2]),list(lines[i+3])])
    return ls
def set_menu(name:str):
    file = open("{}.txt".format(name),'r',encoding="utf-8")
    line = file.readline()
    return line
class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_name = ''
        self.shop_list = ''
        self.shop_menu = ''
        # Define a slash command
    @app_commands.command(name="菜單", description="給出今天的菜單")
    async def menu(self, interaction: discord.Interaction):
        if self.shop_name != '': 
            await interaction.response.send_message(self.shop_menu,ephemeral=True)
        else:    
            await interaction.response.send_message("還沒決定哪間")
    @app_commands.command(name="今日店家",description="今天要喝哪家呢?")
    async def store(self, interaction: discord.Interaction,店家:str):
        self.shop_name=店家
        self.shop_list=set_shop(店家)
        self.shop_menu=set_menu(店家)
        await interaction.response.send_message("各位，今天喝{}喔{}".format(店家,self.shop_menu))
    @app_commands.command(name="點餐",description='想喝什麼')
    @app_commands.describe(飲料="你要喝什麼")
    async def order(self, interaction: discord.Interaction,飲料:str):
        print()		
			
# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))