#check for is_admin() if they are a dev
#check for role_in_support("rolename")
#check for is_support_guild() if the command is in support
#check for commands.check(bot_has_admin())if the bot has admin (used as a bot.check)
from discord.ext import commands
import json
import discord



def is_admin():
    async def predicate(ctx):
        with open("config.json", "r") as r:
            return ctx.author.id in json.load(r)["owners"]

    return commands.check(predicate)


def has_role_in_support(role):
    async def predicate(ctx, role):
        guild = bot.get_guild(591690242675834922)
        for member in guild.members:
            if member.id == ctx.author.id:
                if discord.utils.get(guild.roles, name=role) in member:
                    return True
        return False
    return commands.check(predicate)

def is_support_guild():
    async def predicate(ctx):
        return ctx.guild.id == 591690242675834922
    return commands.check(predicate)

def bot_has_admin():
    async def predicate(ctx):
        return ctx.guild.me.guild_permissions.administrator == True
    return commands.check(predicate)
