import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):
    """Just for fun commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)
    
    @commands.command()
    async def rate(self, ctx, p1: discord.Member=None, p2: discord.Member=None):
        if p1 == None:
            embed = discord.Embed(title="No person provided!", color=0xff0000)
            await ctx.send(embed=embed)
        if p1 != None:
            if p2 == None:
                embed = discord.Embed(title="You must provide two people!", color=0xff0000)
                await ctx.send(embed=embed)
            elif p1 == p2:
                embed = discord.Embed(title=f"Something doesn't add up...", color=0xff0000)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"**{p1.name}** and **{p2.name}** are **{random.randint(1,100)}%** compatable!", color=0x00ff00)
                await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, target: discord.Member):
        target = target.name
        bodypart = ["Heart", "Head", "Mouth", "Eye"]
        killmsg = [f"You stab {target} straight throught the {random.choice(bodypart)}!", f"You run at {target} but slip and stab yourself!", f"You shoot {target} in the {bodypart} and they die!"]
        embed = discord.Embed(title=random.choice(killmsg), color=0x00ff00)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def coinflip(self, ctx):
        ht = ["Heads", "Tails"]
        embed = discord.Embed(title=f"I chose {random.choice(ht)}!", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def rps(self, ctx, playing = True):
        score = [0, 0]
        choices = ["rock", "paper", "scissors"]
        choice = random.choice(choices)
        embed = discord.Embed(title="What score would you like to play to?\nDefault: 3", color=0x00ff00)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='jpg', size=1024))
        msg = await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        message = await self.bot.wait_for("message", check=check)
        if int(max) == max:
            max = message[0]
        else:
            max = 3
        await message.delete()
        playing = True
        while playing == True:
            choices = ["rock", "paper", "scissors"]
            choice = random.choice(choices)
            if score[0] != max and score[1] != max:
                embed = discord.Embed(title=f"Rock Paper or Scissors?", color=0x00ff00)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url_as(format='jpg', size=1024))
                await msg.edit(embed=embed)
                def check2(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                message = await self.bot.wait_for("message", check=check2)
                if message.content.lower() == choice:
                    embed=discord.Embed(title=f"It appears we both chose {choice} the score is still {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif message.content.lower() == "rock" and choice == "scissors":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif message.content.lower() == "paper" and choice == "rock":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif message.content.lower() == "scissors" and choice == "paper":
                    score[0] = score[0] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif choice == "rock" and message.content.lower() == "scissors":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif choice == "paper" and message.content.lower() == "rock":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
                elif choice == "scissors" and message.content.lower() == "paper":
                    score[1] = score[1] + 1
                    embed = discord.Embed(title=f"You chose {message.content} and i chose {choice}. The score is now {score}", color=0x00ff00)
                    await msg.edit(embed=embed)
                    await message.delete()
                    await asyncio.sleep(2)
            elif score[0] == max:
                embed = discord.Embed(title=f"Well played! You won nothing!", color=0x00ff00)
                await msg.edit(embed=embed)
                playing = False
            elif score[1] == max:
                embed = discord.Embed(title=f"Well played! It was a fun game, but you lose!", color=0x00ff00)
                await msg.edit(embed=embed)
                playing = False


def setup(bot):
    bot.add_cog(Fun(bot))
