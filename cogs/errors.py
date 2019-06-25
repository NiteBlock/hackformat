from discord.ext import commands


class ErrorHandler(commands.Cog):
    """Cog used to handle general command errors"""

    # Errors that are ignored
    ignore = [commands.CommandNotFound, commands.TooManyArguments]

    # Error Messages
    error_response = {
        commands.CheckFailure: "You do **Not** have permissions to do this!",
        commands.NoPrivateMessage: "This command doesn't work in private messges!",
        commands.CommandOnCooldown: "This command is on a cooldown: Retry after {e.retry.after}. You can only use this command {e.cooldown.rate} every {e.cooldown.per} Seconds!",
        commands.BadArgument: "Oops an invalid argument has been passed!",
        commands.BadUnionArgument: "An invalid argument has been passed for {e.parent.name}!",
        commands.MissingRequiredArgument: "You need the {e.param.name} for this command to work!"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
