import discord

from utils.bot import Bot
from utils.settings import settings

exts = ["cogs.cmd", "cogs.tasks"]

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = Bot(
    initial_extensions=exts,
    guild_id=settings.GUILD_ID,
    command_prefix="!",
    intents=intents,
)

try:
    if not settings.TOKEN:
        raise Exception("No token available.")

    bot.run(settings.TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
