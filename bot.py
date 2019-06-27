import discord
import os
import discord.utils
from utils.hackformat import HackFormatBot
from pathlib import Path
from functools import reduce

def get_pre(bot, message):
    # mentioned or defaultprefix 
    return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id, bot.config["defaultprefix"]]


bot = HackFormatBot(command_prefix=get_pre)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{bot.config['defaultprefix']}help"))
    print("Started!")


def format_cog(path):
    replacements = (('/', '.'), ('\\', '.'), ('.py', ''))
    for r in replacements:
        path = path.replace(*r)

    return path


if __name__ == "__main__":
    for cog in Path("cogs").glob('**/*.py'):
        cog_path = format_cog(str(cog))
        try:
            bot.load_extension(cog_path)
            print(f"Loaded cog {cog_path}")
        except Exception as e:
            print(f"{e.__class__.__name__} Caused by loading cog {cog_path}: {e}")
    bot.run(bot.config["token"])

