import datetime
import discord
from discord.ext import commands, tasks
from discord import app_commands
from main import CONFIG
from calendar import month_name as monthNames

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthdayChannel = self.bot.get_channel(int(CONFIG["BIRTHDAY_CHANNEL_ID"]))
    
    def _ordinal(self, n: int) -> str: # Adds th, st, nd, and rd to the end of a day (e.g. 25th, 21st).
        s = ("th", "st", "nd", "rd") + ("th",) * 10
        v = n % 100
        if v > 13:
            return f"{n}{s[v % 10]}"
        else:
            return f"{n}{s[v]}"
    
    @tasks.loop(time=datetime.time(8,0,0,0))
    async def birthday(self):
        today = datetime.date.today()
        birthdays = self.bot.db.getAllBirthdays()
        for birthday in birthdays:
            (memberId, month, day) = birthday
            if today.month == month and today.day == day:
                user = await self.bot.fetch_user(memberId)
                if self.birthdayChannel:
                    await self.birthdayChannel.send(f"Happy Birthday {user.display_name}!")
                elif self.bot.defaultChannel:
                    await self.bot.defaultChannel.send(f"Happy Birthday {user.display_name}!")
    
    @app_commands.command(name="setbirthday", description="Sets your birthday. Required to use the Birthday functionality")
    @app_commands.describe(month="An integer between or equal to 1 and 12.",
                           day="An integer between or equal to 1 and 31.",
                           member="A Discord member. Requires administrator privileges.")
    async def setbirthday(self, interaction: discord.Interaction, month: int, day: int, member: discord.Member = None):
        if (1 <= month <= 12) and (1 <= day <= 31):
            if member and interaction.user.guild_permissions.administrator:
                self.bot.db.insertBirthday(member.id, month, day)
                await interaction.response.send_message(f"Set {member.display_name}'s birthday to {month}-{day}.", ephemeral=True)
            elif member:
                await interaction.response.send_message("You do not have sufficient permissions for this command.", ephemeral=True)
            else:
                self.bot.db.insertBirthday(interaction.user.id, month, day)
                await interaction.response.send_message(f"Set your birthday to {month}-{day}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"That is not a valid birthday.", ephemeral=True)

    @app_commands.command(name="getbirthday", description="Gets your birthday.")
    @app_commands.describe(member="A Discord member. Requires administrator privileges.")
    async def getbirthday(self, interaction: discord.Interaction, member: discord.Member = None):
        if member and interaction.user.guild_permissions.administrator: # Specified a member and is an admin
            birthday = self.bot.db.getBirthday(member.id)
            if birthday:
                (month, day) = birthday
                await interaction.response.send_message(f"{member.display_name}'s birthday is {monthNames[month]} {self._ordinal(day)} ({month}/{day}).", ephemeral=True)
            else:
                await interaction.response.send_message(f"{member.display_name} does not have a birthday set.", ephemeral=True)
        elif member: # Specified a member and is not an admin
            await interaction.response.send_message("You do not have sufficient permissions for this command.", ephemeral=True)
        else: # Did not specify anyone
            birthday = self.bot.db.getBirthday(interaction.user.id)
            if birthday:
                (month, day) = birthday
                await interaction.response.send_message(f"Your birthday is {monthNames[month]} {self._ordinal(day)} ({month}/{day}).", ephemeral=True)
            else:
                await interaction.response.send_message("You do not have a birthday set.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Birthday(bot), guilds=[discord.Object(id=int(CONFIG["GUILD_ID"]))])