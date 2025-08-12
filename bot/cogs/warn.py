import disnake
from disnake.ext import commands
import json
import os

class WarnCog(commands.Cog):
    WARN_FILE = 'bot/warns.json'

    def __init__(self, bot):
        self.bot = bot

    def load_warns(self):
        if os.path.exists(self.WARN_FILE):
            with open(self.WARN_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_warns(self, warns):
        with open(self.WARN_FILE, 'w', encoding='utf-8') as f:
            json.dump(warns, f, ensure_ascii=False, indent=4)

    def get_warns_count(self, user_id: int) -> int:
        warns = self.load_warns()
        return warns.get(str(user_id), 0)

    @commands.slash_command(description="Give a warning to a user")
    @commands.has_permissions(ban_members=True)
    async def warn(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        warns = self.load_warns()
        user_id = str(user.id)

        current_warns = self.get_warns_count(user.id) + 1
        warns[user_id] = current_warns
        self.save_warns(warns)

        warn_gave = disnake.Embed(
            title=f"User {user} got 1 warn and now has {current_warns}/3 warns",
            description=f"Moderator: {inter.author}",
            colour=disnake.Colour.dark_gold()
        )
        await inter.response.send_message(embed=warn_gave)

        if current_warns >= 3:
            try:
                warns_max = disnake.Embed(
                    title=f"User {user} reached 3 warns and got banned!",
                    description=f"Moderator: {inter.author}",
                    colour=disnake.Colour.brand_red()
                )
                await inter.followup.send(embed=warns_max)
                await user.ban(reason="Reached 3 warnings")
                warns[user_id] = 0
                self.save_warns(warns)
            except Exception as e:
                await inter.followup.send(f"Failed to ban user: {e}")

    @commands.slash_command(description="Shows user's warns")
    async def warns(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        warns_count = self.get_warns_count(user.id)
        embed = disnake.Embed(
            title=f"{user} has {warns_count}/3 warns now",
            description=f"Command was called by: {inter.author}",
            colour=disnake.Colour.dark_purple(),
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Remove 1 warn from a user")
    @commands.has_permissions(ban_members=True)
    async def unwarn(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        warns = self.load_warns()
        user_id = str(user.id)

        current_warns = self.get_warns_count(user.id)
        if current_warns > 0:
            warns[user_id] = current_warns - 1
            self.save_warns(warns)
            embed = disnake.Embed(
                title=f"{user} has been unwarned and now he has {warns[user_id]}/3 warns",
                description=f"Moderator: {inter.author}",
                colour=disnake.Colour.dark_magenta()
            )
        else:
            embed = disnake.Embed(
                title=f"{user} has no warns to remove",
                colour=disnake.Colour.dark_gray()
            )

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(WarnCog(bot))
