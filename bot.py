import discord
from discord.ext import commands
import os,json
import asyncio
import time
from discord.ext.commands import Bot
import random
import discord.utils



class config():
    def __init__(self):
        self.config = json.loads(open("./config.json", "r").read())
        self.token = self.config["token"]
        self.defaultprefix = self.config["defaultprefix"]


def get_pre(message):
    return commands.when_mentioned_or(config().defaultprefix)

bot = commands.Bot(command_prefix=get_pre)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{config().defaultprefix}help"))
    print("Started!")

if __name__ == "__main__":
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog.replace('.py', '')}")
                print(f"Loaded cog {cog}")
            except Exception as e:
                print(f"{e.__class__.__name__} Caused by loading cog {cog}\n {e}")
    
@bot.command()
async def purge(ctx, amount=30000):
    await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)

    embed = discord.Embed(
         color = discord.Color.dark_green()
    )

    embed.add_field(name="Purged!", value= "Done")

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member = None, reason = None):

    embed = discord.Embed(
         color = discord.Color.dark_green()
    )

    if member == ctx.message.author:

        embed.add_field(name="Error!", value="You can't kick yourself")
        await ctx.send(embed=embed)
        return

    if member == None:

        embed.add_field(name="Error!", value="Please specify a member! I can't kick air")
        await ctx.send(embed=embed)

        return     
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been kicked from {ctx.guild.name} for {reason}!"

    await member.send(message)
    await ctx.guild.kick(member)
    await ctx.channel.send(f"{member} has been kicked!")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.Member = None, reason = None):

    embed = discord.Embed(
         color = discord.Color.dark_green()
    )

    if member == ctx.message.author:
        
        embed.add_field(name="Error!", value="You can't ban yourself!")
        await ctx.send(embed=embed)

        return
    if member == None:
        
        embed.add_field(name="Error!", value="Please specify a member! I can't ban air")
        await ctx.send(embed=embed)

        return     
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been banned from {ctx.guild.name} for {reason}!"

    await member.send(message)
    await ctx.guild.ban(member)
    await ctx.channel.send(f"{member} has been banned!")

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):


    embed = discord.Embed(
         color = discord.Color.dark_green()
    )

    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not member:
        await ctx.send("Member not found!")
        return

    if member == ctx.message.author:

        embed.add_field(name="Error!", value="You can't mute yourself!")
        await ctx.send(embed=embed)

        return
    await member.add_roles(role)

    embed.add_field(name="Done!", value=f"Muted {member.mention}")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):


    embed = discord.Embed(
         color = discord.Color.dark_green()
    )

    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not member:
        await ctx.send("Member not found!")
        return

    if member == ctx.message.author:

        embed.add_field(name="Error!", value="You can't unmute yourself!")
        await ctx.send(embed=embed)

        return
    await member.remove_roles(role)

    embed.add_field(name="Done!", value=f"Unmuted {member.mention}")
    await ctx.send(embed=embed)                                                                    
                                   
    bot.run(config().token)
