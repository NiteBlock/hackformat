import discord
from discord.ext import commands
import random
import asyncio
from utils.embed import em

class Fun(commands.Cog):
    """Just for fun commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)
    
    @commands.command()
    async def rate(self, ctx, p1: discord.Member, p2: discord.Member):
        if p1 == p2:
            embed = discord.Embed(title=f"Something doesn't add up...", color=0xff0000)
            return await ctx.send(embed=embed)
        await ctx.done(f"**{p1.name}** and **{p2.name}** are **{random.randint(1,100)}%** compatable!", "Finished evaluating compatibility!", icon="null")

    @commands.command()
    async def kill(self, ctx, target: discord.Member):
        if target.id is self.bot.user.id:
            killmsg = ["You tried to kill me however you were to useless and died while you were doing the command!", "I am undefetable, dont even try or you will die", "You take a runup to hit me but while your on your way I hack into you and you get terminated."]
            target = "me"
        else:
            target = target.name
            bodypart = ["Heart", "Head", "Mouth", "Eye"]
            killmsg = [f"You stab {target} straight throught the {random.choice(bodypart)}!", f"You run at {target} but slip and stab yourself!", f"You shoot {target} in the {random.choice(bodypart)} and they die!"]
        msg = await ctx.done("Attack", f"You are attacking {target}...", icon="null")
        await asyncio.sleep(random.randint(5,50)/10)

        await msg.edit(**em("Attack finished!", killmsg, "done", icon=None))

    @commands.command()
    async def coinflip(self, ctx):
        ht = ["Heads", "Tails"]
        embed = discord.Embed(title=f"I chose {random.choice(ht)}!", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def rps(self, ctx, playing = True):
        score = [0, 0]
        max = 3
        choices = ["rock", "paper", "scissors"]
        choice = random.choice(choices)
        embed = discord.Embed(title="What score would you like to play to?\nDefault: 3", color=0x00ff00)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='jpg', size=1024))
        msg = await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        message = await self.bot.wait_for("message", check=check)
        max = int(message.content)
        await message.delete()
        playing = True
        while playing == True:
            choices = ["🇷", "🇵", "🇸"]
            choice = random.choice(choices)
            if score[0] != max and score[1] != max:
                embed = discord.Embed(title=f"Rock Paper or Scissors?", color=0x00ff00)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='jpg', size=1024))
                embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                await msg.edit(embed=embed)
                reactions = ["🇷", "🇵", "🇸"]
                for r in reactions:
                    await msg.add_reaction(r)
                def check2(reaction, user):
                    return ctx.author.id == user.id and str(reaction.emoji) in reactions
                reaction, user = await self.bot.wait_for("reaction_add", check=check2)
                if str(reaction.emoji) == "🇷":
                    uchoice = "Rock"
                if str(reaction.emoji) == "🇵":
                    uchoice = "Paper"
                if str(reaction.emoji) == "🇸":
                    uchoice = "Scissors"
                if choice == "🇷":
                    bchoice = "Rock"
                if choice == "🇵":
                    bchoice = "Paper"
                if choice == "🇸":
                    bchoice = "Scissors"
                if str(reaction.emoji) == choice:
                    embed=discord.Embed(title=f"It appears we both chose {bchoice} the score is still: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif str(reaction.emoji) == "🇷" and choice == "🇸":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif str(reaction.emoji) == "🇵" and choice == "🇷":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif str(reaction.emoji) == "🇸" and choice == "🇵":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif choice == "🇷" and str(reaction.emoji) == "🇸":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif choice == "🇵" and str(reaction.emoji) == "🇷":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
                elif choice == "🇸" and str(reaction.emoji) == "🇵":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {uchoice} and i chose {bchoice}. The score is now: User: {score[0]} Bot: {score[1]}", color=0x00ff00)
                    embed.set_footer(text=f"First to: {max} | Current Score: User: {score[0]} Bot: {score[1]}")
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    await asyncio.sleep(2)
            elif score[0] == max:
                embed = discord.Embed(title=f"Well played! You won nothing!", color=0x00ff00)
                embed.set_footer(text=f"First to: {max} | Score: User: {score[0]} Bot: {score[1]}")
                await msg.edit(embed=embed)
                playing = False
            elif score[1] == max:
                embed = discord.Embed(title=f"Well played! It was a fun game, but you lose!", color=0x00ff00)
                embed.set_footer(text=f"First to: {max} | Score: User: {score[0]} Bot: {score[1]}")
                await msg.edit(embed=embed)
                playing = False

def setup(bot):
    bot.add_cog(Fun(bot))
