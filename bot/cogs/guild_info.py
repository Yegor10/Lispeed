from disnake.ext import commands
import disnake

class GuildInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Get info about the server")
    async def guild_info(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild

        created_at = guild.created_at
        online_count = len([member for member in guild.members if member.status != disnake.Status.offline])

        embed = disnake.Embed(
            title="Server info",
            description=f"All info about {guild.name} server",
            color=disnake.Colour.yellow(),
        )
        embed.set_footer(text=f"Information was called by {inter.user.name}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Server name", value=guild.name, inline=True)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Total members", value=guild.member_count, inline=True)
        embed.add_field(name="Members online", value=online_count, inline=True)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Boost level", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boost count", value=guild.premium_subscription_count or 0, inline=True)
        embed.add_field(name="Verification level", value=guild.verification_level.name, inline=True)
        embed.add_field(name="Created at", value=created_at.strftime('%d.%m.%Y'), inline=True)

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(GuildInfo(bot))