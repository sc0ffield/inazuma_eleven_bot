import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, target: str = None):
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                items = get_file("items")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"📦 INVENTARIO de {target.name}")

                if inventories[str(target.id)]["items"]:
                    name_column  = ""
                    tier_column  = ""
                    float_column = ""

                    for item in inventories[str(target.id)]["items"]:
                        name_column += f"• **{items[item['id']]['name']}** `{items[item['id']]['from']}` \n"
                        tier_column += f" *{items[item['id']]['tier']}* \n"
                        showed_float = str(item["float"])
                        for i in range(5 - len(str(item["float"]))):
                            showed_float += "0"
                        float_column += f" __{showed_float}__ • **{item['points']}**\n"
                    embed.add_field(name = "Jugadores", value=name_column)
                    embed.add_field(name = "Tier", value=tier_column)
                    embed.add_field(name = "ID • Puntos", value=float_column)
                else:
                    embed.add_field(name = "Jugadores", value="`¡Todavía no tienes a ningún jugador!`", inline=False)

                if inventories[str(target.id)]["powers"]:
                    powers = get_file("powers")
                    powers_column = ""
                    for power in inventories[str(target.id)]["powers"]:
                        powers_column += f"• **{powers[power]['name']}** `{power}`\n"
                    embed.add_field(name="Supertécnicas", value=powers_column, inline=False)
                else:
                    embed.add_field(name="Supertécnicas", value="`¡Tus jugadores todavía no han aprendido ninguna supertécica!`", inline=False)

                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)


    @commands.command(aliases=["bal"])
    async def balance(self, ctx, target: str = None):
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"💰 CARTERA de {target.name}")
                embed.add_field(name="Cartera", value=f"`{inventories[str(target.id)]['balance']}` monedas.")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)
            

    @commands.command(aliases=["pts", "score"])
    async def points(self, ctx, target: str = None):
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                player_points = 0
                for item in inventories[str(ctx.author.id)]["items"]:
                    player_points += item["points"]
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"⭐ PRESTIGIO de {target.name}")
                embed.add_field(name="Puntos", value=f"`{player_points}` puntos de prestigio.")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)


async def setup(client):
    await client.add_cog(UserInfo(client))
