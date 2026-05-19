import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, choices, randint, uniform
from time import time


class Claims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spin(self, ctx):
        cooldowns = get_file("cooldowns")

        if time() > (cooldowns[str(ctx.author.id)]['spin'] + (1)):

            inventories = get_file("inventories")
            items = get_file("items")

            s_tier = []
            a_tier = []
            b_tier = []
            c_tier = []
            d_tier = []

            for key in items.keys():
                if items[key]["tier"] in ["S+", "S", "S-"]:
                    s_tier.append(key)
                elif items[key]["tier"] in ["A+", "A", "A-"]:
                    a_tier.append(key)
                elif items[key]["tier"] in ["B+", "B", "B-"]:
                    b_tier.append(key)
                elif items[key]["tier"] in ["C+", "C", "C-"]:
                    c_tier.append(key)
                else:
                    d_tier.append(key)
                    
            tiers = {"S": s_tier, "A": a_tier, "B": b_tier, "C": c_tier, "D": d_tier}
            reward_tier = choices(["S", "A", "B", "C", "D"], weights=[10, 10, 10, 10, 10], k=1)[0]
            reward_key = choice(tiers[reward_tier])
            reward_float = round(uniform(0, 1), 3)
            tier_points, float_multiplicator = get_points(reward_tier, reward_float)
            reward_points = tier_points * float_multiplicator

            embed = discord.Embed(color=default_color)
            embed.set_author(name="⌛ JUGADOR ALEATORIO")
            embed = set_footer(embed, ctx)
            embed.add_field(name=f"**{items[reward_key]['name']}** ({tier_points} x {float_multiplicator} = {reward_points} PTS)",
                            value=f"*{items[reward_key]['description']}*  •  __{items[reward_key]['from']}__",
                            inline=False)
            embed.add_field(name="Tier", value=f"`{items[reward_key]['tier']}`", inline=True)
            embed.add_field(name="ID", value=f"`{reward_float}`", inline=True)
            embed.add_field(name="🇯🇵", value=f"`{items[reward_key]['jp']}`", inline=True)
            embed.set_image(url=f"{items[reward_key]['url']}")
            await ctx.send(embed=embed)

            inventories[str(ctx.author.id)]["items"].append({"id": reward_key, "float": reward_float, "points": reward_points})
            cooldowns[str(ctx.author.id)]["spin"] = time()
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

        else:
            await gen_error("cooldown_spin", ctx)


    @commands.command()
    async def daily(self, ctx):
        cooldowns = get_file("cooldowns")
        id_key = str(ctx.author.id)

        if time() > (cooldowns[id_key]["daily"] + (60 * 60 * 24)):

            inventories = get_file("inventories")
            reward_sum = randint(1, 500)

            embed = discord.Embed(color=default_color)
            embed.set_author(name="📅 RECOMPENSA DIARIA")
            embed.add_field(name="Recompensa :", value=f":moneybag: +`{reward_sum}` | Tu cartera : "
                                                   f"`{inventories[id_key]['balance'] + reward_sum}` monedas.")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

            cooldowns[id_key]["daily"] = time()
            inventories[id_key]["balance"] += reward_sum
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

        else:
            await gen_error("cooldown_daily", ctx)


async def setup(client):
    await client.add_cog(Claims(client))
