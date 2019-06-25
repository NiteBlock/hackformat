from discord.ext import commands


class AntiSpam(commands.Cog):
    """Cog for AntiSpam and AntiAdvertisement"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(AntiSpam(bot))
