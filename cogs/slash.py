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
name = "飲料店"
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
class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Define a slash command
    @app_commands.command(name="菜單", description="列出菜單的所有項目")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message(menu)

# Cog setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
