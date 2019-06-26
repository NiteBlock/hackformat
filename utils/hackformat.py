from discord.ext import commands
import discord
import json
from utils.embed import em

#icons from https://flaticon.com/ we dont own these


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
        try:
            reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)
        except TimeoutError:
            raise commands.CommandError("Timed out!")
        if reaction[0].emoji == '👍':
            return True
        return False

    async def ask_channel(self, **kwargs):
        title = kwargs.get("title", "Choose a channel")
        description = kwargs.get("description", "Mention a channel to choose it!")
        msg = await self.info(title, description, icon="null")
        def check(m):
            return msg.channel == m.channel and m.author.id == self.author.id
        try:
            m = await self.bot.wait_for("message", check=check, timeout=kwargs.get("timeout", 60))
        except TimeoutError:
            raise commands.CommandError("Timed out!")

        for channel in self.guild.text_channels:
            if len(str(m.content).split(str(channel.id))) >= 2:

                return channel
        raise commands.CommandError("Not found!")
            
        
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

        try:
            reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)
        except TimeoutError:
            raise commands.CommandError("Timed out!")
        return reactions.get(str(reaction.emoji))

    async def error(self, error, title=None, **kwargs):
        return await self.send(**em(error, title, "error", **kwargs))


    async def done(self, description, title=None, **kwargs):
        return await self.send(**em(description, title, "done", **kwargs))


    async def info(self, description, title=None, **kwargs):
        return await self.send(**em(description, title, "info", **kwargs))


class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")

        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=HackFormatContext)
