from disnake.ext import commands
import disnake

class Avatar(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.slash_command(description="Shows user's avatar")
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        avatar_url = user.display_avatar.url
        embed = disnake.Embed(
            title=f"{user}'s avatar:",
            colour=disnake.Colour.purple(),
        )
        embed.set_image(url=avatar_url)
        await inter.response.send_message(embed=embed) 

def setup(bot):
    bot.add_cog(Avatar(bot))