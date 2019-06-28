from discord.ext import commands
from utils.embed import em
import random
from discord import utils
from utils import db
import discord

class Format(commands.Cog):
    """Cog for Format"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if f"{message.guild.id}-{message.channel.id}" in db.list("formats"):
            data = db.get("formats", f"{message.guild.id}-{message.channel.id}")
            await message.channel.send("```py\n" + str(data["actions"]) + "```")
            for v in data["variables"]:
                if len(message.content.split(v)) != 2:
                    await message.delete()
                    await message.channel.send("Invalid usage of format", delete_after=3)
                    return
            c = message.content.replace(data["variables"][0], "")
            for action in data["actions"]:

                if action["name"] == "create_channel":
                    await message.guild.create_text_channel(**action["args"], **action["kwargs"])
                elif action["name"] == "send_message":
                    y = self.bot.get_channel(action["channel"]) or message.channel
                    await y.send(**action["kwargs"])


    @commands.group(name="format")
    async def format(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send_help(self.format)

    @commands.has_permissions(administrator=True)
    @format.command(name="new")
    async def format_new(self, ctx):
        if await ctx.confirm(**em("React with :thumbsup: to confirm!", "Would you like to create a new format?", "info", icon="null")):
            format_channel = await ctx.ask_channel(title="What channel do you want the format to take effect in?")
            n, m = await ctx.emoji_choice({"1\N{combining enclosing keycap}": 1, "2\N{combining enclosing keycap}": 2, "3\N{combining enclosing keycap}": 2, "4\N{combining enclosing keycap}": 4, "5\N{combining enclosing keycap}":5}, **em("Right now you can choose up to 5 only.", "How many variables do you want to use for this format?", "info"))
            while True:
                vs = []
                for i in range(int(n)):
                    x = await ctx.question(title="What should we use as this variable", description=f"This should be short, eg '{random.choice(['title','text','user','suggestion'])}''")
                    if x.content in vs and x.content in ["user", "1", "2", "3", "4", "5"]:
                        raise commands.CommandError("You cant use the same variable 2 times.")
                    vs.append(x.content)
                example = "```"
                for var in vs:
                    example += "[" + var + "] <insert text here>\n"
                example += "```"
                if await ctx.confirm(**em(f"Please confirm. {example}", "This is how it will look like.", type="info")):
                    break
            n, m = await ctx.emoji_choice({"1\N{combining enclosing keycap}": 1, "2\N{combining enclosing keycap}": 2, "3\N{combining enclosing keycap}": 2, "4\N{combining enclosing keycap}": 4, "5\N{combining enclosing keycap}":5}, **em("Right now you can choose up to 5 only.", "How many actions do you want to do after this format?", "info"))
            while True:
                actions = []
                for i in range(n):
                    y = {"➕" : "create_channel", "💬": "send_message", "🙂": "add_reaction", "📝": "add_role"}
                    embed = em("You can choose only one at the time", "Choose an action", "info")["embed"]
                    for x in y:

                        embed.add_field(name=x + " " + y[x], value = f"Do this action by adding the {x} reaction")
                    
                    action, m = await ctx.emoji_choice(y, embed=embed)
                    if action is "create_channel":
                        action = {"name": action}
                        
                        cat = await ctx.question(description="Please get the exact name of the category the channel should go to.", title="What is the category the channel should go to.")
                        cat = utils.get(ctx.guild.categories, name=cat.content)
                        if cat is None:
                            raise commands.CommandError("Invalid Category")
                        x = ""
                        for var in vs:
                            x += f"${var} | The variable that was inputed for [{var}]\n"
                        name = await ctx.question(title="What should be the name of the channel", description="Placeholders:```{number} | the number of times this format has been done\n"+ x +"{user} | The author of the message\n{user.mention} | Mentions the user\n{user.name} | the name of the author```")
                        if await ctx.confirm(**em("React with a :thumbsup: if you want to set the topic.", "Do you want to have a topic")):
                            x = await ctx.question(title="What should the topic be?", description="You can use the same placeholders as before.")
                            action["kwargs"]["topic"] = x.content
                        var = i
                        action["args"] = [ name ]
                        actions.append(actions)
                        await ctx.info("")
                    if action is "send_message":
                        action = {"name": action}
                        await ctx.info("Mention a channel, use 'self' as the current channel or say the name of a variable before (create_channel actions only)", "Choose a channel to send the message to", icon="null")
                        def check(m):
                            return ctx.channel == m.channel and m.author.id == ctx.author.id
                        try:
                            m = await self.bot.wait_for("message", check=check, timeout=60)
                        except TimeoutError:
                            raise commands.CommandError("Timed out!")
                        try:
                            x = int(m.content)
                        except:
                            x = 0
                        channel = None
                        if channel is "self":
                            channel = format_channel
                        if x in range(i-1) and not i >= 1 and actions[x - 1 ]["name"] is "create_channel":
                            channel = x
                        else:
                            for channel in ctx.guild.text_channels:
                                if len(str(m.content).split(str(channel.id))) >= 2:
                                    action["channel"] = channel.id

                        if channel is None:
                            raise commands.CommandError("That is not a channel!")
                        t =  await ctx.question(title="What should the title for this message be", description="This here is a description above is the title")
                        d = await ctx.question(title="What should the description for this message be", description="This here is a description above is the title")
                        action["kwargs"] = em(d,t, "info", icon="null")
                        action["args"] = []
                        actions.append(action)
                if await ctx.confirm(**em(str(actions), "Do you wish to use this", "info")):
                    break
            await ctx.send("done")
            data = {
                "channel" : format_channel.id,
                "guild" : ctx.guild.id,
                "variables" : vs,
                "example" : example,
                "number" : 0,
                "actions" : actions
            }
            db.update("formats", f"{ctx.guild.id}-{format_channel.id}", data)
                        
                            
            await ctx.info(f"Its a work in progress. {channel.mention} {vs}")
        else:
            await ctx.error("Process Cancelled", "Cancelled.")
def setup(bot):
    bot.add_cog(Format(bot))
