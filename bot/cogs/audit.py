from disnake.ext import commands
import disnake
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Audit(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.AUDIT_CHANNEL = "audit_channel.json"
        self.AUDIT_MODER = "audit_moder.json"
        self.AUDIT_USER = "audit_user.json"

    def save_audit_moder(self, audit_message):
        try:
            existing_logs = self.load_audit_moder()
            if not isinstance(existing_logs, list):
                existing_logs = []
            existing_logs.append(audit_message)
            with open(self.AUDIT_MODER, 'w', encoding="utf-8") as f:
                json.dump(existing_logs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving audit moder file: {e}")

    def load_audit_moder(self):
        try:
            if os.path.exists(self.AUDIT_MODER):
                with open(self.AUDIT_MODER, 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to parse {self.AUDIT_MODER}. Returning empty list.")
            return []
        except Exception as e:
            logger.error(f"Error loading audit moder file: {e}")
            return []

    def save_audit_user(self, audit_message):
        try:
            existing_logs = self.load_audit_user()
            if not isinstance(existing_logs, list):
                existing_logs = []
            existing_logs.append(audit_message)
            with open(self.AUDIT_USER, 'w', encoding="utf-8") as f:
                json.dump(existing_logs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving audit user file: {e}")

    def load_audit_user(self):
        try:
            if os.path.exists(self.AUDIT_USER):
                with open(self.AUDIT_USER, 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to parse {self.AUDIT_USER}. Returning empty list.")
            return []
        except Exception as e:
            logger.error(f"Error loading audit user file: {e}")
            return []

    def load_channel_audit(self):
        try:
            if os.path.exists(self.AUDIT_CHANNEL):
                with open(self.AUDIT_CHANNEL, 'r', encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            logger.error(f"Failed to parse {self.AUDIT_CHANNEL}. Returning empty dictionary.")
            return {}
        except Exception as e:
            logger.error(f"Error loading audit channel file: {e}")
            return {}

    def get_channel_for_guild(self, guild_id: int):
        channel = self.load_channel_audit()
        return channel.get(str(guild_id), None)

    def iterate_moder_logs(self):
        logs = self.load_audit_moder()
        result = []
        for log in logs:
            log_str = (
                f"Time: {log.get('timestamp', 'N/A')}, "
                f"Moderator: {log.get('user', 'N/A')} (ID: {log.get('user_id', 'N/A')}), "
                f"Command: {log.get('command', 'N/A')}, "
                f"Action: {log.get('action', 'N/A')}, "
                f"Channel ID: {log.get('channel_id', 'N/A')}, "
                f"Guild ID: {log.get('guild_id', 'N/A')}"
            )
            result.append(log_str)
        return result

    def iterate_user_logs(self, user_id: int):
        logs = self.load_audit_user()
        result = []
        for log in logs:
            if str(log.get('user_id')) == str(user_id):
                log_str = (
                    f"Time: {log.get('timestamp', 'N/A')}, "
                    f"User: {log.get('user', 'N/A')} (ID: {log.get('user_id', 'N/A')}), "
                    f"Command: {log.get('command', 'N/A')}, "
                    f"Options: {log.get('options', 'None')}, "
                    f"Channel ID: {log.get('channel_id', 'N/A')}, "
                    f"Guild ID: {log.get('guild_id', 'N/A')}"
                )
                result.append(log_str)
        return result

    @commands.slash_command(description="Set audit channel")
    @commands.has_permissions(manage_channels=True)
    async def audit_setchannel(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        logger.info(f"Setting audit channel by {inter.author} (ID: {inter.author.id}) in guild {inter.guild.id}")
        audit_channel = self.load_channel_audit()
        guild_id = str(inter.guild.id)
        role = inter.guild.default_role
        try:
            await channel.set_permissions(role, send_messages=False)
            audit_channel[guild_id] = channel.id
            with open(self.AUDIT_CHANNEL, 'w', encoding="utf-8") as f:
                json.dump(audit_channel, f, ensure_ascii=False, indent=4)
            self.save_audit_moder({
                "timestamp": inter.created_at.isoformat(),
                "user": str(inter.author),
                "user_id": inter.author.id,
                "action": "set_audit_channel",
                "channel_id": channel.id,
                "guild_id": inter.guild.id
            })
            embed = disnake.Embed(
                title=f"{channel.mention} was successfully set as audit channel!",
                description=f"Moderator: {inter.author.mention}",
                colour=disnake.Colour.green()
            )
            await inter.response.send_message(embed=embed)
            logger.info(f"Audit channel set to {channel.id} in guild {inter.guild.id}")
        except Exception as e:
            logger.error(f"Failed to set audit channel in guild {inter.guild.id}: {e}")
            embed = disnake.Embed(
                title="Error",
                description="Failed to set audit channel.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(description="Disable the audit notification channel")
    @commands.has_permissions(manage_channels=True)
    async def audit_disablechannel(self, inter: disnake.ApplicationCommandInteraction):
        logger.info(f"Disabling audit channel by {inter.author} (ID: {inter.author.id}) in guild {inter.guild.id}")
        guild_id = str(inter.guild.id)
        audit_channel = self.load_channel_audit()
        channel_id = audit_channel.get(guild_id)
        if not channel_id:
            logger.error(f"No audit channel set for guild {inter.guild.id}")
            embed = disnake.Embed(
                title="Error",
                description="No audit channel is set for this guild.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        try:
            channel = self.bot.get_channel(channel_id)
            if channel:
                role = inter.guild.default_role
                await channel.set_permissions(role, send_messages=False)
            audit_channel[guild_id] = None
            with open(self.AUDIT_CHANNEL, 'w', encoding="utf-8") as f:
                json.dump(audit_channel, f, ensure_ascii=False, indent=4)
            self.save_audit_moder({
                "timestamp": inter.created_at.isoformat(),
                "user": str(inter.author),
                "user_id": inter.author.id,
                "action": "disable_audit_channel",
                "channel_id": channel_id,
                "guild_id": inter.guild.id
            })
            embed = disnake.Embed(
                title="Audit channel has been successfully disabled",
                description=f"Moderator: {inter.author.mention}",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed)
            logger.info(f"Audit channel disabled in guild {inter.guild.id}")
        except Exception as e:
            logger.error(f"Failed to disable audit channel in guild {inter.guild.id}: {e}")
            embed = disnake.Embed(
                title="Error",
                description="Failed to disable audit channel.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(description="Shows moderator commands audit")
    @commands.has_permissions(manage_channels=True)
    async def audit_moderlogs(self, inter: disnake.ApplicationCommandInteraction, loggs_count: int):
        logger.info(f"show_moder_audit invoked by {inter.author} (ID: {inter.author.id}) in guild {inter.guild.id} with loggs_count={loggs_count}")
        if loggs_count <= 0:
            logger.error(f"Invalid loggs_count {loggs_count} provided by {inter.author.id} in guild {inter.guild.id}")
            embed = disnake.Embed(
                title="Error",
                description="Number of logs must be greater than 0.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        logs = self.iterate_moder_logs()
        if not logs:
            logger.error(f"No moderator logs found for guild {inter.guild.id}")
            embed = disnake.Embed(
                title="Moderator Audit",
                description="No moderator logs found.",
                colour=disnake.Colour.orange()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        logs_to_show = logs[:min(loggs_count, len(logs))]
        description = "\n".join(logs_to_show)
        if len(logs) > loggs_count:
            description += f"\n\n...and {len(logs) - loggs_count} more logs."
        embed = disnake.Embed(
            title="Moderator Commands Audit",
            description=description or "No data to display.",
            colour=disnake.Colour.blue(),
            timestamp=inter.created_at
        )
        embed.set_footer(text=f"Guild ID: {inter.guild.id}")
        try:
            await inter.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"Successfully displayed {len(logs_to_show)} moderator logs for {inter.author.id} in guild {inter.guild.id}")
        except Exception as e:
            logger.error(f"Failed to send moder audit embed for {inter.author.id} in guild {inter.guild.id}: {e}")
            embed = disnake.Embed(
                title="Error",
                description="Failed to send audit. Try again later.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(description="Shows user commands audit")
    @commands.has_permissions(manage_channels=True)
    async def audit_userlogs(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, loggs_count: int = 10):
        logger.info(f"show_user_audit invoked by {inter.author} (ID: {inter.author.id}) for user {user} (ID: {user.id}) in guild {inter.guild.id} with loggs_count={loggs_count}")
        if loggs_count <= 0:
            logger.error(f"Invalid loggs_count {loggs_count} provided by {inter.author.id} in guild {inter.guild.id}")
            embed = disnake.Embed(
                title="Error",
                description="Number of logs must be greater than 0.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        logs = self.iterate_user_logs(user.id)
        if not logs:
            logger.error(f"No user logs found for user {user.id} in guild {inter.guild.id}")
            embed = disnake.Embed(
                title="User Audit",
                description=f"No command logs found for {user.mention}.",
                colour=disnake.Colour.orange()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        logs_to_show = logs[:min(loggs_count, len(logs))]
        description = "\n".join(logs_to_show)
        if len(logs) > loggs_count:
            description += f"\n\n...and {len(logs) - loggs_count} more logs."
        embed = disnake.Embed(
            title=f"User Commands Audit for {user.display_name}",
            description=description or "No data to display.",
            colour=disnake.Colour.blue(),
            timestamp=inter.created_at
        )
        embed.set_footer(text=f"Guild ID: {inter.guild.id}")
        try:
            await inter.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"Successfully displayed {len(logs_to_show)} user logs for user {user.id} by {inter.author.id} in guild {inter.guild.id}")
        except Exception as e:
            logger.error(f"Failed to send user audit embed for user {user.id} by {inter.author.id} in guild {inter.guild.id}: {e}")
            embed = disnake.Embed(
                title="Error",
                description="Failed to send audit. Try again later.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.ApplicationCommandInteraction):
        command_name = inter.application_command.name
        options = str(inter.filled_options) if inter.filled_options else "None"
        logger.info(
            f"Command invoked in guild {inter.guild.id} by {inter.author} (ID: {inter.author.id}): "
            f"/{command_name} with options: {options}"
        )
        audit_message = {
            "timestamp": inter.created_at.isoformat(),
            "user": str(inter.author),
            "user_id": inter.author.id,
            "command": command_name,
            "options": options,
            "channel_id": inter.channel.id,
            "guild_id": inter.guild.id
        }
        is_moderator = inter.author.guild_permissions.manage_channels
        try:
            if is_moderator:
                existing_moder_logs = self.load_audit_moder()
                if not isinstance(existing_moder_logs, list):
                    existing_moder_logs = []
                existing_moder_logs.append(audit_message)
                with open(self.AUDIT_MODER, 'w', encoding="utf-8") as f:
                    json.dump(existing_moder_logs, f, ensure_ascii=False, indent=4)
            else:
                existing_user_logs = self.load_audit_user()
                if not isinstance(existing_user_logs, list):
                    existing_user_logs = []
                existing_user_logs.append(audit_message)
                with open(self.AUDIT_USER, 'w', encoding="utf-8") as f:
                    json.dump(existing_user_logs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving audit log: {e}")
        audit_channel_id = self.get_channel_for_guild(inter.guild.id)
        if not audit_channel_id:
            return
        audit_channel = self.bot.get_channel(audit_channel_id)
        if not audit_channel:
            logger.error(f"Audit channel {audit_channel_id} not found in guild {inter.guild.id}")
            return
        embed = disnake.Embed(
            title="Audit Log: Command Invoked",
            description=f"**Invoker:** {inter.author.mention} ({inter.author.id})\n"
                        f"**Command:** /{command_name}\n"
                        f"**Options/Arguments:** {options}\n"
                        f"**Channel:** {inter.channel.mention}",
            colour=disnake.Colour.blue(),
            timestamp=inter.created_at
        )
        embed.set_footer(text=f"Guild ID: {inter.guild.id}")
        try:
            await audit_channel.send(embed=embed)
            audit_message["action"] = "sent_audit_log"
            if is_moderator:
                existing_moder_logs = self.load_audit_moder()
                if not isinstance(existing_moder_logs, list):
                    existing_moder_logs = []
                existing_moder_logs.append(audit_message)
                with open(self.AUDIT_MODER, 'w', encoding="utf-8") as f:
                    json.dump(existing_moder_logs, f, ensure_ascii=False, indent=4)
            else:
                existing_user_logs = self.load_audit_user()
                if not isinstance(existing_user_logs, list):
                    existing_user_logs = []
                existing_user_logs.append(audit_message)
                with open(self.AUDIT_USER, 'w', encoding="utf-8") as f:
                    json.dump(existing_user_logs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Failed to send audit embed to channel {audit_channel_id}: {e}")

def setup(bot: commands.InteractionBot):
    bot.add_cog(Audit(bot))