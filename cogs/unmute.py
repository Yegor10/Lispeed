from disnake.ext import commands
import disnake

class Unmute(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.slash_command(description="Unmutes user")
    @commands.has_permissions(mute_members=True)
    async def unmute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        await member.timeout(until=None)
        embed = disnake.Embed(
            title=f"{member} has been unmuted!",
            description=f"Moderator: {inter.user}",
            colour=disnake.Colour.green(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(Unmute(bot))