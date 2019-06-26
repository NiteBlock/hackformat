import discord
from discord.ext import commands


class HelpCog(commands.HelpCommand):
    """Formating the help command so its actually ok and not ugly"""
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.help_command = HelpCog(bot)