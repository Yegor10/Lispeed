from disnake.ext import commands
import disnake

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(description="get info about user")
    async def user_info(inter, user: disnake.Member):
        is_bot = "Roar"
        if user.bot == True:
            is_bot == "Yes"
        else:
            is_bot == "No"
        embed = disnake.Embed(
            title="All info about user",
            description=f"Shows all info about {user}",
            colour="0000FF",
        )
        embed.set_footer(text=f"All information about {user} was called by {inter.author}")
        if user.icon:
            embed.set_thumbnail(url=user.icon.url)
        embed.add_field(name="User name: ", value=inter.user, inline=True)
        embed.add_field(name="User ID: ", value=user.id, inline=True)
        embed.add_field(name="User's name in guild: ", value=inter.member.nick, inline=True)
        embed.add_field(name="Is user a bot: ", value=is_bot, inline=True)
        embed.add_field(name="User joined discord at: ", value=user.created_at, inline=True)
        embed.add_field(name=f"User joined {inter.guild.name} at: ", value=user.joined_at, inline=True)
        await inter.response.send_message(embed=embed) 

def setup(bot):
    bot.add_cog(UserInfo(bot))