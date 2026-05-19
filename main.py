import discord                                                                   
from os import listdir, chdir, path, system
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *

abspath = path.abspath(__file__)                     
dname = path.dirname(abspath)
chdir(dname)
system("cls")

print("INAZUMA BOT")

token = ''                           
description = open("data/metadata/description.txt", "r").read()
bot = commands.Bot(command_prefix="=",
                   description=description,
                   case_insensitive=True,
                   intents = discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():                                                             
    commands_list = []                                                           
    commands_dict = {}
    bot_is_ready = False
    if not bot_is_ready:                                                            
        bot_is_ready = True                                                        
        print(f"BOT: "+bot.user.name)
        print(f"ID: "+str(bot.user.id))
        for filename in listdir("./cogs"):                                          
            if filename.endswith(".py"):                                           
                await bot.load_extension(f"cogs.{filename[:-3]}")                       
                cog = bot.get_cog(filename[:-3])
                cog_methods = cog.get_commands() + cog.get_listeners()
                for method in cog_methods:
                    if isinstance(method, commands.Command):
                        commands_list.append(f"={method.name}")
                        commands_dict[method.name] = method.name
                        for aliases in method.aliases:
                            commands_list.append(f"={aliases}")
                            commands_dict[aliases] = method.name
        print("Commands log:\n")

        f = open("data/metadata/commands.list.txt", "w")                           
        commands_list += ["+in", "-in", "+out", "-out"]
        f.write("\n".join(commands_list))
        f.close()                                                                   

        f = open("data/metadata/commands.dict.txt", "w")                           
        commands_str = [f"{key}:{value}" for (key, value) in commands_dict.items()]
        f.write("\n".join(commands_str))
        f.close()

        bot.owner_id = open("data/metadata/owner.id.txt", "r").read()               

@bot.event
async def on_message(message):                                                      
    pass                                                                           
                                                                                   
bot.run(token)                                                                      