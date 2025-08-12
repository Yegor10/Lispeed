from disnake.ext import commands
import disnake
from datetime import timedelta

class NickChanger(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.slash_command(description="Chabges member's nickname")
    @commands.has_permissions(change_nickname=True)
    async def nick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, new_nickname: str):
        previous_name = member.display_name
        await member.edit(nick=new_nickname)
        embed = disnake.Embed(
            title=f"{previous_name}'s nick was succesfully changed to {new_nickname}",
            description=f"Moderator: {inter.user}",
            colour=disnake.Colour.dark_blue()
        )
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(NickChanger(bot))