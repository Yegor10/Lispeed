from disnake.ext import commands
import disnake
from datetime import timedelta

class MuteCommand(commands.Cog):
    def __init__(self, bot=commands.bot):
        self.bot = bot
    
    @commands.slash_command(description="Mutes member for entered minutes")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, time_type: str = commands.Param(choices=["minutes", "hours", "days"]), amount: int = commands.Param(gt=0), reason=str):
        if time_type == "minutes":
            duration = timedelta(minutes=amount)
        elif time_type == "hours":
            duration = timedelta(hours=amount)
        elif time_type == "days":
            duration = timedelta(days=amount)
        
        try:
            await member.timeout(until=disnake.utils.utcnow() + duration, reason=reason)
        except disnake.Forbidden:
            await inter.response.send_message("У меня нет прав для мута этого пользователя.", ephemeral=True)
            return
        except disnake.HTTPException:
            await inter.response.send_message("Не удалось замутить пользователя из-за ошибки API.", ephemeral=True)
            return
        embed = disnake.Embed(
            title=f"User {member} has been muted!",
            description=f"Moderator: {inter.user}",
            colour=disnake.Colour.red()
        )
        embed.add_field(name="Duration: ", value=f"{amount} {time_type}")
        embed.add_field(name="Reason: ", value=reason)
        embed.set_thumbnail(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(MuteCommand(bot))