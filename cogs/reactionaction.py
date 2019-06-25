from discord.ext import commands
import asyncio


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        msg = await ctx.send(":regional_indicator_s: Server Settings\n :regional_indicator_u: User Settings")
        reactions = ["🇸", "🇺"]
        for r in reactions:
            await msg.add_reaction(r)
        await asyncio.sleep(5 / 10)

        def check(reaction, user):
            return user == ctx.author and reaction == reaction

        reaction, user = await self.bot.wait_for('raw_reaction_add', check=check)
        print(reaction, user)


def setup(bot):
    bot.add_cog(Reactions(bot))
