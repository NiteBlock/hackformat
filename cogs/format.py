from discord.ext import commands
from utils.embed import em

class Format(commands.Cog):
    """Cog for Format"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["format", "new"])
    @commands.has_permissions(manage_guild=True)
    async def new_format(self, ctx):
        if await ctx.confirm(**em("React with :thumbsup: to confirm!", "Would you like to create a new format?", "info", icon="null")):
        
            channel = await ctx.ask_channel("What channel do you want the format to take effect in?")
            n = await ctx.emoji_choice([{"1️⃣": 1}, {"2️⃣": 2}, {"3️⃣": 2}, {"4️⃣": 4}, {"5️⃣":5}], **em("For now you can only choose 5","How many variables do you want to use for this format?", type="info"))
        else:
            await ctx.error("Cancled!", icon="null")
def setup(bot):
    bot.add_cog(Format(bot))
