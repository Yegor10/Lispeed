import disnake
from disnake.ext import commands
import json
import os

class LevelsCog(commands.Cog):
    LEVELS_FILE = 'levels.json'
    def __init__(self, bot):
        self.bot = bot

def load_user_level(self, guild_id: str, user_id: str):
    if os.path.exists(self.LEVELS_FILE):
        with open(self.LEVELS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            level = data[guild_id][user_id]["level"]
    return level

def load_user_messages(self, guild_id: str, user_id: str):
    if os.path.exists(self.LEVELS_FILE):
        with open(self.LEVELS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            messages = data[guild_id][user_id]["message"]
        return messages

def register_user(self, guild):
    