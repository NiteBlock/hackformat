import discord
import os
import discord.utils
from utils.hackformat import HackFormatBot


async def get_pre(bot, message):
    # mentioned or defaultprefix
    return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id, bot.config["defaultprefix"]]


bot = HackFormatBot(command_prefix=get_pre)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{bot.config['defaultprefix']}help"))
    print("Started!")

if __name__ == "__main__":
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog.replace('.py', '')}")
                print(f"Loaded cog {cog}")
            except Exception as e:
                print(f"{e.__class__.__name__} Caused by loading cog {cog}\n {e}")

    bot.run(bot.config["token"])
