import json

import discord
from discord import app_commands
from discord.ext import commands


def read():
    with open("user_data.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def write(data):
    with open("user_data.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)
    return


class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.commands.command()
    async def pay(self, ctx, amount: int, member: discord.Member):
        data = read()
        if ctx.author.id in data:
            if data[ctx.author.id]["balance"] >= amount:
                data[ctx.author.id]["balance"] -= amount
                data[member.id]["balance"] += amount
                write(data)
                await ctx.send(f"Successfully paid {amount} to {member.mention}")
            else:
                await ctx.send("You don't have enough balance to pay")
        else:
            await ctx.send("You don't have an account")


async def setup(bot):
    bot.add_cog(Payment(bot))
