import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

load_dotenv()

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

bot.load_extension("cogs.guild_info")

bot.run(TOKEN)