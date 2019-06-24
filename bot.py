import discord
from discord.ext import commands
import os,json
import asyncio
import time
from discord.ext.commands import Bot
import random
import discord.utils


class Config:
    def __init__(self):
        self.config = json.loads(open("./config.json", "r").read())
        self.token = self.config["token"]
        self.default_prefix = self.config["defaultprefix"]


def get_pre(message):
    return commands.when_mentioned_or(Config().default_prefix)


bot = commands.Bot(command_prefix=get_pre)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{Config().default_prefix}help"))
    print("Started!")

if __name__ == "__main__":
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog.replace('.py', '')}")
                print(f"Loaded cog {cog}")
            except Exception as e:
                print(f"{e.__class__.__name__} Caused by loading cog {cog}\n {e}")

    bot.run(Config().token)
