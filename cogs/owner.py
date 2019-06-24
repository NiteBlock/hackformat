from discord.ext import commands
import json
import discord
from contextlib import redirect_stdout
import textwrap
import io
import traceback


def is_owner():
    async def predicate(ctx):
        with open("config.json", "r") as r:
            return ctx.author.id in json.load(r)["owners"]
    return commands.check(predicate)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="owner", invoke_without_command=True)
    async def owner(self, ctx):
        await ctx.send_help(self.owner)

    @owner.command(name="load")
    @is_owner()
    async def load_extension(self, ctx, extension: str):
        """Load an Extension"""

        embed = discord.Embed(title="Load Extension")
        try:
            self.bot.load_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except commands.ExtensionAlreadyLoaded:
            embed.add_field(name=extension, value="Success! Was Already Loaded!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @owner.command(name="unload")
    @is_owner()
    async def unload(self, ctx, extension: str):
        """Unload an extension"""

        embed = discord.Embed(title="Unload Extension")
        try:
            self.bot.unload_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @owner.command(name="reload")
    @is_owner()
    async def reload(self, ctx, extension: str):
        """Reload an extension"""

        embed = discord.Embed(title="Reload Extension")
        try:
            self.bot.reload_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @owner.command(name="list")
    @is_owner()
    async def list(self, ctx):
        embed = discord.Embed(title="Extensions", color=discord.Color.green())
        for extension in self.bot.extensions:
            embed.add_field(name=extension, value="Loaded!", inline=False)
        await ctx.send(embed=embed)

    @owner.command(name="eval")
    @is_owner()
    async def owner_eval(self, ctx, *, code: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        code = code.strip('```')
        print(code)

        code = f'async def my_func(): \n{textwrap.indent(code, "  ")}'

        print(code)

        stdout = io.StringIO()

        with redirect_stdout(stdout):
            exec(code, env)

        func = env['my_func']

        try:
            with redirect_stdout(stdout):
                output = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if not output:
                return await ctx.send(f"Value: \n ```{value}```")
            return await ctx.send(f"Value: \n ```{value} \n {output}```")


def setup(bot):
    bot.add_cog(Owner(bot))
