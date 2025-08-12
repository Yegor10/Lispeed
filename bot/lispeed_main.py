
import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "sosal.env"))

TOKEN = os.getenv("TOKEN")
intents = disnake.Intents.default()
intents.members = True
bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

for filename in os.listdir("bot/cogs"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.run(TOKEN)