import discord
from discord.ext import commands
from utils.storage import Storage

from typing import Optional

class Bot(commands.Bot):
    storage = Storage()

    def __init__(
            self,
            initial_extensions: list[str],
            guild_id: Optional[int] = None,
            *args,
            **kwargs
            ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.guild_id = guild_id

    async def setup_hook(self) -> None:
        print("initiation of setup hook ...")

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        if not self.guild_id:
            return
        
        guild = discord.Object(self.guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')

        # 診斷步驟：列印機器人可存取的所有公會 ID
        print("Accessible Guild IDs:")
        for guild in self.guilds:
            print(f"- {guild.name}: {guild.id}")
