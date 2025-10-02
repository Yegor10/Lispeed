import disnake
from disnake.ext import commands
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def add_message(self, guild_id: str, user_id: str):
    if os.path.exists(self.LEVELS_FILE):
        with open(self.LEVELS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[guild_id][user_id]["message"] + 1
        
def add_level(self, guild_id: str, user_id: str):
    if os.path.exists(self.LEVELS_FILE):
        with open(self.LEVELS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[guild_id][user_id]["level"] + 1
class LevelsCog(commands.Cog):
    LEVELS_FILE = 'levels.json'
    def __init__(self, bot):
        self.bot = bot
    
    