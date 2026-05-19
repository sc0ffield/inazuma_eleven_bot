import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["baltop"])
    async def balancetop(self, ctx):
        inventories = get_file("inventories")
        balances = {}
        for player in inventories.keys():
            balances[player] = inventories[player]["balance"]

        baltop = sorted(balances.items(), key=lambda x: x[1], reverse=True)
        player_field = ""
        amount_field = ""
        rank = 1

        for player in baltop:
            player_field += f"`#{rank}` <@{player[0]}>\n"
            amount_field += f"`{player[1]}`\n"
            rank += 1

        embed = discord.Embed(color=default_color)
        embed.set_author(name="🏆 CLASIFICACIÓN POR DINERO")
        embed.add_field(name="[#] Usuario", value=player_field)
        embed.add_field(name="Monedas", value=amount_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["ptop", "scoretop", "stop"])
    async def pointstop(self, ctx):
        inventories = get_file("inventories")
        players_points = {}

        for player in inventories.items():
            player_points = 0
            for item in player[1]["items"]:
                player_points += item["points"]
            players_points[player[0]] = player_points

        ptop = sorted(players_points.items(), key=lambda x: x[1], reverse=True)

        player_field = ""
        points_field = ""
        rank = 1

        for player in ptop:
            player_field += f"`#{rank}` <@{player[0]}>\n"
            points_field += f"`{player[1]}`\n"
            rank += 1

        embed = discord.Embed(color=default_color)
        embed.set_author(name="🏆 CLASIFICACIÓN POR PRESTIGIO")
        embed.add_field(name="[#] Usuario", value=player_field)
        embed.add_field(name="Puntos", value=points_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Leaderboards(client))
