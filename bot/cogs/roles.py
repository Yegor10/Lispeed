from disnake.ext import commands
import disnake
import os
import json
class RoleManager(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.AUTOROLE_FILE = "autorole.json"

    def load_autorole(self):
        if os.path.exists(self.AUTOROLE_FILE):
            with open(self.AUTOROLE_FILE, 'r', encoding="utf-8") as f:
                return json.load(f)
            
    def save_autorole(self, tf):
        with open(self.AUTOROLE_FILE, 'w', encoding="utf-8") as f:
            json.dump(tf, f, ensure_ascii=False, indent=4)

    @commands.slash_command(description="This command is used to add role to member. ADMINISTRATOR ONLY")
    @commands.has_permissions(administrator=True)
    async def role_add(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: disnake.Role):
        try:
            member.add_roles(role, reason="Roles edited by Lispeed", atomic=True)
            embed = disnake.Embed(
                title=f"{member}'s roles were succesfully edited!",
                description=f"Moderator: {inter.author}",
                colour=disnake.Colour.green()
            )
            embed.add_field(name="Changes: added this role to member ", value=role)
            await inter.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Failed to edit {member}'s roles",
                description=f"Moderator {inter.author}",
                colour=disnake.Colour.red()
            )
            embed.add_field(name="Error: ", value=e, inline=True)
            await inter.response.send_message(embed=embed)

    @commands.slash_command(description="This command is used to remove member rolles. ADMINISTRATOR ONLY")
    @commands.has_permissions(administrator=True)
    async def role_remove(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: disnake.Role):
        try:
            member.remove_roles(role, reason="Roles edited by Lispeed", atomic=True)
            embed = disnake.Embed(
                title=f"{member}'s roles were succsessfully edited!",
                description=f"Moderator: {inter.author}",
                colour=disnake.Colour.green()
            )
            embed.add_field(name=f"Changes: removed {role}", value=f"role from {member}")
            await inter.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Failed to edit {member}'s roles",
                description=f"Moderator {inter.author}",
                colour=disnake.Colour.red()
            )
            embed.add_field(name="Error: ", value=e, inline=True)
            await inter.response.send_message(embed=embed)
    
    @commands.slash_command(description="Shows member's roles")
    async def roles(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        roles = member.roles
        embed = disnake.Embed(
            title=f"Here are {member}s roles:",
            description=f"Command was called by: {inter.author}",
            colour=disnake.Colour.magenta()
        )
        for role in roles:
            embed.add_field(name=" ", value=role)
        await inter.response.send_message(embed=embed)
    
import disnake
from disnake.ext import commands
import json
import logging

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.onoff = self.load_autorole()

    def load_autorole(self):
        try:
            with open("autorole.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_autorole(self):
        with open("autorole.json", "w") as f:
            json.dump(self.onoff, f, indent=4)

    @commands.slash_command(description="Sets the role to be automatically assigned to new members")
    @commands.has_permissions(administrator=True)
    async def set_autorole(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        if not inter.guild.me.guild_permissions.manage_roles:
            embed = disnake.Embed(
                title="Error!",
                description="I don't have permission to manage roles!",
                colour=disnake.Colour.dark_red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            guild_id = str(inter.guild.id)
            self.onoff = self.load_autorole()
            self.onoff[guild_id] = [role.id, True]
            self.save_autorole()
            embed = disnake.Embed(
                title="Success!",
                description=f"Auto-role set to {role.mention} for new members.",
                colour=disnake.Colour.green()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logging.error(f"Error in set_autorole: {e}")
            embed = disnake.Embed(
                title="Error has occurred!",
                description=f"An error occurred: {e}",
                colour=disnake.Colour.dark_red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    @commands.slash_command(description="Clears the auto-role for new members")
    @commands.has_permissions(administrator=True)
    async def clear_autorole(self, inter: disnake.ApplicationCommandInteraction):
        try:
            guild_id = str(inter.guild.id)
            if guild_id in self.onoff:
                del self.onoff[guild_id]
                self.save_autorole()
                embed = disnake.Embed(
                    title="Success!",
                    description="Auto-role cleared for this server.",
                    colour=disnake.Colour.green()
                )
            else:
                embed = disnake.Embed(
                    title="Error!",
                    description="No auto-role was set for this server.",
                    colour=disnake.Colour.dark_red()
                )
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = disnake.Embed(
                title="Error!",
                description=f"Failed to clear auto-role: {e}",
                colour=disnake.Colour.dark_red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild_id = str(member.guild.id)
        if guild_id not in self.onoff:
            return

        role_id, enabled = self.onoff[guild_id]
        if not enabled:
            return

        role = member.guild.get_role(role_id)
        if role is None:
            logging.warning(f"Role {role_id} not found in guild {guild_id}")
            return

        try:
            await member.add_roles(role)
            logging.info(f"Added role {role.name} to {member.name} in guild {guild_id}")
        except disnake.Forbidden:
            logging.error(f"Missing permissions to add role {role_id} to {member.id} in guild {guild_id}")
        except Exception as e:
            logging.error(f"Error adding role to {member.id} in guild {guild_id}: {e}")

def setup(bot):
    bot.add_cog(AutoRole(bot))