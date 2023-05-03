import re
import datetime
from discord.ext import commands
from main import CONFIG

class Clock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        #if CONFIG["DAYLIGHT"]:
            #offset = f"-0{TZ_OFFSETS[role] - 1}00"
        #else:
            #offset = f"-0{TZ_OFFSETS[role]}00"
        offset = "-0500"
        # ^ Fix offset

        found = re.findall("((?:0?1?\d|2[0-3]):(?:[0-5]\d)(?: ?)|24:00(?: ?)|(?<!\d)[0-9]{1,2}(?: ?)(?=[apAP]))(?:(?<=[\d ])(am|AM|Am|pm|PM|Pm)\s?)?", message.content)
        
        if found:
            
            messageToSend = ""
            
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
                
                messageToSend += "*** " + "EST" + ":***  " + referenceTime.strftime("%I:%M %p") + " | ***Local:*** <t:" + str(int(totalSeconds)) + ":t> \n"
                # ^ Fix time zones
                
            messageToSend = f">>> {messageToSend}"

            await message.channel.send(messageToSend)

async def setup(bot):
    await bot.add_cog(Clock(bot))
