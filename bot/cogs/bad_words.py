from disnake.ext import commands
import disnake
import os
import json
from datetime import timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BadWords(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.BADWORDS_FILE = os.path.join(os.path.dirname(__file__), "badwords.json")

    def load_badwords(self):
        try:
            if os.path.exists(self.BADWORDS_FILE):
                with open(self.BADWORDS_FILE, 'r', encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            logger.error(f"Failed to parse {self.BADWORDS_FILE}. Returning empty dictionary.")
            return {}
        except Exception as e:
            logger.error(f"Error loading badwords file: {e}")
            return {}

    def save_badwords(self, badwords):
        try:
            with open(self.BADWORDS_FILE, 'w', encoding="utf-8") as f:
                json.dump(badwords, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving badwords file: {e}")

    def get_badwords_for_guild(self, guild_id: int):
        badwords = self.load_badwords()
        return badwords.get(str(guild_id), [])

    @commands.slash_command(description="Adds bad word that will be deleted if someone will type it.")
    @commands.has_permissions(moderate_members=True, manage_channels=True)
    async def badwords_add(self, inter: disnake.ApplicationCommandInteraction, bad_word: str):
        if not bad_word or len(bad_word) > 50:
            embed = disnake.Embed(
                title="Invalid Input",
                description="Bad word must be non-empty and less than 50 characters.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        badwords = self.load_badwords()
        guild_id = str(inter.guild.id)

        if guild_id not in badwords:
            badwords[guild_id] = []

        bad_word = bad_word.lower()
        if bad_word in badwords[guild_id]:
            embed = disnake.Embed(
                title="Duplicate Bad Word",
                description=f"'{bad_word}' is already in the bad word list.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        badwords[guild_id].append(bad_word)
        self.save_badwords(badwords)

        embed = disnake.Embed(
            title=f"Bad Word Added",
            description=f"'{bad_word}' was added to the bad word list.\nModerator: {inter.author.mention}",
            color=disnake.Color.dark_gray()
        )
        await inter.response.send_message(embed=embed)
    @commands.slash_command(description="Removes bad word from bad words list /badword_list to view badword")
    @commands.has_permissions(moderate_members=True, manage_channels=True)
    async def badwords_remove(self, inter: disnake.ApplicationCommandInteraction, bad_word: str):
        badwords = self.load_badwords()
        guild_id = str(inter.guild.id)
        try:
            badwords[guild_id].remove(bad_word)
            self.save_badwords(badwords)
            embed = disnake.Embed(
                title=f"Bad word {bad_word} was successfully removed from bad word list!",
                description=f"Moderator: {inter.author}",
                colour=disnake.Colour.green()
            )
            await inter.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="An error has occured",
                description=f"Error: {e}",
                colour=disnake.Colour.red()
            )
    @commands.slash_command(description="Shows bad word list")
    async def badwords_list(self, inter: disnake.ApplicationCommandInteraction):
        badwords = self.load_badwords()
        guild_id = str(inter.guild.id)
        embed = disnake.Embed(
            title=f"{inter.guild.name}'s badwords list",
            description=f"Command was called by: {inter.author}",
            colour=disnake.Colour.gold()
        )
        for badword in badwords[guild_id]:
            embed.add_field(name="", value=badword)
        
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Clears bad words list")
    async def badwords_clear(self, inter: disnake.ApplicationCommandInteraction ):
        badwords = self.load_badwords()
        guild_id = str(inter.guild.id)
        badwords[guild_id] = []
        self.save_badwords(badwords)
        embed = disnake.Embed(
            title=f"{inter.guild.name}'s badwords list",
            description=f"Command was called by: {inter.author}",
            colour=disnake.Colour.dark_magenta()
        )
        embed.add_field(name="Badwords list now: ", value=badwords[guild_id], inline=False)
        await inter.response.send_message(embed=embed)
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        logging.info(f"[BadWords] Received message: {message.content}. Is author bot: {message.author.bot}. In guid: {message.guild is not None}.")
        if message.author.bot or message.guild is None:
            return

        badwords = self.get_badwords_for_guild(message.guild.id)
        content = message.content.lower()

        logging.info(f"[BadWords] Fetched badwords for guild {message.guild.id}: {badwords}")
        
        for badword in badwords:
            if badword.lower() in content:
                logging.info(f"[BadWords] Found bad word in message: {badword}. Trying delete message.")

                try:
                    await message.delete()
                    logging.info(f"[BadWords] Message deleted.")
                except disnake.Forbidden:
                    await message.channel.send(
                        "I don't have permission to delete messages. Please contact an administrator.",
                        delete_after=5
                    )
                    break

                try:
                    await message.author.timeout(duration=timedelta(seconds=30), reason="Used a forbidden word")
                    embed = disnake.Embed(
                        title="Forbidden Word Detected",
                        description=f"{message.author.mention} has been muted for 30 seconds.",
                        color=disnake.Color.red()
                    )
                    await message.channel.send(embed=embed, delete_after=10)
                except disnake.Forbidden:
                    embed = disnake.Embed(
                        title="Forbidden Word Detected",
                        description="I don't have permission to mute users. The message was deleted.",
                        color=disnake.Color.red()
                    )
                    await message.channel.send(embed=embed, delete_after=10)
                break

def setup(bot):
    bot.add_cog(BadWords(bot))