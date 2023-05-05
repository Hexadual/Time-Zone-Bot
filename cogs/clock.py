import re
import datetime
import time
import discord
from discord.ext import commands
from discord import app_commands
from main import CONFIG

class Clock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temporaryStorage = {} # TODO: Implement permanent storage
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if not message.author.id in self.temporaryStorage:
            return
        
        sign = "-" if self.temporaryStorage[message.author.id] - time.daylight < 0 else "+"
        offset = f"{sign}{abs(self.temporaryStorage[message.author.id] + time.daylight):02d}00"
        
        found = re.findall("((?:0?1?\d|2[0-3]):(?:[0-5]\d)(?: ?)|24:00(?: ?)|(?<!\d)[0-9]{1,2}(?: ?)(?=[apAP]))(?:(?<=[\d ])(am|AM|Am|pm|PM|Pm)\s?)?", message.content)
        
        if found: 
            now = datetime.datetime.now()
            currentTime = now.time()
            currentDate = now.date()

            for i in range(len(found)):
                timeString = f"{found[i][0]}-{found[i][1]}-{str(currentDate)}-{offset}"
                timeString = timeString.replace(" ", "")
                referenceTime = None
                if found[i][1] == "":
                    if ":" in timeString:
                        referenceTime = datetime.datetime.strptime(timeString, "%I:%M--%Y-%m-%d-%z")
                    else:
                        referenceTime = datetime.datetime.strptime(timeString, "%I--%Y-%m-%d-%z")

                    if currentTime > referenceTime.time():
                        referenceTime = referenceTime + datetime.timedelta(hours=12)
                else:
                    if ":" in timeString:
                        referenceTime = datetime.datetime.strptime(timeString, "%I:%M-%p-%Y-%m-%d-%z")
                    else:
                        referenceTime = datetime.datetime.strptime(timeString, "%I-%p-%Y-%m-%d-%z")

                locationTime = referenceTime
                totalSeconds = (locationTime.astimezone() - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()
                messageToSend = "*** " + message.author.display_name + ":***  " + referenceTime.strftime("%I:%M %p") + " | ***Local:*** <t:" + str(int(totalSeconds)) + ":t> \n"
 
            messageToSend = f">>> {messageToSend}"
            await message.channel.send(messageToSend)
    
    @app_commands.command(name="setutcoffset",
                          description="Sets your UTC offset. Required to use the Clock functionality.")
    @app_commands.describe(offset="An integer between -12 and 14.")
    async def setutcoffset(self, interaction: discord.Interaction, offset: int) -> None:
        if -12 <= offset <= 14:
            self.temporaryStorage[interaction.user.id] = offset
            await interaction.response.send_message("Successfully set your UTC offset.", ephemeral=True)
        else:
            await interaction.response.send_message("That is not a valid UTC offset.", ephemeral=True)
    
    @app_commands.command(name="getutcoffset",
                          description="Gets your UTC offset.")
    async def getutcoffset(self, interaction: discord.Interaction) -> None:
        if interaction.user.id in self.temporaryStorage:
           offset = self.temporaryStorage[interaction.user.id]
           await interaction.response.send_message(f"Your UTC offset is {offset}.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have a UTC offset.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clock(bot), guilds=[discord.Object(id=int(CONFIG["GUILD_ID"]))])
