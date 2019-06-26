import discord
from discord.ext import commands
import aiohttp


class AntiSpam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def spam(self, message):
        ctx = await self.bot.get_context(message)

        async for m in message.channel.history(limit=1, before=message):
            last_msg = m

        if last_msg.author.id is message.author.id and last_msg.clean_content == message.clean_content:
            try:
                await message.delete()
            except discord.Forbidden:
                await ctx.send("I'm sorry, an error had occurred an I am unable to delete that spam.")
            except Exception as e:
                return


def setup(client):
    n = AntiSpam(client)
    client.add_listener(n.spam, "on_message")
    client.add_cog(n)
