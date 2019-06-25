import discord


class Utility(commands.Cog):
    """Utility Commands"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Utility(bot))
