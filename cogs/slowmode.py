from disnake.ext import commands
import disnake

class SlowMode(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.slash_command(description="Makes slow mode in selected channel. Enter time in secounds")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, inter: disnake.ApplicationCommandInteraction, seconds: int):
        await inter.channel.edit(slowmode_delay=seconds)
        await inter.response.send_message(f"Slowmode is {seconds} now")

def setup(bot):
    bot.add_cog(SlowMode(bot))