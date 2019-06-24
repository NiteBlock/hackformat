from discord.ext import commands
import json


class HackFormatBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.json")

        with open(self.config_file, 'r') as r:
            self.config = json.load(r)

        super().__init__(command_prefix, **kwargs)
