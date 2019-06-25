from discord.ext import commands


class Fun(commands.Cog):
    """Just for fun commands"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Fun(bot))
