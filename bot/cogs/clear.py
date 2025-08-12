from disnake.ext import commands
import disnake

class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Clears messages in channel for amount you write")
    async def clean(self, inter: disnake.ApplicationCommandInteraction, messages: int, ):
        await inter.channel.purge(limit=messages)
        embed = disnake.Embed(
            title=f"Channel was cleaned for {messages} messages",
            description=f"Moderator: {inter.author}",
            color=disnake.Colour.blue(),
        )
        await inter.response.send_message(embed=embed)
    
def setup(bot):
    bot.add_cog(ClearCommand(bot))