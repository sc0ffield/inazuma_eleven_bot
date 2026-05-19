from discord import Embed
from discord.ext import commands
from time import strftime
from json import loads, dumps
from modules.chat_effects import default_color, error_color, warning_color, admin_color
from os import listdir

def get_time() -> str:
    return strftime("%H:%M:%S")

def get_file(filename: str) -> dict:
    return loads(open(f"data/gamedata/{filename}.json", "r", encoding="utf-8").read())

def is_registered(user_id: str) -> bool:
    inventories = get_file("inventories")
    return str(user_id) in inventories

def is_bot_owner(ctx: commands.Context) -> bool:
    return ctx.author.id == int(open("data/metadata/owner.id.txt", "r").read())

async def gen_error(error_id: str, ctx: commands.Context) -> Embed:
    errors = get_file("errors")
    error = Embed(color=error_color)
    error.add_field(name="⚠️ " + errors[error_id]["title"], value=errors[error_id]['txt'])
    error = set_footer(error, ctx)
    await ctx.send(embed=error)

def set_footer(embed: Embed, ctx: commands.Context) -> Embed:
    return embed.set_footer(icon_url=ctx.author.avatar.url, text=f"{ctx.author.display_name} • {get_time()}")

def update_file(filename: str, variable_dict: dict) -> None:
    try:
        file = open(f"data/gamedata/{filename}.json", "w", encoding="utf-8")
        file.write(dumps(variable_dict, indent=3))
        file.close()
    except TypeError:
        print("TypeError")

def get_points(item_tier: str, item_float: float) -> tuple:
    POINTS_SCALE = {"S": 100, "A": 25, "B": 10, "C": 5, "D": 1}
    tier_points = POINTS_SCALE[item_tier]
    if 1.000 > item_float > 0.200:
        float_multiplicator = 1
    elif 0.199 > item_float > 0.100:
        float_multiplicator = 1.5
    elif 0.099 > item_float > 0.010:
        float_multiplicator = 5
    elif 0.009 > item_float > 0.000:
        float_multiplicator = 10
    return (tier_points, float_multiplicator)

async def target_parser(ctx: commands.Context, target: str) -> tuple:
    if target is None:
        target = ctx.author
        target_found = True
    else:
        try:
            target = await commands.MemberConverter().convert(ctx, target)
            target_found = True
        except commands.BadArgument:
            target_found = False
    return (target_found, target)

def load_cogs(bot: commands.Bot, cog_name: str) -> None:
    bot.load_extension(f"cogs.{cog_name}")

def unload_cog(bot: commands.Bot, cog_name: str) -> None:
    bot.unload_extension(f"cogs.{cog_name}")

def reload_cog(bot: commands.Bot, cog_name: str) -> None:
    unload_cog(bot, cog_name)
    load_cogs(bot, cog_name)

def get_commands_list() -> list:
    return open("data/metadata/commands.list.txt", "r").read().split("\n")

def get_commands_dict() -> dict:
    commands_dict = {}
    f =  open(f"data/metadata/commands.dict.txt", "r", encoding="utf-8").read()
    for command in f.split("\n"):
        commands_dict[command.split(":")[0]] = command.split(":")[1]
    return commands_dict

def check_embed(embed: Embed) -> bool:
    if len(embed) <= 6000:
        if hasattr(embed, "title"):
            if len(embed.title) <= 256:
                pass
            else:
                return False
        if len(embed.fields) <= 25:
            for field in embed.fields:
                if len(field.name) <= 69420:
                    pass
        
        