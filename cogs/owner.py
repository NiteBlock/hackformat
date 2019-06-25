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


class Code(commands.Converter):
    async def convert(self, ctx, arg):
        return self.cleanup_code(arg)

    @staticmethod
    def cleanup_code(code):
        if code.startswith('```') and code.endswith('```'):
            return code.strip("```").strip("\n")
        return code.strip('\n')


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
    async def owner_eval(self, ctx, *, code: Code):
        stdout = io.StringIO()

        env = {
            'ctx': ctx,
            'bot': self.bot,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'message': ctx.message
        }
        print(code)
        env.update(globals())
        formatted_code = f'async def my_func(): \n{textwrap.indent(code, "  ")}'
        print(formatted_code)

        try:
            with redirect_stdout(stdout):
                exec(formatted_code, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['my_func']

        try:
            with redirect_stdout(stdout):
                func_return = await func()
        except:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()

            if not func_return:
                return await ctx.send(f"""```py\n Output: \n {value}```""")
            return await ctx.send(f"""```py\n Output: \n {value} \n Returned: \n {func_return} ```""")


def setup(bot):
    bot.add_cog(Owner(bot))
