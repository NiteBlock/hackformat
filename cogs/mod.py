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
        await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)

        embed = discord.Embed(color=discord.Color.dark_green())

        embed.add_field(name="Purged!", value="Done")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason="No given reason"):

        if member is ctx.message.author:
            raise commands.CommandError("You cant kick yourself!")
        
        embed = discord.Embed(colour=discord.Colour.red(), title=f"You have been kicked from {ctx.guild.name} for {reason}!")

        await member.send(embed=embed)
        await ctx.guild.kick(member, reason=reason)
        await ctx.Done(f"{member} has been kicked!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason="No given reason"):

        if member == ctx.message.author:
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

        if member == ctx.message.author:
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

        if member == ctx.message.author:
            embed.add_field(name="Error!", value="You can't unmute yourself!")
            return await ctx.send(embed=embed)

        await member.remove_roles(role)

        embed.add_field(name="Done!", value=f"Unmuted {member.mention}")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only
    @commands.has_permissions(send_message=True)
    async def info(self, ctx, member : discord.Member):

        roles = [role for role in member.roles]
        embed = discord.Embed(
        color = discord.Color.green()
        )
        embed.set_author(name="User info")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Guild name:", value=member.display_name, inline=False)

        embed.add_field(name="Account created:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top Role:", value=member.top_role.mention, inline=False)
        embed.add_field(name="Bot?", value=member.bot, inline=False)

        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Moderation(bot))
