from discord.ext import commands
from utils.embed import em

class Format(commands.Cog):
    """Cog for Format"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="format")
    async def format(self, ctx):
        await ctx.send_group_help(self.format)
        pass

    @commands.has_permissions(administrator=True)
    @format.command(name="new")
    async def format_new(self, ctx):
        if await ctx.confirm(**em("React with :thumbsup: to confirm!", "Would you like to create a new format?", "info", icon="null")):
        
            channel = await ctx.ask_channel("What channel do you want the format to take effect in?")
            n = await ctx.emoji_choice([{"1️⃣": 1}, {"2️⃣": 2}, {"3️⃣": 2}, {"4️⃣": 4}, {"5️⃣":5}], **em("How many variables do you want to use for this format?"))
        else:
            await ctx.error(icon="null")
def setup(bot):
    bot.add_cog(Format(bot))
