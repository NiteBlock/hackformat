import discord
from discord.ext import commands
import asyncio


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        dm = await ctx.author.create_dm()
        msg = await dm.send(":regional_indicator_s: Server Settings\n :regional_indicator_u: User Settings")
        reactions = ["🇸", "🇺"]
        for r in reactions:
            await msg.add_reaction(r)
        await asyncio.sleep(5 / 10)
        reaction = await self.bot.wait_for('raw_reaction_add')
        if str(reaction.emoji) == reactions[0]:
            await msg.edit(":regional_indicator_o: Overview\n:regional_indicator_m: Moderation\n:regional_indicator_r: Roles")
            reactions = ["🇴", "🇲", "🇷"]
            for r in reactions:
                await msg.add_reaction(r)
            reaction = await self.bot.wait_for('raw_reaction_add')
            if str(reaction.emoji) == reactions[0]:
                print("a")
            if str(reaction.emoji) == reactions[1]:
                print("b")
            if str(reaction.emoji) == reactions[2]:
                print("c")
        elif str(reaction.emoji) == reactions[1]:
            await dm.send("Work in progress!")

def setup(bot):
    bot.add_cog(Reactions(bot))