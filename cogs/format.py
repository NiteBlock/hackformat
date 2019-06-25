from discord.ext import commands


class Format(commands.Cog):
    """Cog for Format"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Format(bot))
