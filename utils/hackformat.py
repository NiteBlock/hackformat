from discord.ext import commands
import discord
import json
from utils.embed import em

# icons from https://flaticon.com/ we dont own these


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


class HackFormatHelp(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    def get_command_signature(self, command):
        return f"```{self.clean_prefix}{command.qualified_name} {command.signature}```"

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, description=command.description, color=discord.Color.green())
        if len(command.aliases) > 0:
            embed.add_field(name="Aliases", value=', '.join(command.aliases))
        embed.add_field(name="Usage", value=self.get_command_signature(command))
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="All Commands", color=discord.Color.green())
        for cog, cog_commands in mapping.items():
            if not cog:
                category = "Uncatagorized"
            else:
                category = getattr(cog, 'qualified_name')

            command_signatures = '\n'.join([self.get_command_signature(c) for c in cog_commands])

            if not command_signatures:
                continue

            embed.add_field(name=category, value=command_signatures, inline=False)

        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name)
        for command in group.commands:
            embed.add_field(name=command.qualified_name, value=self.get_command_signature(command))

        await self.context.send(embed=embed)


class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")
        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=HackFormatContext)
