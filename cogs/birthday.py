import datetime
import discord
from discord.ext import commands, tasks
from discord import app_commands
from main import CONFIG

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temporaryStorage = {} # TODO: Implement permanent storage
        self.channelId = CONFIG["BIRTHDAY_CHANNEL_ID"]
    
    @tasks.loop(time=datetime.time(8,0,0,0))
    async def birthday(self):
        if self.channelId:
            channel = self.get_channel(self.channelId)
            today = datetime.date.today()
            for userId, birthday in self.temporaryStorage.items():
                if today.month == birthday[0] and today.day == birthday[1]:
                    user = await self.fetch_user(userId)
                    await channel.send(f"Happy Birthday {user.display_name}!")
    
    @app_commands.command(name="setbirthday", description="Sets your birthday. Required to use the Birthday functionality")
    @app_commands.describe(month="An integer between or equal to 1 and 12.",
                           day="An integer between or equal to 1 and 31.",
                           member="A Discord member. Requires administrator privileges.")
    async def setbirthday(self, interaction: discord.Interaction, month: int, day: int, member: discord.Member = None):
        if (1 <= month <= 12) and (1 <= day <= 31):
            if member and interaction.user.guild_permissions.administrator:
                self.temporaryStorage[member.id] = (month, day)
                await interaction.response.send_message(f"Set {member.display_name}'s birthday to {month}-{day}.", ephemeral=True)
            elif member:
                await interaction.response.send_message("You do not have sufficient permissions for this command.", ephemeral=True)
            else:
                self.temporaryStorage[interaction.user.id] = (month, day)
                await interaction.response.send_message(f"Set your birthday to {month}-{day}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"That is not a valid birthday.", ephemeral=True)

    @app_commands.command(name="getbirthday", description="Gets your birthday.")
    @app_commands.describe(member="A Discord member. Requires administrator privileges.")
    async def getbirthday(self, interaction: discord.Interaction, member: discord.Member = None):
        if member and interaction.user.guild_permissions.administrator:
            birthday = self.temporaryStorage[member.id]
            await interaction.response.send_message(f"{member.display_name}'s birthday is {birthday[0]}-{birthday[1]}.", ephemeral=True)
        elif member:
            await interaction.response.send_message("You do not have sufficient permissions for this command.", ephemeral=True)
        else:
            birthday = self.temporaryStorage[interaction.user.id]
            await interaction.response.send_message(f"Your birthday is {birthday[0]}-{birthday[1]}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Birthday(bot), guilds=[discord.Object(id=int(CONFIG["GUILD_ID"]))])