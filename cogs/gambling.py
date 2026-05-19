import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, randint


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx, bet: int = 10):
        if bet % 1 == 0 and bet > 0:
            inventories = get_file("inventories")
            if bet <= inventories[str(ctx.author.id)]["balance"]:

                inventories[str(ctx.author.id)]["balance"] -= bet
                win = choice([True, False])

                embed = discord.Embed(color=default_color)
                embed.set_author(name="🎲 CARA O CRUZ")
                embed = set_footer(embed, ctx)

                if win:
                    inventories[str(ctx.author.id)]["balance"] += bet * 2
                    update_file("inventories", inventories)
                    embed.add_field(name="Resultado",
                                    value=f":trophy: ¡Has ganado : **+**`{bet * 2}`! "
                                          f"Tu cartera : `{inventories[str(ctx.author.id)]['balance']}` monedas.")
                else:
                    update_file("inventories", inventories)
                    embed.add_field(name="Resultado",
                                    value=f":x: ¡Has perdido : **-**`{bet}`! "
                                          f"Tu cartera : `{inventories[str(ctx.author.id)]['balance']}` monedas.")
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_money", ctx)
        else:
            await gen_error("incorrect_value", ctx)


    @commands.command()
    async def bet(self, ctx, bet: int = 10, odd: int = 2):
        if bet >= 1:
            inventories = get_file("inventories")
            if bet <= inventories[str(ctx.author.id)]["balance"]:
                if randint(1, odd) == 1:
                    result_field = f"{ctx.author.mention}, has ganado **{odd}**x tu apuesta : **+**`{(bet * odd) - bet}`"
                    inventories[str(ctx.author.id)]["balance"] += bet * (odd - 1)
                else:
                    result_field = f"{ctx.author.mention}, has perdido tu apuesta : **-**`{bet}`"
                    inventories[str(ctx.author.id)]["balance"] -= bet
                update_file("inventories", inventories)
                embed = discord.Embed(color=default_color)
                embed.set_author(name="🎰 APUESTA")
                embed.add_field(name="Resultado", value=result_field)
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_money", ctx)
        else:
            await gen_error("incorrect_value", ctx)
            

async def setup(client):
    await client.add_cog(Gambling(client))