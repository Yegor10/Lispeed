import disnake
from disnake.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="🆘 Показать подробную помощь по всем командам Lispeed")
    async def help_command(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="🆘 Lispeed - Полная справка по командам",
            description="**Lispeed** — продвинутый модераторский бот с ИИ, уровнями, анти-спамом и развлечениями! 🌟\n\n**Категории команд ниже. Используйте /help [category] для деталей.**\n\nВот обзор всех доступных команд:",
            colour=disnake.Colour.from_rgb(88, 101, 242)  # Discord синий для стиля
        )
        
        # 🔨 Moderation (анти-спам, модерация, мутинг)
        moderation_value = (
            "🔨 **Анти-спам & Фильтры:**\n"
            "• `/antispam [on/off]` - Вкл/выкл анти-спам (5+ сообщений за 5 сек) 🚫\n"
            "• `/caps_filter [on/off]` - Фильтр капса (70%+ заглавных) 📢\n"
            "• `/badwords_add <word>` - Добавить запрещённое слово ❌\n"
            "• `/badwords_remove <word>` - Удалить слово 📝\n"
            "• `/badwords_list` - Список запрещённых слов 📋\n"
            "• `/badwords_clear` - Очистить список 🗑️\n\n"
            "🔨 **Модерация:**\n"
            "• `/ban <member> [reason]` - Бан пользователя 👮\n"
            "• `/kick <member> [reason]` - Кик с сервера 🚪\n"
            "• `/mute <member> [time] [reason]` - Мут (мин/час/дни) 🤐\n"
            "• `/unmute <member>` - Снять мут 🔊\n"
            "• `/clear <amount>` - Удалить сообщения 🧹\n"
            "• `/lock <channel>` - Заблокировать канал 🔒\n"
            "• `/unlock <channel>` - Разблокировать канал 🔓\n"
            "• `/slowmode <seconds>` - Замедленный режим ⏱️\n"
            "• `/warn <member>` - Выдать предупреждение ⚠️\n"
            "• `/unwarn <member>` - Снять предупреждение ✅\n"
            "• `/warns <member>` - Кол-во предупреждений 📊"
        )
        embed.add_field(name="🔨 **Модерация & Анти-спам**", value=moderation_value, inline=False)
        
        # ⚙️ Utility (инфо, утилиты)
        utility_value = (
            "⚙️ **Информация:**\n"
            "• `/user_info <user>` - Инфо о пользователе 👤\n"
            "• `/guild_info` - Инфо о сервере 🏰\n"
            "• `/avatar <user>` - Аватар пользователя 🖼️\n"
            "• `/roles <member>` - Роли участника 🎭\n"
            "• `/nick <member> <new_nick>` - Изменить никнейм ✏️\n\n"
            "⚙️ **Управление:**\n"
            "• `/invites_setchannel <channel>` - Канал для уведомлений об инвайтах 📢\n"
            "• `/invites_disablechannel` - Отключить канал 🛑\n"
            "• `/invites_check [user]` - Кол-во инвайтов пользователя 🔗"
        )
        embed.add_field(name="⚙️ **Утилиты & Инфо**", value=utility_value, inline=False)
        
        # 🎉 Fun (развлечения)
        fun_value = (
            "🎉 **Действия & Реакции:**\n"
            "• `/hug <member>` - Обнимашки 🤗\n"
            "• `/kiss <member>` - Поцелуй 💋\n"
            "• `/punch <member>` - Шлепок 👊\n"
            "• `/dance <member>` - Танец 💃🕺\n"
            "• `/highfive <member>` - Хай-фай ✋\n"
            "• `/cry` - Плач 😢\n"
            "• `/laugh` - Смех 😂\n"
            "• `/sleep` - Сон 😴\n"
            "• `/eat` - Еда 🍔\n"
            "• `/run <member>` - Бегство 🏃\n"
            "• `/fly` - Полёт 🦸\n"
            "• `/magic <member>` - Магия ✨\n"
            "• `/sing` - Пение 🎤\n"
            "• `/wave <member>` - Мах рукой 👋\n"
            "• `/thumbsup` - Лайк 👍\n\n"
            "🎉 **Животные:**\n"
            "• `/meow [member]` - Котик 🐱\n"
            "• `/woof` - Собачка 🐶\n"
            "• `/pat <member>` - Погладить 🐾"
        )
        embed.add_field(name="🎉 **Развлечения**", value=fun_value, inline=False)
        
        # 📈 Levels
        levels_value = (
            "📈 **Система уровней:**\n"
            "• `/level_info` - Таблица требований к уровням 📊\n"
            "• `/user_level <user>` - Уровень пользователя 🆙\n"
            "• Автоматический прогресс за сообщения! (Пороги: 30, 60...4800) 💬\n"
            "(Макс. уровень: 16!)"
        )
        embed.add_field(name="📈 **Уровни**", value=levels_value, inline=False)
        
        # 👑 Roles
        roles_value = (
            "👑 **Роли & Авто-роли:**\n"
            "• `/role_add <member> <role>` - Добавить роль ➕\n"
            "• `/role_remove <member> <role>` - Удалить роль ➖\n"
            "• `/set_autorole <role>` - Авто-роль для новичков 🤖\n"
            "• `/clear_autorole` - Очистить авто-роль 🗑️"
        )
        embed.add_field(name="👑 **Роли**", value=roles_value, inline=False)
        
        # 📝 Audit & Logs
        audit_value = (
            "📝 **Аудит & Логи:**\n"
            "• `/audit_setchannel <channel>` - Канал для логов 📢\n"
            "• `/audit_disablechannel` - Отключить канал 🛑\n"
            "• `/audit_moderlogs <count>` - Логи модераторов 📋\n"
            "• `/audit_userlogs <user> [count]` - Логи пользователя 👤"
        )
        embed.add_field(name="📝 **Аудит & Логи**", value=audit_value, inline=False)
        
        # ℹ️ Общие
        embed.add_field(
            name="ℹ️ **Заметки**",
            value="• Все команды — slash (/).\n• Для модерации нужны права (manage_channels, ban_members и т.д.).\n• Бот на Disnake — стабильный и быстрый! 🚀\n• Поддержка: GitHub репо ниже.",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Разработчик: Yegor10 | Версия: 1.0 | Дата: 02.10.2025", 
                         icon_url="https://avatars.githubusercontent.com/u/Yegor10")  # Замени на реальный аватар
        embed.timestamp = disnake.utils.utcnow()
        
        # View с кнопками
        view = disnake.ui.View(timeout=180)
        view.add_item(disnake.ui.Button(label="GitHub Репо", url="https://github.com/Yegor10/Lispeed", style=disnake.ButtonStyle.link, emoji="📂"))
        view.add_item(disnake.ui.Button(label="Пригласить Бота", url="https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands", style=disnake.ButtonStyle.link, emoji="🤖"))  # Замени YOUR_BOT_ID
        
        await inter.response.send_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(HelpCog(bot))