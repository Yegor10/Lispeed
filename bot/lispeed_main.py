
import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "sosal.env"))

TOKEN = os.getenv("TOKEN")
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    custom_emoji = bot.get_emoji()
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"за {guild_count} гильдиями", emoji=custom_emoji))
    print("Bot is ready")

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

for filename in os.listdir("bot/cogs"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.run(TOKEN)