import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from modules.bot_functions import *
from modules.chat_effects import *


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        if not is_registered(ctx.author.id):

            inventories = get_file("inventories")
            cooldowns = get_file("cooldowns")
            cooldowns[str(ctx.author.id)] = {"daily": 0, "spin": 0}
            inventories[str(ctx.author.id)] = {"balance": 0,
                                               "items": [],
                                               "packs": {},
                                               "powers": [],
                                               "shares":{},
                                               "shield_active": False}
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name="🚩 INSCRIPCIÓN")
            embed.add_field(name="¡Bienvenido al universo de Inazuma Eleven!", value=f"{ctx.author.mention}, empieza a formar tu equipo definitivo.")
            embed.set_image(url="https://static.wikia.nocookie.net/logocreation/images/c/c9/Logo.png/revision/latest/scale-to-width-down/572?cb=20150124162049&path-prefix=es")
            await ctx.send(embed=embed)
            embed = set_footer(embed, ctx)

        else:
            await gen_error("account_existing", ctx)

    
    @commands.command(aliases=["delete account", "ragequit"])
    async def delete_account(self, ctx):
        confirmation_text = "Estás a punto de eliminar definitivamente tu \
                            cuenta del juego. Tus jugadores, paquetes, acciones y potenciadores serán \
                            también eliminado permanentemente. Nunca serás \
                            reembolsado y tus posesiones no serán restituidas.\n\
                            Confirme esta acción:"


        embed = discord.Embed(color=warning_color)
        embed.set_author(name="🗑️ ELIMINAR CUENTA")
        embed.add_field(name="Todos tus datos serán borrados", value=confirmation_text)
        embed = set_footer(embed, ctx)
        confirmation = await ctx.send(embed=embed)

        await confirmation.add_reaction("✅")
        await confirmation.add_reaction("❌")

        check = lambda reaction, reaction_user: reaction.emoji in ["✅", "❌"] and reaction_user.id == ctx.author.id

        try:
            reaction, reaction_user = await self.bot.wait_for("reaction_add", check=check, timeout=10.0)
            
            if reaction.emoji == "✅":
                cooldowns = get_file("cooldowns")
                inventories = get_file("inventories")
                market = get_file("market")
                
                del cooldowns[str(ctx.author.id)]
                del inventories[str(ctx.author.id)]
                for offer in market["offers"]:
                    if offer["seller"] == ctx.author.id:
                        market["offers"].remove(offer)
                        
                update_file("cooldowns", cooldowns)
                update_file("inventories", inventories)
                update_file("market", market)
                
                embed.clear_fields()
                embed.add_field(name="¡Hasta pronto!", value=f"{ctx.author.mention} tu cuenta se ha eliminado definitivamente.")
                embed.set_image(url="https://static.wikia.nocookie.net/logocreation/images/c/c9/Logo.png/revision/latest/scale-to-width-down/572?cb=20150124162049&path-prefix=es")
                embed = set_footer(embed, ctx)
                await confirmation.edit(embed=embed)
                
            elif reaction.emoji == "❌":
                await confirmation.delete()
                await gen_error("canceled", ctx)
            
        except asyncio.TimeoutError:
            await confirmation.delete()
            await gen_error("timeout", ctx)

async def setup(client):
    await client.add_cog(Account(client))
