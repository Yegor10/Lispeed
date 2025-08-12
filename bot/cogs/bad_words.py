from disnake.ext import commands
import disnake
import os
import json
from datetime import timedelta
class BadWords(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.BADWORDS_FILE = "bot/cogs/badwords.json"
    def load_badwords(self):
        if os.path.exists(self.BADWORDS_FILE):
            with open(self.BADWORDS_FILE, 'r', encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_badwords(self, badwords):
        with open(self.BADWORDS_FILE, 'w', encoding="utf-8") as f:
            json.dump(badwords, f, ensure_ascii=False, indent=4)

    def get_badwords_for_guild(self, guild_id: int):
        badwords = self.load_badwords()
        return badwords.get(str(guild_id), [])

    @commands.slash_command(description="Adds bad word that will be deleted if someone will type it.")
    @commands.has_permissions(administrator=True)
    async def add_badword(self, inter: disnake.ApplicationCommandInteraction, bad_word: str):
        badwords = self.load_badwords()
        guild_id = str(inter.guild.id)

        if guild_id not in badwords:
            badwords[guild_id] = []

        badwords[guild_id].append(bad_word)
        self.save_badwords(badwords)

        embed = disnake.Embed(
            title=f"New badword '{bad_word}' was added to badword list",
            description=f"Moderator: {inter.author}",
            colour=disnake.Colour.dark_gray()
        )
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or message.guild is None:
            return

        badwords = self.get_badwords_for_guild(message.guild.id)
        content = message.content.lower()

        for badword in badwords:
            if badword.lower() in content:
                try:
                    await message.delete()
                except disnake.Forbidden:
                    pass

                try:
                    await message.author.timeout(duration=timedelta(seconds=30), reason="Used a forbidden word")
                except disnake.Forbidden:
                    pass

                embed = disnake.Embed(
                    title="Forbidden word detected!",
                    description=f"{message.author.mention} has been muted for 30 seconds.",
                    colour=disnake.Colour.red()
                )
                await message.channel.send(embed=embed, delete_after=10)
                break

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(BadWords(bot))