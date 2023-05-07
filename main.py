import discord
import asyncio
from discord.ext import commands
from dotenv import dotenv_values
import db

CONFIG = dotenv_values(".env")
DATABASE = db.Database("sqlite.db")

class TimeZoneBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=CONFIG["COMMAND_PREFIX"], intents=intents, application_id=int(CONFIG["APPLICATION_ID"]))
        self.db = db.Database("sqlite.db")
    
    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=int(CONFIG["GUILD_ID"])))

async def main() -> None:
    bot = TimeZoneBot()
    async with bot:
        await bot.load_extension("cogs.clock")
        await bot.load_extension("cogs.birthday")
        await bot.start(token=CONFIG["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
