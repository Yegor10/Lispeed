from disnake.ext import commands
import disnake

class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Kicks member")
    @commands.has_permissions(kick_members=True) 
    async def kick(self,inter: disnake.ApplicationCommandInteraction, member:disnake.Member, reason: str):
        await member.kick(reason=reason)
        embed = disnake.Embed(
            title=f"User {member} has been kicked!",
            description=f"Moderathor: {inter.user}",
            color=disnake.Colour.purple(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Reason: ", value=reason, inline=True)
        await inter.response.send_message(embed=embed) 

def setup(bot):
    bot.add_cog(KickCommand(bot))