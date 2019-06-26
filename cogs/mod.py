import inspect
import discord
from discord.ext import commands
import asyncio
import time
from discord.ext.commands import Bot
import random
import discord.utils


class Moderation(commands.Cog):
    """Commands to be used for moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=100):
        if not await ctx.confirm(f"Delete {amount} messages?"):
            return

        await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)

        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="Purged!", value="Done")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason="No given reason"):

        if member is ctx.author:
            raise commands.CommandError("You cant kick yourself!")
        
        embed = discord.Embed(colour=discord.Colour.red(), title=f"You have been kicked from {ctx.guild.name} for {reason}!")

        await member.send(embed=embed)
        await ctx.guild.kick(member, reason=reason)
        await ctx.Done(f"{member} has been kicked!")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason="No given reason"):

        if member == ctx.author:
            raise commands.CommandError("You can't ban yourself!")

        embed = discord.Embed(colour=discord.Colour.red(), title=f"You have been banned from {ctx.guild.name} for {reason}!")

        await member.send(embed=embed)
        await ctx.guild.ban(member)
        await ctx.info(f"{member} has been banned!")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=discord.Color.dark_green())

        role = discord.utils.get(ctx.guild.roles, name="muted")
        if not member:
            return await ctx.send("Member not found!")

        if member == ctx.author:
            embed.add_field(name="Error!", value="You can't mute yourself!")
            return await ctx.send(embed=embed)

        await member.add_roles(role)

        embed.add_field(name="Done!", value=f"Muted {member.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=discord.Color.dark_green())

        role = discord.utils.get(ctx.guild.roles, name="muted")
        if not member:
            return await ctx.send("Member not found!")

        if member == ctx.author:
            embed.add_field(name="Error!", value="You can't unmute yourself!")
            return await ctx.send(embed=embed)

        await member.remove_roles(role)

        embed.add_field(name="Done!", value=f"Unmuted {member.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name="User Info")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Username:", value=member.name, inline=True)
        embed.add_field(name="Display Name:", value=member.display_name, inline=True)
        embed.add_field(name="Account created:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)

        embed.add_field(name="Top Role:", value=member.top_role.mention, inline=True)
        embed.add_field(name=f"Roles ({len(member.roles)})", value=" ".join([role.mention for role in member.roles]), inline=True)
        embed.add_field(name="Bot?", value=member.bot, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):

     embed = discord.Embed(
     color = discord.Color.green())

     embed.set_author(name="Help")
     embed.add_field(name="+enable (spam/swear/ad)", value="enables the antispam, swear or ad (depending on what the user chooses, ADMINS ONLY)", inline=False)
     embed.add_field(name="+disable (spam/swear/ad)", value ="disables the antispam, swear or ad (depending on what the user chooses, ADMINS ONLY)", inline=False)
     embed.add_field(name="+kick", value ="Kicks the specified user (Admin only)", inline=False)
     embed.add_field(name="+unmute", value ="Unmutes the specified user (Admin only)", inline=False)
     embed.add_field(name="+ban", value ="Bans the specified user (Admin only)", inline=False)
     embed.add_field(name="+warn", value ="Warns the desired player", inline=False)
     embed.add_field(name="+info", value ="Shows your desired player's server-info", inline=False)
     embed.add_field(name="+invite", value ="sends back an invite link for the bot", inline=False)
     embed.add_field(name="+support", value ="Crates a ticket", inline=False)
     embed.add_field(name="+help", value ="Shows this", inline=False)
     embed.add_field(name="+purge", value = "Clears X amount of messages (Admin Only)", inline=False)
     embed.add_field(name="+format", value = "sends out a message in a desired form (Admin Only)", inline=False)
     embed.add_field(name="+eval", value = "evals a code", inline=False)
     embed.add_field(name="+sudo", value = "Sudos a player (Admin only)", inline=False)
     embed.add_field(name="+db", value = "update/get/drop> <datebase> <collection> <data>", inline=False)
     embed.add_field(name="+reactionaction", value="ReactionRole, but for more  than roles", inline=False)
     embed.add_field(name="+8ball", value ="Answers a yes or no question from the beyond", inline=False)
     embed.add_field(name="+square", value ="Times the wanted number by itself (Squares it)", inline=False)
     embed.add_field(name="+avatar", value="Shows specified user's profile pciture", inline=False)
     embed.add_field(name="+Divied", value="Divides two numbers", inline=False)
     embed.add_field(name="+Add", value="Adds two numbers", inline=False)
     embed.add_field(name="+Subtract", value="Subtracts two numbers", inline=False)
     embed.add_field(name="+Multiply", value="Multiplies two numbers", inline=False)
     embed.add_field(name="+random", value="Generates a random password (Customizable)", inline=False)

     await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
