import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, uniform, randint

class Powers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def use(self, ctx, power: str):
        author_key = str(ctx.author.id)
        inventories = get_file("inventories")
        if not power in inventories[author_key]["powers"]:
            powers = get_file("powers")
            embed = discord.Embed(color=default_color)
            embed.set_author(name="⚡️ SUPERTÉCNICA")
            embed.add_field(name="", value="¡"+f"{ctx.author.mention} ha usado `{powers[power]['name']}`!")
            embed = set_footer(embed, ctx)
            embed.set_image(url=f"{powers[power]['url']}")
            await ctx.send(embed=embed)

        else:
            await gen_error("missing_power", ctx)

async def setup(client):
    await client.add_cog(Powers(client))