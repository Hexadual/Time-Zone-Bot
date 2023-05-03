import datetime
from discord.ext import commands, tasks

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(time=datetime.time(8,0,0,0))
    async def birthday(self):
        message_channel_id=555555555555555555
        message_channel=self.get_channel(message_channel_id)

        # List of birthdays
        BIRTHDAY_LIST = {
            'null': datetime.date(2000, 1, 1),
            'null': datetime.date(2000, 1, 1),
            'null': datetime.date(2000, 1, 1),
            'null': datetime.date(2000, 1, 1),
            'null': datetime.date(2000, 1, 1),
        }
        today = datetime.date.today()
        for name, birthday in BIRTHDAY_LIST.items():
            if today.month == birthday.month and today.day == birthday.day:
                await message_channel.send(f'Happy Birthday {name}!')

async def setup(bot):
    await bot.add_cog(Birthday(bot))
