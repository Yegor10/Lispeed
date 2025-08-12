from disnake.ext import commands
import disnake

class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Bans member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member:disnake.Member, reason: str):
        await member.ban(reason=reason)
        embed = disnake.Embed(
            title=f"User {member} has been banned!",
            description=f"Moderathor: {inter.user}",
            color=disnake.Colour.red(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Reason: ", value=reason, inline=True)
        await inter.response.send_message(embed=embed) 

def setup(bot):
    bot.add_cog(BanCommand(bot))