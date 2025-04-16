# bot/bot.py

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import (
    handle_start, handle_balance, handle_add_user,
    handle_remove_user, handle_change_role, handle_list_users, handle_help
)
from config.config import TELEGRAM_BOT_TOKEN


# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


async def set_commands_for_user(user_id):
    """
    Устанавливает доступные команды для пользователя в зависимости от его роли.
    """
    from users.permissions import PermissionsManager
    permissions_manager = PermissionsManager()

    role = permissions_manager.get_role(user_id)

    if role == "admin":
        commands = [
            BotCommand(command="start", description="Начать работу"),
            BotCommand(command="balance", description="Просмотр баланса"),
            BotCommand(command="add_user", description="Добавить пользователя"),
            BotCommand(command="remove_user", description="Удалить пользователя"),
            BotCommand(command="change_role", description="Изменить роль пользователя"),
            BotCommand(command="list_users", description="Список пользователей"),
            BotCommand(command="help", description="Помощь")
        ]
    elif role == "user":
        commands = [
            BotCommand(command="start", description="Начать работу"),
            BotCommand(command="balance", description="Просмотр баланса"),
            BotCommand(command="help", description="Помощь")
        ]
    else:  # guest
        commands = [
            BotCommand(command="start", description="Начать работу"),
            BotCommand(command="help", description="Помощь")
        ]

    await bot.set_my_commands(commands, scope={"type": "chat", "chat_id": user_id})


# Регистрация обработчиков
dp.register_message_handler(handle_start, commands=["start"])
dp.register_message_handler(handle_balance, commands=["balance"])
dp.register_message_handler(handle_add_user, commands=["add_user"])
dp.register_message_handler(handle_remove_user, commands=["remove_user"])
dp.register_message_handler(handle_change_role, commands=["change_role"])
dp.register_message_handler(handle_list_users, commands=["list_users"])
dp.register_message_handler(handle_help, commands=["help"])