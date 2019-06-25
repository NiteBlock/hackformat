from discord.ext import commands
import discord
import json


class HackFormatContext(commands.Context):
    async def confirm(self, **kwargs):
        def check(reaction, user):
            return self.author.id == user.id and reaction.emoji in ['👎', '👍']

        prompt = kwargs.get("prompt", None)
        embed = kwargs.get("embed", None)
        timeout = kwargs.get('timeout', 60)

        if prompt is None and embed is None:
            raise ValueError("You need to define prompt or embed")

        msg = await self.send(content=prompt, embed=embed)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        reaction = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)

        if reaction[0].emoji == '👍':
            return True
        return False

    async def emoji_choice(self, reactions, **kwargs):
        def check(reaction, user):
            return self.author.id == user.id and reaction.emoji in reactions.keys()

        prompt = kwargs.get("prompt", None)
        embed = kwargs.get("embed", None)
        timeout = kwargs.get('timeout', 60)

        if prompt is None and embed is None:
            raise ValueError("You need to define prompt or embed")

        msg = await self.send(content=prompt, embed=embed)

        for reaction in reactions.keys():
            await msg.add_reaction(reaction)

        reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)

        return reactions.get(str(reaction.emoji))





class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")

        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=HackFormatContext)
