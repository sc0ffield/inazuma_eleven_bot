import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from os import system
from json import dumps


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["=off", "=shutdown"])
    @commands.check(is_bot_owner)
    async def admin_off(self, ctx):
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔌 DESCONECTAR BOT", value=f"{ctx.author.mention}, Inazuma Eleven Bot será desconectado del servidor.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        await self.bot.logout()                                                    

        print("=" * 45)                                                           
        print(red("Inazuma Bot se ha desconectado..."))                    
        print("=" * 45 + "\n")                                                      


    @commands.command(aliases = ["=reboot", "=reload"])
    @commands.check(is_bot_owner)
    async def admin_reboot(self, ctx):
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 REINICIAR BOT", value=f"{ctx.author.mention}, Inazuma Eleven Bot será reiniciado.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        
        print("=" * 45 )                                                          
        print(red("Inazuma Eleven Bot se ha reiniciado."))                      
        print("=" * 45 + "\n")                                                     
        system("python main.py")                                                    


    @commands.command(aliases = ["=reloadcog"])
    @commands.check(is_bot_owner)
    async def admin_reload_cog(self, ctx, cog_name: str):
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 ACTUALIZAR COG", value=f"{ctx.author.mention}, el cog **{cog_name}** será actualizado.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        reload_cog(self.bot, cog_name)


    @commands.command(aliases = ["=give"])
    @commands.check(is_bot_owner)
    async def admin_give(self, ctx, target: discord.Member, item_id: str, item_float: float):
        inventories = get_file("inventories")
        items = get_file("items")
        if item_id in items:
            inventories[str(target.id)]["items"].append({"id": item_id, "float": item_float})
            update_file("inventories", inventories)
            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="➕ REGALAR", value=f"{ctx.author.mention}, `{item_id}:{item_float}` fue regalado a : {target.mention}")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await gen_error("missing_item", ctx)

    
    @commands.command(aliases=["=credit"])
    @commands.check(is_bot_owner)
    async def admin_credit(self, ctx, target: discord.Member, sum: int = 100):
        if is_registered(target.id):
            
            inventories = get_file("inventories")
            inventories[str(target.id)]["balance"] += sum
            update_file("inventories", inventories)

            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="💰 CRÉDITO",
                            value=f"{ctx.author.mention}, {target.mention} fue acreditado con `{sum}` monedas.")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)


    @commands.command(aliases=["=reset"])
    @commands.check(is_bot_owner)
    async def admin_reset(self, ctx, target: discord.Member):
        inventories = get_file("inventories")
        cooldowns = get_file("cooldowns")
        del inventories[str(target.id)]
        del cooldowns[str(target.id)]
        update_file("inventories", inventories)
        update_file("cooldowns", cooldowns)

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="♻️ REINICIAR CUENTA", value=f"{ctx.author.mention}, la cuenta de {target.mention} será eliminada.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=additem"])
    @commands.check(is_bot_owner)
    async def admin_add_item(self, ctx, *item_infos: tuple):
        items = get_file("items")
        item_infos = "".join(item_infos)
        item_id, item_name, item_from, item_desc, item_tier = item_infos.split(",")
        items[item_id] = {"name": item_name, "from": item_from, "description": item_desc, "tier": item_tier}
        update_file("items", items)

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="➕ AÑADIR ITEM", value=f"{ctx.author.mention}, el item : **{item_name}** ({item_id}) se ha añadido.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=skip"])
    @commands.check(is_bot_owner)
    async def admin_skip(self, ctx, target: discord.Member, category: str = "spin"):
        cooldowns = get_file("cooldowns")
        if category in cooldowns[str(target.id)]:
            cooldowns[str(target.id)][category] = 0
            update_file("cooldowns", cooldowns)
            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ ADMIN")
            embed.add_field(name="⏩ SALTAR COOLDOWN", value=f"{ctx.author.mention}, se ha saltado el cooldown `{category}` de {target.mention}")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await gen_error("invalid_synthax", ctx)


async def setup(client):
    await client.add_cog(Admin(client))
