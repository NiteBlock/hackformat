from discord.ext import commands
import discord


class Moderation(commands.Cog):
    """Commands to be used for moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=30000):
        await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)

        embed = discord.Embed(color=discord.Color.dark_green())

        embed.add_field(name="Purged!", value="Done")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member = None, reason=None):
        embed = discord.Embed(color=discord.Color.dark_green())

        if member is ctx.message.author:
            embed.add_field(name="Error!", value="You can't kick yourself")
            return ctx.send(embed=embed)

        if member is None:
            embed.add_field(name="Error!", value="Please specify a member! I can't kick air")
            return await ctx.send(embed=embed)

        if reason is None:
            reason = "No reason at all!"
        message = f"You have been kicked from {ctx.guild.name} for {reason}!"

        await member.send(message)
        await ctx.guild.kick(member)
        await ctx.channel.send(f"{member} has been kicked!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member = None, reason=None):
        embed = discord.Embed(
            color=discord.Color.dark_green()
        )

        if member == ctx.message.author:
            embed.add_field(name="Error!", value="You can't ban yourself!")
            await ctx.send(embed=embed)

            return
        if member is None:
            embed.add_field(name="Error!", value="Please specify a member! I can't ban air")
            return await ctx.send(embed=embed)

        if reason is None:
            reason = "No reason at all!"
        message = f"You have been banned from {ctx.guild.name} for {reason}!"

        await member.send(message)
        await ctx.guild.ban(member)
        await ctx.channel.send(f"{member} has been banned!")

    @commands.command()
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

        
def setup(bot):
    bot.add_cog(Moderation(bot))
