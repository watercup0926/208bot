import discord
from discord.ext import commands
from discord import app_commands
"""
名字
中杯
大杯
不可調甜度 做熱飲 不可調冰塊
"""
import os
store = ''
def set_shop(name:str):
    file = open("{}.txt".format(name),'r',encoding="utf-8")
    lines = file.readlines()
    ls = []
    menu = ''
    for i in range(0,len(lines),4):
        ls.append([lines[i],int(lines[i+1]),int(lines[i+2]),list(lines[i+3])])
    for i in range(0,len(ls)):
        menu += "{} 中杯{} 大杯{} ".format(ls[i][0],ls[i][1],ls[i][2])
        if ls[i][3][0] == '1':
            menu += "不可調甜度 "
        if ls[i][3][1] == '1':
            menu += "可做冷飲 "
        if ls[i][3][0] == '1':
            menu += "不可調冰塊"
        menu += '\n'
    return menu
class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Define a slash command
    @app_commands.command(name="菜單", description="列出菜單的所有項目")
    async def menu(self, interaction: discord.Interaction):
        #if store != '': 
        await interaction.response.send_message(set_shop(store),ephemeral=True)
        #else:
        #    await interaction.response.send_message("還沒決定哪間")
    @app_commands.command(name="今日店家",description="今天要喝哪家呢?")
    async def store(self, interaction: discord.Interaction,店家:str):
        store = 店家
        await interaction.response.send_message("各位，今天喝{}喔\n{}".format(store,set_shop(store)))
    
# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
