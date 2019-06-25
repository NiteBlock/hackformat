import discord
from discord.ext import commands
import asyncio


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        msg = await ctx.send(":regional_indicator_s: Server Settings\n :regional_indicator_u: User Settings")
        reactions = ["🇸", "🇺"]
        for r in reactions:
            await msg.add_reaction(r)
        await asyncio.sleep(5 / 10)
        reaction = await self.bot.wait_for('raw_reaction_add')
        if reaction.user_id == ctx.author.id:
            if str(reaction.emoji) == reactions[0]:
                await ctx.send(reactions[0])
            elif str(reaction.emoji) == reactions[1]:
                await ctx.send(reactions[1])

def setup(bot):
    bot.add_cog(Reactions(bot))