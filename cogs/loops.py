import discord
import asyncio
from discord.ext import commands, tasks
from modules.bot_functions import *
from modules.chat_effects import *
from random import randint, choice
from os import listdir, mkdir, getcwd
from os.path import getsize
from time import strftime
from shutil import copyfile
from hurry.filesize import size
from random import randint


class Loops(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.calc_event.start()
        self.change_status.start()
        self.save_data.start()
        self.stocks_evolution.start()
        self.loop_num_backup = 0
        self.loop_num_stocks = 0

    @tasks.loop(hours=1)
    async def calc_event(self):
        if randint(1, 5) == 1:
            a = randint(-10, 10)
            b = randint(-10, 10)
            c = randint(-10, 10)
            operator_1 = choice(["+", "-", "*"])
            operator_2 = choice(["+", "-", "*"])
            calc = f"{a} {operator_1} {b} {operator_2} {c}"
            result = eval(calc)
            chosen_guild = choice(self.bot.guilds)
            chosen_channel = choice(chosen_guild.text_channels)

            embed = discord.Embed(color=admin_color)
            embed.set_author(name="⏱️ EVENTO ALEATORIO")
            embed.add_field(name="Reto de cálculo", value=f"El primero en resolver este cálculo antes de 20 segundos gana una recompensa :\n```{calc} = ?```")
            embed.set_footer(text=f"EVENTO ALEATORIO • {get_time()}", icon_url=self.bot.user.avatar.url)
            random_event = await chosen_channel.send(embed=embed)
            print(f"[{get_time()}] : {yellow('[EVENT]')} {blue('Reto de cálculo')} : {str(calc)} = {str(result)} {red('(' + chosen_channel.name + ')')}")

            def check(msg):
                return msg.channel == chosen_channel and int(msg.content) == result and is_registered(msg.author.id)

            try:
                answer = await self.bot.wait_for("message", check=check, timeout=20.0)
            except asyncio.TimeoutError:
                embed.clear_fields()
                embed.add_field(name="Reto de cálculo", value=f"```{calc} = {result}```", inline=False)
                embed.add_field(name="¡Se acabó el tiempo!", value=":x: Nadie respondió antes de que terminara el cronómetro (20 seg.)", inline=False)
                await random_event.edit(embed=embed)
                await random_event.delete(delay=300.0)
            else:
                inventories = get_file("inventories")
                powers = get_file("powers")
                reward = choice(list(powers.keys()))
                inventories[str(answer.author.id)]["powers"].append(reward)
                update_file("inventories", inventories)

                embed.clear_fields()
                embed.add_field(name="Reto de cálculo", value=f"```{calc} = {result}```")
                embed.add_field(name="Recompensa", value=f"{answer.author.mention} ha desbloqueado la supertécnica : `{reward}`", inline=False)
                await random_event.edit(embed=embed)
                await random_event.delete(delay=300.0)


    @tasks.loop(minutes=5)
    async def change_status(self):
        presences = open("data/metadata/presences.txt", "r").read().split("\n")
        presence = choice(presences)
        presence_type = presence.split(" ")[0]
        presence_name = " ".join(presence.split(" ")[1:])
        ACTIVITY_TYPES = {
            "movie": discord.ActivityType.watching,
            "game": discord.ActivityType.playing,
            "song": discord.ActivityType.listening 
        }
        activity = discord.Activity(type=ACTIVITY_TYPES[presence_type], name=f"{presence_name} | =help")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)


    @tasks.loop(hours=2)
    async def save_data(self):
        if self.loop_num_backup > 1:
            backup_folder = strftime("%d-%m-%Y_%H.%M.%S")
            mkdir(f"backup/{backup_folder}")
            for filename in listdir("./data"):
                if filename[:-5] in ["inventories", "cooldowns", "market"]:
                    copyfile(f"data/{filename}", f"backup/{backup_folder}/{filename}")

            save_size = 0
            backup_directory_size = 0
            
            for backup_directory in listdir("./backup"):
                for file in listdir(f"./backup/{backup_directory}"):
                    file_size = getsize(f"{getcwd()}\\backup\{backup_directory}\{file}")
                    if backup_directory == backup_folder:
                        save_size += file_size
                    backup_directory_size += file_size
            print(f"[{get_time()}] : {yellow('[BACKUP]')} backup/{backup_folder} {red(f'(SIZE (in bytes) > save : {size(save_size)}o | directory : {size(backup_directory_size)}o)')}")
        self.loop_num_backup += 1

async def setup(client):
    await client.add_cog(Loops(client))
