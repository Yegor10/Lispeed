import disnake
from disnake.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="🆘 Show detailed help for all Lispeed commands")
    async def help_command(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="🆘 Lispeed - Full Command Reference",
            description="**Lispeed** — an advanced moderation bot with AI, levels, anti-spam, and entertainment features! 🌟\n\n**Command categories below. Use /help [category] for details.**\n\nHere's an overview of all available commands:",
            colour=disnake.Colour.from_rgb(88, 101, 242)  # Discord blue for style
        )
        
        # 🔨 Moderation (anti-spam, moderation, muting)
        moderation_value = (
            "🔨 **Anti-Spam & Filters:**\n"
            "• `/antispam [on/off]` - Enable/disable anti-spam (5+ messages in 5 sec) 🚫\n"
            "• `/caps_filter [on/off]` - Caps filter (70%+ uppercase) 📢\n"
            "• `/badwords_add <word>` - Add forbidden word ❌\n"
            "• `/badwords_remove <word>` - Remove word 📝\n"
            "• `/badwords_list` - List of forbidden words 📋\n"
            "• `/badwords_clear` - Clear list 🗑️\n\n"
            "🔨 **Moderation:**\n"
            "• `/ban <member> [reason]` - Ban user 👮\n"
            "• `/kick <member> [reason]` - Kick from server 🚪\n"
            "• `/mute <member> [time] [reason]` - Mute (min/hr/days) 🤐\n"
            "• `/unmute <member>` - Unmute 🔊\n"
            "• `/clear <amount>` - Delete messages 🧹\n"
            "• `/lock <channel>` - Lock channel 🔒\n"
            "• `/unlock <channel>` - Unlock channel 🔓\n"
            "• `/slowmode <seconds>` - Slow mode ⏱️\n"
            "• `/warn <member>` - Issue warning ⚠️\n"
            "• `/unwarn <member>` - Remove warning ✅\n"
            "• `/warns <member>` - Warning count 📊"
        )
        embed.add_field(name="🔨 **Moderation & Anti-Spam**", value=moderation_value, inline=False)
        
        # ⚙️ Utility (info, utilities)
        utility_value = (
            "⚙️ **Information:**\n"
            "• `/user_info <user>` - User info 👤\n"
            "• `/guild_info` - Server info 🏰\n"
            "• `/avatar <user>` - User avatar 🖼️\n"
            "• `/roles <member>` - Member roles 🎭\n"
            "• `/nick <member> <new_nick>` - Change nickname ✏️\n\n"
            "⚙️ **Management:**\n"
            "• `/invites_setchannel <channel>` - Channel for invite notifications 📢\n"
            "• `/invites_disablechannel` - Disable channel 🛑\n"
            "• `/invites_check [user]` - User's invite count 🔗"
        )
        embed.add_field(name="⚙️ **Utilities & Info**", value=utility_value, inline=False)
        
        # 🎉 Fun (entertainment)
        fun_value = (
            "🎉 **Actions & Reactions:**\n"
            "• `/hug <member>` - Hug 🤗\n"
            "• `/kiss <member>` - Kiss 💋\n"
            "• `/punch <member>` - Punch 👊\n"
            "• `/dance <member>` - Dance 💃🕺\n"
            "• `/highfive <member>` - High-five ✋\n"
            "• `/cry` - Cry 😢\n"
            "• `/laugh` - Laugh 😂\n"
            "• `/sleep` - Sleep 😴\n"
            "• `/eat` - Eat 🍔\n"
            "• `/run <member>` - Run away 🏃\n"
            "• `/fly` - Fly 🦸\n"
            "• `/magic <member>` - Magic ✨\n"
            "• `/sing` - Sing 🎤\n"
            "• `/wave <member>` - Wave 👋\n"
            "• `/thumbsup` - Thumbs up 👍\n\n"
            "🎉 **Animals:**\n"
            "• `/meow [member]` - Cat 🐱\n"
            "• `/woof` - Dog 🐶\n"
            "• `/pat <member>` - Pat 🐾"
        )
        embed.add_field(name="🎉 **Entertainment**", value=fun_value, inline=False)
        
        # 📈 Levels
        levels_value = (
            "📈 **Leveling System:**\n"
            "• `/level_info` - Level requirements table 📊\n"
            "• `/user_level <user>` - User's level 🆙\n"
            "• Automatic progress for messages! (Thresholds: 30, 60...4800) 💬\n"
            "(Max level: 16!)"
        )
        embed.add_field(name="📈 **Levels**", value=levels_value, inline=False)
        
        # 👑 Roles
        roles_value = (
            "👑 **Roles & Auto-Roles:**\n"
            "• `/role_add <member> <role>` - Add role ➕\n"
            "• `/role_remove <member> <role>` - Remove role ➖\n"
            "• `/set_autorole <role>` - Auto-role for new members 🤖\n"
            "• `/clear_autorole` - Clear auto-role 🗑️"
        )
        embed.add_field(name="👑 **Roles**", value=roles_value, inline=False)
        
        # 📝 Audit & Logs
        audit_value = (
            "📝 **Audit & Logs:**\n"
            "• `/audit_setchannel <channel>` - Channel for logs 📢\n"
            "• `/audit_disablechannel` - Disable channel 🛑\n"
            "• `/audit_moderlogs <count>` - Moderator logs 📋\n"
            "• `/audit_userlogs <user> [count]` - User logs 👤"
        )
        embed.add_field(name="📝 **Audit & Logs**", value=audit_value, inline=False)
        
        # ℹ️ General
        embed.add_field(
            name="ℹ️ **Notes**",
            value="• All commands are slash (/).\n• Moderation requires permissions (manage_channels, ban_members, etc.).\n• Bot on Disnake — stable and fast! 🚀\n• Support: GitHub repo below.",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Developer: Yegor10 | Version: 1.0 | Date: 02.10.2025", 
                         icon_url="https://avatars.githubusercontent.com/u/Yegor10")  # Replace with real avatar
        embed.timestamp = disnake.utils.utcnow()
        
        # View with buttons
        view = disnake.ui.View(timeout=180)
        view.add_item(disnake.ui.Button(label="GitHub Repo", url="https://github.com/Yegor10/Lispeed", style=disnake.ButtonStyle.link, emoji="📂"))
        view.add_item(disnake.ui.Button(label="Invite Bot", url="https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands", style=disnake.ButtonStyle.link, emoji="🤖"))  # Replace YOUR_BOT_ID
        
        await inter.response.send_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(HelpCog(bot))