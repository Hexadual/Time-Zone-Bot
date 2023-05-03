import discord
import asyncio
from discord.ext import commands
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=CONFIG["COMMAND_PREFIX"], intents=intents)

async def main() -> None:
    async with bot:
        await bot.load_extension("cogs.clock")
        await bot.load_extension("cogs.birthday")
        await bot.start(token=CONFIG["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())









"""
class MyClient(discord.Client):
        
    @tasks.loop(time=dt.time(8,0,0,0))
    async def birthday(self):
        message_channel_id=555555555555555555
        message_channel=self.get_channel(message_channel_id)

        # List of birthdays
        BIRTHDAY_LIST = {
            'null': dt.date(2000, 1, 1),
            'null': dt.date(2000, 1, 1),
            'null': dt.date(2000, 1, 1),
            'null': dt.date(2000, 1, 1),
            'null': dt.date(2000, 1, 1),
        }
        today = dt.date.today()
        for name, birthday in BIRTHDAY_LIST.items():
            if today.month == birthday.month and today.day == birthday.day:
                await message_channel.send(f'Happy Birthday {name}!')

    async def on_ready(self):
        self.prefix = '$'
        self.ignore_list = []
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.birthday.start()

    #@birthday.before_loop
    #async def before(self):
    #    await self.wait_until_ready()
    #    print("Finished waiting")

    async def on_message(self, message):
        global DAYLIGHT
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # only respond to messages with the prefix
        if message.content.startswith(self.prefix):

            if "ignore" in message.content:
                self.ignore_list.append(message.author.id)

            if "attention" in message.content:
                self.ignore_list.remove(message.author.id)

            if "help" in message.content:
                await message.channel.send("``` Here are a list of commands \n * ignore : stop trying to guess my times \n * daylight : type yes if daylight or no if not \n * attention : try to guess my times```")

            ''' if "embed" in message.content:
                 names=[str(i) for i in range(10)]
                names = '\n'.join(names)
                embedVar = discord.Embed(title="Commands", description="A list of commands I use", color=0x00ff00)
                embedVar.add_field(name="Command", value=names, inline=True)
                embedVar.add_field(name="Description", value="", inline=True)
                await message.channel.send(embed=embedVar)'''

            if "daylight" in message.content:
                answer = message.content.split(' ')[1].lower()
                if answer == "yes":
                    DAYLIGHT = True
                elif answer == "no":
                    DAYLIGHT = False
                await message.channel.send("daylight set to " + DAYLIGHT)

        else:
            if message.author.id in self.ignore_list:
                return

            VALID_ROLES = {"atlantic", "east coast", "central", "mountain time", "west coast"}
            TZ_CODES = {"atlantic": "AST", "east coast": "EST", "central": "CST", "mountain time": "MDT", "west coast": "PST"}
            TZ_OFFSETS = {"atlantic": 4, "east coast": 5, "central": 6, "mountain time": 7, "west coast": 8}
            roles = [y.name.lower() for y in message.author.roles if y.name.lower() in VALID_ROLES]

            if not roles: return # No roles related to clock bot

            role = roles[0] # Use first role

            time_zone = TZ_CODES[role]

            if DAYLIGHT:
                offset = f"-0{TZ_OFFSETS[role] - 1}00"
            else:
                offset = f"-0{TZ_OFFSETS[role]}00"

            found = re.findall("((?:0?1?\d|2[0-3]):(?:[0-5]\d)(?: ?)|24:00(?: ?)|(?<!\d)[0-9]{1,2}(?: ?)(?=[apAP]))(?:(?<=[\d ])(am|AM|Am|pm|PM|Pm)\s?)?", message.content)
            
            if found != []:
                
                message_to_send = ""
                embedVar = discord.Embed(title="Time", description="Desc", color=0x00ff00)
                
                now = dt.datetime.now()
                current_time = now.time()
                current_date = now.date()

                for i in range(len(found)):
                    time_string = found[i][0] + "-" + found[i][1] +"-"+str(current_date)+"-"+offset
        
                    time_string = time_string.replace(" ","")
                    
                    ref_time = None

                    if (found[i][1]==""):

                        if ':' in time_string:
                            ref_time = dt.datetime.strptime(time_string, "%I:%M--%Y-%m-%d-%z")
                        else:
                            ref_time = dt.datetime.strptime(time_string, "%I--%Y-%m-%d-%z")
                        
                        if current_time > ref_time.time():
                            ref_time = ref_time + timedelta(hours=12)
                        
                    else:
                        if ':' in time_string:
                            ref_time = dt.datetime.strptime(time_string, "%I:%M-%p-%Y-%m-%d-%z")
                        else:
                            ref_time = dt.datetime.strptime(time_string, "%I-%p-%Y-%m-%d-%z")
                    
                    loc_time = ref_time
                    ts = get_unix_epochs(loc_time.astimezone())
                   
                    message_to_send += "*** "+ time_zone +":***  "+ ref_time.strftime("%I:%M %p") + " | ***Local:*** <t:"+str(int(ts))+":t> \n"
                    
                message_to_send = ">>> " + message_to_send
                
                await message.channel.send(message_to_send)
    
    
    def listRoles(self, message):
        return [role for role in message.guild.roles if role.color.value == 16777215] 

"""