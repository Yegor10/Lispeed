from disnake.ext import commands
import disnake

class LockUnlock(commands.Cog):
    def __init__(self, bot=commands.bot):
        self.bot = bot
    
    @commands.slash_command(description="Locks channel and only admins can write in this channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        role = inter.guild.default_role
        await channel.set_permissions(role, send_messages=False)
        embed = disnake.Embed(
            title=f"Channel {channel} has been locked",
            description=f"Moderator: {inter.user}",
            colour=disnake.Colour.red()
        )
        await inter.response.send_message(embed=embed)

    
    @commands.slash_command(description="Unlocks locked channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        role = inter.guild.default_role
        perms = channel.permissions_for(role)
        if perms.send_messages:
            embed = disnake.Embed(
                title=f"Channel {channel} is already unlocked",
                description=f"Moderator: {inter.user}",
                colour=disnake.Colour.dark_purple()
            )
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"Chanell {channel} is unlocked for everyone now",
                description=f"Moderator: {inter.user}",
                colour=disnake.Colour.blue()
            )
            await channel.set_permissions(role, send_messages=True)
            await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(LockUnlock(bot))