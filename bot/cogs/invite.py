import disnake
from disnake.ext import commands
import json
import os

class InviteManagerCog(commands.Cog):
    INVITE_FILE = 'bot/invites.json'
    CHANNEL_FILE = 'bot/invite_channel.json'

    def __init__(self, bot):
        self.bot = bot
        self.invites_cache = {}

    def load_invites(self):
        try:
            if os.path.exists(self.INVITE_FILE):
                with open(self.INVITE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (IOError, json.JSONDecodeError):
            return {}

    def save_invites(self, invites):
        try:
            with open(self.INVITE_FILE, 'w', encoding='utf-8') as f:
                json.dump(invites, f, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def set_channel_invite(self, channel_id):
        try:
            with open(self.CHANNEL_FILE, 'w', encoding='utf-8') as f:
                json.dump({'channel_id': channel_id}, f, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def load_channel(self):
        try:
            if os.path.exists(self.CHANNEL_FILE):
                with open(self.CHANNEL_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('channel_id')
            return None
        except (IOError, json.JSONDecodeError):
            return None

    def get_invite_count(self, user_id: int, guild_id: int) -> int:
        invites = self.load_invites()
        guild_id_str = str(guild_id)
        user_id_str = str(user_id)
        return invites.get(guild_id_str, {}).get(user_id_str, 0)

    def add_invite(self, user_id: int, guild_id: int):
        invites = self.load_invites()
        guild_id_str = str(guild_id)
        user_id_str = str(user_id)
        if guild_id_str not in invites:
            invites[guild_id_str] = {}
        invites[guild_id_str][user_id_str] = invites[guild_id_str].get(user_id_str, 0) + 1
        self.save_invites(invites)

    @commands.slash_command(description="Set a channel to receive invite notifications")
    @commands.has_permissions(manage_channels=True)
    async def invites_setchannel(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        self.set_channel_invite(channel.id)
        embed = disnake.Embed(
            title=f"{channel.mention} was successfully set as invite channel!",
            description=f"Moderator: {inter.author.mention}",
            colour=disnake.Colour.purple()
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Disable the invite notification channel")
    @commands.has_permissions(manage_channels=True)
    async def invites_disablechannel(self, inter: disnake.ApplicationCommandInteraction):
        self.set_channel_invite(None)
        embed = disnake.Embed(
            title="Invite channel has been successfully disabled",
            description=f"Moderator: {inter.author.mention}",
            colour=disnake.Colour.purple()
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Check the number of invites for a user")
    async def invites_check(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        guild = inter.guild
        target_user = user if user else inter.author

        invite_count = self.get_invite_count(target_user.id, guild.id)
        embed = disnake.Embed(
            title=f"Invite Count for {target_user.name}",
            description=f"{target_user.mention} has **{invite_count}** invite{'s' if invite_count != 1 else ''} in this server.",
            colour=disnake.Colour.purple()
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try:
                self.invites_cache[guild.id] = await guild.invites()
            except disnake.errors.Forbidden:
                self.invites_cache[guild.id] = []

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        try:
            new_invites = await guild.invites()
        except disnake.errors.Forbidden:
            return

        old_invites = self.invites_cache.get(guild.id, [])
        used_invite = None

        for invite in new_invites:
            for old_invite in old_invites:
                if invite.code == old_invite.code and invite.uses > old_invite.uses:
                    used_invite = invite
                    break

        if used_invite:
            self.add_invite(used_invite.inviter.id, guild.id)
            embed = disnake.Embed(
                title="🎉 New Member Joined!",
                description=f"{member.mention} has joined using invite `{used_invite.code}`.",
                color=disnake.Color.purple()
            )
            embed.add_field(
                name="Inviter",
                value=f"{used_invite.inviter.mention}",
                inline=True
            )
            embed.add_field(
                name="Total Invites",
                value=str(self.get_invite_count(used_invite.inviter.id, guild.id)),
                inline=True
            )
            embed.set_footer(text="Invite Tracker Bot")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

            invite_channel_id = self.load_channel()
            if invite_channel_id:
                channel = guild.get_channel(invite_channel_id)
                if channel:
                    await channel.send(embed=embed)

        self.invites_cache[guild.id] = new_invites

def setup(bot):
    bot.add_cog(InviteManagerCog(bot))