import asyncio
import os
import sys

import discord
import git
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
# 將單一角色名稱改為多個角色列表，使用逗號分隔
admin_roles = os.getenv("ADMIN_ROLE_NAME").split(',')
premix = os.getenv("PREMIX")
channel_id = int(os.getenv("CHANNEL_ID"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=premix, intents=intents)


# 機器人啟動完成
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    # Sync the bot's slash commands with Discord
    await bot.tree.sync()
    print("Slash commands have been synced.")
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Bot is up and ready!")


# 檢查是否具有管理員角色的函數
def is_admin():
    async def predicate(ctx):
        return any(role.name in admin_roles for role in ctx.author.roles)
    return commands.check(predicate)


# 指令：$load
@bot.command()
@is_admin()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} successfully.")


# 指令：$unload
@bot.command()
@is_admin()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} successfully.")


# 指令：$reload
@bot.command()
@is_admin()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} successfully.")


# 指令: restart
@bot.command(name="restart", help="重新啟動機器人")
@is_admin()
async def restart(ctx):
    await ctx.send("Restarting the bot...")
    # Restart the bot program
    os.execv(sys.executable, ["python"] + sys.argv)


# 指令: shutdown
@bot.command(name="shutdown", help="關閉機器人")
@is_admin()
async def shutdown(ctx):
    await ctx.send("Shutting down the bot...")
    await bot.close()


@bot.command()
@is_admin()
async def gitpull(ctx):
    try:
        repo = git.Repo(os.getcwd())
        origin = repo.remotes.origin
        origin.pull()
        await ctx.send("Git pull completed successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


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
