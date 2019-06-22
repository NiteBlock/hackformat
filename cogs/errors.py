#the handeling of errors:
from discord.ext import commands

#ingored errors
ignore = [commands.CommandNotFound, commands.TooManyArguments]

#the format for each error that can happen
#e will be the error from an on_command_Error event using .format(e=error, c=ctx) most proabbly if we need the context
format = {
    commands.CheckFailure: "You do **Not** have permissions to do this!",
    commands.NoPrivateMessage: "This command doesn't work in private messges!",
    commnads.CommandOnCooldown: "This command is on a cooldown: Retry after {e.retry_after}. You can only use this command {e.cooldown.rate} every {e.cooldown.per} Seconds!",
    commands.BadArgument : "Oops an invalid argument has been passed!",
    commands.BadUnionArgument: "An invalid argument has been passed for {e.paran.name}!"
    commands.MissingRequiredArgument: "You need the {e.param.name} for this command to work!"
}
