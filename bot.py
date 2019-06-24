import discord
from discord.ext import commands
import os,json

class config():
    def __init__(self):
        self.config = json.loads(open("./config.json", "r").read())
        self.token = self.config["token"]
        self.defaultprefix = self.config["defaultprefix"]


def get_pre(message):
    return commands.when_mentioned_or(config().defaultprefix)

bot = commands.Bot(command_prefix=get_pre)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{config().defaultprefix}help"))
    print("Started!")

if __name__ == "__main__":
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog.replace('.py', '')}")
                print(f"Loaded cog {cog}")
            except Exception as e:
                print(f"{e.__class__.__name__} Caused by loading cog {cog}\n {e}")
    
    bot.run(config().token)