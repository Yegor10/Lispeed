import disnake
from disnake.ext import commands

class LispeedHelp(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.slash_command(description="help command with all commands")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="📜 Lispeed Help 📜", color=disnake.Color.blue())
        embed.add_field(name="/add_badword", value="Add bad word 🔥", inline=True)
        embed.add_field(name="/avatar", value="Show user's avatar 🌟", inline=True)
        embed.add_field(name="/badword_list", value="View bad word list 📋", inline=True)
        embed.add_field(name="/ban", value="Ban member 🚫", inline=True)
        embed.add_field(name="/clean", value="Clear messages 🧹", inline=True)
        embed.add_field(name="/info", value="Server info ℹ️", inline=True)
        embed.add_field(name="/kick", value="Kick member 👢", inline=True)
        embed.add_field(name="/lock", value="Lock channel 🔒", inline=True)
        embed.add_field(name="/mute", value="Mute member 🔇", inline=True)
        embed.add_field(name="/nick", value="Change member's nickname 🖌️", inline=True)
        embed.add_field(name="/ping", value="Check bot latency ⏱️", inline=True)
        embed.add_field(name="/remove_badword", value="Remove bad word ❌", inline=True)
        embed.add_field(name="/slowmode", value="Enable slow mode ⏳", inline=True)
        embed.add_field(name="/unlock", value="Unlock channel 🔓", inline=True)
        embed.add_field(name="/unmute", value="Unmute member 🔊", inline=True)
        embed.add_field(name="/unwarn", value="Remove warning ⚠️", inline=True)
        embed.add_field(name="/user_info", value="Get user info 👤", inline=True)
        embed.add_field(name="/warn", value="Warn a user ⚠️", inline=True)
        embed.add_field(name="/warns", value="Show user's warns 📊", inline=True)
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(LispeedHelp(bot))