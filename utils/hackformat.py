from discord.ext import commands
import discord
import json


class HackFormatContext(commands.Context):
    async def confirm(self, prompt):
        def check(reaction, user):
            return self.author.id == user.id and reaction.emoji in ['👎', '👍']

        if isinstance(prompt, str):
            msg = await self.send(prompt)
        elif isinstance(prompt, discord.Embed):
            msg = await self.send(embed=prompt)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        reaction = await self.bot.wait_for('reaction_add', check=check, timeout=60)

        if reaction[0].emoji == '👍':
            return True
        return False


class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")

        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=HackFormatContext)
