import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


# 機器人啟動完成
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    # Sync the bot's slash commands with Discord
    await bot.tree.sync()
    print("Slash commands have been synced.")


# 指令：$load
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} successfully.")


# 指令：$unload
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} successfully.")


# 指令：$reload
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} successfully.")


# 開機時載入所有子程式
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")


# 開機程式
async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)


# 啟動機器
if __name__ == "__main__":
    asyncio.run(main())
