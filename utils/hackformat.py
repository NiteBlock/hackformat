from discord.ext import commands
import discord
import json


class HackFormatContext(commands.Context):
    async def confirm(self, **kwargs):
        """Helper for messages where the user answers a yes or no question"""
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
        """Helper for messages where use chooses an emoji. NOTE: only works with unicode emojis"""
        def check(reaction, user):
            return self.author.id == user.id and ord(reaction.emoji) in reactions.keys()

        reactions = {ord(k): v for (k, v) in reactions.items()}

        prompt = kwargs.get("prompt", None)
        embed = kwargs.get("embed", None)
        timeout = kwargs.get('timeout', 60)

        if prompt is None and embed is None:
            raise ValueError("You need to define prompt or embed")

        msg = await self.send(content=prompt, embed=embed)

        for reaction in reactions.keys():
            await msg.add_reaction(chr(reaction))

        reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)

        return reactions.get(ord(reaction.emoji))


class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")

        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=HackFormatContext)

