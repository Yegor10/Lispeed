import disnake
from disnake.ext import commands
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LevelsCog(commands.Cog):
    LEVELS_FILE = 'levels.json'

    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(self.LEVELS_FILE):
            with open(self.LEVELS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def _load_data(self):
        if os.path.exists(self.LEVELS_FILE):
            with open(self.LEVELS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_data(self, data):
        with open(self.LEVELS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_user_level(self, guild_id: str, user_id: str) -> int:
        data = self._load_data()
        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = {"level": 0, "message": 0}
            self._save_data(data)
        return data[guild_id][user_id]["level"]

    def load_user_messages(self, guild_id: str, user_id: str) -> int:
        data = self._load_data()
        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = {"level": 0, "message": 0}
            self._save_data(data)
        return data[guild_id][user_id]["message"]

    def add_message(self, guild_id: str, user_id: str):
        data = self._load_data()
        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = {"level": 0, "message": 0}
        data[guild_id][user_id]["message"] += 1
        self._save_data(data)

    def add_level(self, guild_id: str, user_id: str):
        data = self._load_data()
        if guild_id in data and user_id in data[guild_id]:
            data[guild_id][user_id]["level"] += 1
            self._save_data(data)
    @commands.slash_command(name="level_info", description="Shows the level requirements")
    async def level_info(self, inter: disnake.ApplicationCommandInteraction):
        lvls = [30, 60, 120, 240, 360, 480, 600, 800, 1200, 1400, 1600, 2400, 3000, 3400, 3600, 4800]
        
        table = "| Level | Messages Required |\n|-------|-------------------|\n"
        for i, msgs in enumerate(lvls, start=1):
            table += f"| {i}     | {msgs:,}             |\n"
        
        embed = disnake.Embed(
            title="📈 Level Progression Guide",
            description=f"**Reach these message milestones to level up!**\n\n{table}",
            colour=disnake.Colour.gold()
        )
        embed.set_footer(text="Keep chatting to climb the ranks! 💬")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1234567890.png")
        
        await inter.response.send_message(embed=embed)
    @commands.slash_command(name="user_level", description="Shows user's level")
    async def user_level(self, user_id: disnake.Member, guild_id: disnake.Guild, inter: disnake.ApplicationCommandInteraction):
        lvl = self.load_user_level(f"{guild_id}", f"{user_id}")
        embed = disnake.Embed(
            title=f"{user_id}'s level is {lvl}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.brand_green()
        )

        await inter.response.send_message(embed=embed)
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        self.add_message(guild_id, user_id)
        user_messages = self.load_user_messages(guild_id, user_id)

        lvls = [30, 60, 120, 240, 360, 480, 600, 800, 1200, 1400, 1600, 2400, 3000, 3400, 3600, 4800]

        for i in lvls:
            if user_messages == i:
                self.add_level(guild_id, user_id)
                user_lvl = self.load_user_level(guild_id, user_id)
                embed = disnake.Embed(
                    title="Level up!",
                    description=f"User {message.author.mention} has leveled up and now he is level {user_lvl}!",
                    colour=disnake.Colour.purple()
                )
                await message.channel.send(embed=embed)
            elif user_lvl == 16:
                embed = disnake.Embed(
                    title="Level up!",
                    description=f"User {message.author.mention} has leveled up and now he is 16 (MAX LVL)!!!!!",
                    colour=disnake.Colour.purple()
                )
                await message.channel.send(embed=embed)
                break

def setup(bot):
    bot.add_cog(LevelsCog(bot))