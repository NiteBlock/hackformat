from discord.ext import commands
from utils.embed import em
import random
from discord import utils

class Format(commands.Cog):
    """Cog for Format"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="format")
    async def format(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send_help(self.format)

    @commands.has_permissions(administrator=True)
    @format.command(name="new")
    async def format_new(self, ctx):
        if await ctx.confirm(**em("React with :thumbsup: to confirm!", "Would you like to create a new format?", "info", icon="null")):
            channel = await ctx.ask_channel(title="What channel do you want the format to take effect in?")
            n = await ctx.emoji_choice({"1\N{combining enclosing keycap}": 1, "2\N{combining enclosing keycap}": 2, "3\N{combining enclosing keycap}": 2, "4\N{combining enclosing keycap}": 4, "5\N{combining enclosing keycap}":5}, **em("Right now you can choose up to 5 only.", "How many variables do you want to use for this format?", "info"))
            while True:
                vs = []
                for i in range(n):
                    x = await ctx.question(title="What should we use as this variable", description=f"This should be short, eg '{random.choise('title','text','user','suggestion')}'. ")
                    if x.content in vs:
                        raise commands.CommandError("You cant use the same variable 2 times.")
                    vs.append(x.content)
                example = "```"
                for var in vs:
                    example += "[" + var + "] <insert text here>\n"
                example += "```"
                if await ctx.confirm(**em(f"Please confirm. {example}", "This is how it will look like.", type="info")):
                    break
            n = await ctx.emoji_choice({"1\N{combining enclosing keycap}": 1, "2\N{combining enclosing keycap}": 2, "3\N{combining enclosing keycap}": 2, "4\N{combining enclosing keycap}": 4, "5\N{combining enclosing keycap}":5}, **em("Right now you can choose up to 5 only.", "How many actions do you want to do after this format?", "info"))
            while True:
                actions = []
                for i in range(n):
                    embed = em("You can choose only one at the time")["embed"]
                    action = await ctx.emoji_choice({"➕" : "create_channel", "💬": "send_message", "🙂": "add_reaction", "📝": "add_role"}, embed)
                    if action is "create_channel":
                        action = {"name": action}
                        cat = await ctx.question("Please get the exact name of the category the channel should go to.", "What is the category the channel should go to.")
                        cat = utils.get(ctx.guild.categories, name=cat)
                        if cat is None:
                            raise commands.CommandError("Invalid Category")
                        x = ""
                        for var in vs:
                            x += f"${var} | The variable that was inputed for [{var}]\n"
                        await ctx.question(title="What should be the name of the channel \nPlaceholders:```$number | the number of times this format has been done\n{x}$user | The author of the message\n$mention | Mentions the user\n",description="")
                        
            await ctx.info(f"Its a work in progress. {channel.mention} {vs}")
        else:
            await ctx.error("Process Cancelled", "Cancelled.")
def setup(bot):
    bot.add_cog(Format(bot))
