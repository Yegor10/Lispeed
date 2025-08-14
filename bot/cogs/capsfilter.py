from disnake.ext import commands
import disnake
import json
import os

class CapsFilter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.caps_file = "caps.json"
        self._load_caps_settings()

    def _load_caps_settings(self):
        if not os.path.exists(self.caps_file):
            with open(self.caps_file, "w") as f:
                json.dump({}, f)
        with open(self.caps_file, "r") as f:
            self.caps_settings = json.load(f)

    def _save_caps_settings(self):
        with open(self.caps_file, "w") as f:
            json.dump(self.caps_settings, f, indent=4)

    @commands.slash_command(description="Turn on or off caps lock filter")
    @commands.has_permissions(manage_channels=True)
    async def caps_filter(self, inter: disnake.ApplicationCommandInteraction, state: str = commands.Param(choices=["on", "off"])):
        guild_id = str(inter.guild.id)
        if state == "on":
            self.caps_settings[guild_id] = True
            self._save_caps_settings()
            embed = disnake.Embed(
                title="Caps filter is on",
                description=f"Now everyone who types in caps will be muted and their message deleted.\nModerator: {inter.author.mention}",
                colour=disnake.Colour.dark_purple()
            )
            await inter.response.send_message(embed=embed)
        elif state == "off":
            self.caps_settings[guild_id] = False
            self._save_caps_settings()
            embed = disnake.Embed(
                title="Caps filter is off",
                description=f"Now caps messages won't trigger mutes or deletions.\nModerator: {inter.author.mention}",
                colour=disnake.Colour.dark_orange()
            )
            await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.caps_settings or not self.caps_settings[guild_id]:
            return

        text = message.content
        if len(text) < 5:
            return

        total_letters = 0
        upper_letters = 0
        for char in text:
            if char.isalpha():
                total_letters += 1
                if char.isupper():
                    upper_letters += 1

        if total_letters > 0 and upper_letters / total_letters >= 0.7:
            try:
                await message.author.timeout(duration=10, reason="Caps lock")
                embed = disnake.Embed(
                    title="Caps detected!",
                    description=f"{message.author.mention} has been muted for 10 seconds.",
                    colour=disnake.Colour.dark_red()
                )
                await message.reply(embed=embed, delete_after=5)
                await message.delete()
            except disnake.Forbidden:
                await message.reply("❌ I don't have permission to mute this user!", delete_after=5)
            except Exception as e:
                await message.reply(f"❌ Error: {e}", delete_after=5)

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(CapsFilter(bot))