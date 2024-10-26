import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    # Sync the bot's slash commands with Discord
    await bot.tree.sync()
    print("Slash commands have been synced.")

# Command: Load a specific cog
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} successfully.")

# Command: Unload a specific cog
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} successfully.")

# Command: Reload a specific cog
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} successfully.")

# Function: Load all extensions (cogs) at startup
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")

# Function: The main async entry point
async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

# Start the bot
if __name__ == "__main__":
    asyncio.run(main())
