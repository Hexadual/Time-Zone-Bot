import discord
import datetime
from discord.ext import commands
from main import CONFIG

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logsChannel = self.bot.get_channel(int(CONFIG["LOGS_CHANNEL_ID"]))

    # Log when a member joins
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(
            color=0x00cc00,
            title="Member Joined",
            description=f"@{member.display_name} | {member.name}{member.discriminator}",
            timestamp=datetime.datetime.now(),
            url=member.default_avatar.url
        )
        embed.add_field(
            name="Member ID",
            value=str(member.id)
        )
        if self.logsChannel:
            await self.logsChannel.send(embed=embed)
        elif self.bot.defaultChannel:
            self.bot.defaultChannel.send(embed=embed)
    
    # Log when a member leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(
            color=0xcc0000,
            title="Member Left",
            description=f"@{member.display_name} | {member.name}{member.discriminator}",
            timestamp=datetime.datetime.now(),
            url=member.default_avatar.url
        )
        embed.add_field(
            name="Member ID",
            value=str(member.id)
        )
        if self.logsChannel:
            await self.logsChannel.send(embed=embed)
        elif self.bot.defaultChannel:
            self.bot.defaultChannel.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Logs(bot), guilds=[discord.Object(id=int(CONFIG["GUILD_ID"]))])
