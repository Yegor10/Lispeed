from disnake.ext import commands
import disnake
import json
import os
from collections import defaultdict
import time

class AntiSpam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.antispam_file = "antispam.json"
        self.message_tracker = defaultdict(list)
        self._load_antispam_settings()

    def _load_antispam_settings(self):
        if not os.path.exists(self.antispam_file):
            with open(self.antispam_file, "w") as f:
                json.dump({}, f)
        with open(self.antispam_file, "r") as f:
            self.antispam_settings = json.load(f)

    def _save_antispam_settings(self):
        with open(self.antispam_file, "w") as f:
            json.dump(self.antispam_settings, f, indent=4)

    @commands.slash_command(description="Turn on or off anti-spam filter")
    @commands.has_permissions(manage_channels=True)
    async def antispam(self, inter: disnake.ApplicationCommandInteraction, state: str = commands.Param(choices=["on", "off"])):
        guild_id = str(inter.guild.id)
        if state == "on":
            self.antispam_settings[guild_id] = True
            self._save_antispam_settings()
            embed = disnake.Embed(
                title="Anti-spam filter is on",
                description=f"Now users sending 5+ messages in 5 seconds will be muted and their messages deleted.\nModerator: {inter.author.mention}",
                colour=disnake.Colour.dark_purple()
            )
            await inter.response.send_message(embed=embed)
        elif state == "off":
            self.antispam_settings[guild_id] = False
            self._save_antispam_settings()
            embed = disnake.Embed(
                title="Anti-spam filter is off",
                description=f"Now spam messages won't trigger mutes or deletions.\nModerator: {inter.author.mention}",
                colour=disnake.Colour.dark_orange()
            )
            await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if not message.guild or message.author.bot:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.antispam_settings or not self.antispam_settings[guild_id]:
            return

        user_id = message.author.id
        current_time = time.time()
        self.message_tracker[user_id].append(current_time)

        self.message_tracker[user_id] = [t for t in self.message_tracker[user_id] if current_time - t < 5]
        if len(self.message_tracker[user_id]) >= 5:
            try:
                await message.author.timeout(duration=10, reason="Spamming")
                embed = disnake.Embed(
                    title="Spam detected!",
                    description=f"{message.author.mention} has been muted for 10 seconds for spamming.",
                    colour=disnake.Colour.dark_red()
                )
                await message.reply(embed=embed, delete_after=5)
                async for msg in message.channel.history(limit=10):
                    if msg.author.id == user_id and current_time - msg.created_at.timestamp() < 5:
                        try:
                            await msg.delete()
                        except:
                            pass
                self.message_tracker[user_id].clear()
            except disnake.Forbidden:
                await message.reply("❌ I don't have permission to mute this user!", delete_after=5)
            except Exception as e:
                await message.reply(f"❌ Error: {e}", delete_after=5)

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(AntiSpam(bot))