import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *

class GameInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, target: str = "*"):
        help = get_file("help_draft")
        if target == "*" or target in help.keys() or ("=" + target) in get_commands_list():            
            embed = discord.Embed(color=default_color)
            author_value = ""

            if target == "*":
                for key in help.keys():
                    embed.add_field(name=help[key]["display_name"],
                                    value=f"`=help {key}`", inline=True)

            elif target in help.keys():
                author_value += f" | {help[target]['display_name']}"
                help_lines = list(help[target].keys())
                help_lines.remove("display_name")
                for key in help_lines:
                    embed.add_field(name=f"🔹 {help[target][key]['title']}",
                                    value=f"{help[target][key]['desc']}", inline=False)

            elif ("=" + target) in get_commands_list():
                commands_dict = get_commands_dict()
                default_cmd_name = commands_dict[target]
                for category in list(help.keys()):
                    try:
                        embed.add_field(name=f"🔹 {help[category][default_cmd_name]['title']}",
                                        value=help[category][default_cmd_name]['desc'])
                    except KeyError:
                        pass
                
            embed.set_author(name=author_value)
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await gen_error("invalid_synthax", ctx)


    @commands.command()
    async def items(self, ctx):
        embed = discord.Embed(color=default_color)
        embed.set_author(name="📜 LISTA DE JUGADORES")

        if ctx.message.channel.type == discord.ChannelType.text:
            info_field = f"{ctx.author.mention}, la lista de jugadores se te enviará por DM. "\
                         "La lista puede tardar algo de tiempo en generarse.\n\n"                              \
                         ":warning: Algunas columnas pueden estar desalineadas con las demás."
        
        else:
            info_field = f":warning: {ctx.author.mention}, algunas columnas pueden estar desalineadas con las demás. " 

        embed.add_field(name="Información", value=info_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)

        name_column = ""
        tier_column = ""
        from_column = ""

        items = dict(sorted(get_file("items").items(), key = lambda item: item[1]["name"]))
        item_index = 0
        page = 1
        finished = False

        embed = discord.Embed(color=default_color)
        embed.add_field(name="Nombre", value="*")
        embed.add_field(name="Tier", value="*")
        embed.add_field(name="Equipo", value="*")
        
        for item_key in list(items.keys()):
            if len(embed) <= 6000 and                                                                         \
               len(embed.fields[0].value) + len(f"{items[item_key]['name']}\n") < 1024 and   \
               len(embed.fields[1].value) + len(f"{items[item_key]['tier']}\n") < 1024 and              \
               len(embed.fields[2].value) + len(f"{items[item_key]['from']}\n") < 1024:
                   
                embed.set_author(name=f"📜 LISTA DE JUGADORES | Página n°{page}")
                name_column += f"{items[item_key]['name']}\n"
                tier_column += f"{items[item_key]['tier']}\n"
                from_column += f"{items[item_key]['from']}\n"

                embed.clear_fields()

                embed.add_field(name="Nombre", value=name_column)
                embed.add_field(name="Tier", value=tier_column)
                embed.add_field(name="Equipo", value=from_column)
                embed = set_footer(embed, ctx)
                   
            else:
                await ctx.author.send(embed=embed)
                
                embed.clear_fields()
                embed.add_field(name="Nombre", value="*")
                embed.add_field(name="Tier", value="*")
                embed.add_field(name="Equipo", value="*")

                name_column = ""
                tier_column = ""
                from_column = ""
                page += 1
                
        await ctx.author.send(embed=embed)

    @commands.command()
    async def powers(self, ctx):
        embed = discord.Embed(color=default_color)
        embed.set_author(name="⚡ LISTA DE SUPERTÉCNICAS")

        if ctx.message.channel.type == discord.ChannelType.text:
            info_field = f"{ctx.author.mention}, la lista de jugadores se te enviará por DM. "\
                         "La lista puede tardar algo de tiempo en generarse.\n\n"                              \
                         ":warning: Algunas columnas pueden estar desalineadas con las demás."
        
        else:
            info_field = f":warning: {ctx.author.mention}, algunas columnas pueden estar desalineadas con las demás. " 

        embed.add_field(name="Información", value=info_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)

        name_column = ""
        desc_column = ""
        n = 1

        powers = dict(sorted(get_file("powers").items(), key = lambda item: item[1]["name"]))
        power_index = 0
        page = 1
        finished = False

        embed = discord.Embed(color=default_color)
        embed.add_field(name="Nombre", value="*")
        embed.add_field(name="Descripción", value="*")
        
        for power_key in list(powers.keys()):
            if len(embed) <= 6000 and                                                                        \
               len(embed.fields[0].value) + len(f"{powers[power_key]['name']}\n") < 1024 and          \
               len(embed.fields[1].value) + len(f"{powers[power_key]['desc']}\n") < 1024:\
            
                embed.set_author(name=f"⚡ LISTA DE SUPERTÉCNICAS | Página n°{page}")
                name_column += "**["+str(n)+"]** "+f"{powers[power_key]['name']}\n"
                desc_column += f"{powers[power_key]['desc']}\n"

                n += 1
                embed.clear_fields()

                embed.add_field(name="Nombre", value=name_column)
                embed.add_field(name="Descripción", value=desc_column)
                embed = set_footer(embed, ctx)
                   
            else:
                await ctx.author.send(embed=embed)
                
                embed.clear_fields()
                embed.add_field(name="Nombre", value="*")
                embed.add_field(name="Descripción", value="*")

                name_column = ""
                desc_column = ""
                page += 1
                
        await ctx.author.send(embed=embed)

    @commands.command()
    async def players(self, ctx):
        inventories = get_file("inventories")
        players_field = ""

        if list(inventories.keys()):
            for player_id in inventories.keys():
                players_field += f"• <@{player_id}>\n"
        else:
            players_field = "🍂 `Aún no hay usuarios...` 🕸️"

        embed = discord.Embed(color=default_color)
        embed.set_author(name="👥 LISTA DE USUARIOS")
        embed.add_field(name="Usuarios", value=players_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["stats"])
    async def statistics(self, ctx):
        stats = get_file("statistics")
        inventories = get_file("inventories")

        game_field = ""
        game_field += f"total de **spin** : `{stats['spin']}`\n"
        game_field += f"total de **daily** : `{stats['daily']}`\n"
        game_field += f"total de **trade** : `{stats['trade']}`\n"
        game_field += f"total de **pay** : `{stats['pay']}`"

        money_qtty = 0
        points_qtty = 0
        items_qtty = 0
        
        for player in inventories.keys():
            money_qtty += inventories[player]["balance"]
        for player in inventories.keys():
            items_qtty += len(inventories[player]["items"])
            for item in inventories[player]["items"]:
                points_qtty += item["points"]

        qtty_field = f"total de **monedas** : `{money_qtty}`\n"  \
                     f"total de **jugadores** : `{items_qtty}`\n"              \
                     f"total de **puntos** : `{points_qtty}`"

        bot_field = f"número de **usuarios** : `{len(list(inventories.keys()))}`\n"         \
                    f"número de **servers** : `{len(self.bot.guilds)}`\n"                  \
                    f"**ID** del propietario : `{open('data/metadata/owner.id.txt', 'r').read()}`\n" \
                    f"**latencia** : `{self.bot.latency}` s."

        embed = discord.Embed(color=default_color)
        embed.set_author(name="📊 ESTADÍSTICAS")
        embed.add_field(name="Comandos", value=game_field, inline=False)
        embed.add_field(name="Patrimonio", value=qtty_field, inline=False)
        embed.add_field(name="Bot", value=bot_field,  inline=False)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(GameInfo(client))
