from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from emoji import demojize


class Log(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.send_log = yellow("[SEND]")                                             
        self.edit_log = yellow("[EDIT]")
        self.del_log = yellow("[DELETE]")
        self.comands_list = get_commands_list()                                     

    @commands.Cog.listener(name = "on_message")
    async def on_message(self, message):
        if not message.author.bot:
            if message.content.split(" ")[0] in self.comands_list:
                if is_registered(message.author.id) or message.content in ["=start", "=help"]:
                    ctx = await self.bot.get_context(message)
                    async with ctx.typing():
                        await self.bot.process_commands(message)
                    print(demojize(f"[{get_time()}] : {self.send_log} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))


    @commands.Cog.listener(name = "on_message_edit")
    async def on_message_edit(self, before, after):
        print(demojize(f"[{get_time()}] : {self.edit_log} {blue(str(before.author.name))} {after.content} {red(f'({after.channel})')}"))


    @commands.Cog.listener(name = "on_message_delete")
    async def on_message_delete(self, message):
        print(demojize(f"[{get_time()}] : {self.del_log} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))


async def setup(client):
    await client.add_cog(Log(client))