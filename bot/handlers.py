# bot/handlers.py

from aiogram import types
from api.api_client import TochkaAPIClient
from core.account_manager import AccountManager
from bot.logger import setup_logger
from users.permissions import PermissionsManager


logger = setup_logger()
permissions_manager = PermissionsManager()

# Инициализация компонентов
api_client = TochkaAPIClient()
account_manager = AccountManager()


async def handle_start(message: types.Message):
    """
    Обрабатывает команду /start.
    """
    user_id = message.from_user.id
    role = permissions_manager.get_role(user_id)  # Получаем роль пользователя

    if not permissions_manager.has_permission(user_id, "start"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    username = message.from_user.username or "Нет username"
    first_name = message.from_user.first_name or "Нет имени"
    last_name = message.from_user.last_name or "Нет фамилии"
    language_code = message.from_user.language_code or "Нет языка"

    log_message = (
        f"Пользователь подключился: ID={user_id}, Username=@{username}, "
        f"Имя={first_name}, Фамилия={last_name}, Язык={language_code}"
    )

    logger.info(log_message)

    # Формируем приветственное сообщение в зависимости от роли
    if role == "admin":
        welcome_message = (
            "Привет, админ!\n\n"
            "Доступные команды:\n"
            "- /balance - Просмотр баланса\n"
            "- /add_user - Добавить пользователя\n"
            "- /remove_user - Удалить пользователя\n"
            "- /change_role - Изменить роль пользователя\n"
            "- /list_users - Список пользователей"
        )
    elif role == "user":
        welcome_message = (
            "Привет, пользователь!\n\n"
            "Доступные команды:\n"
            "- /balance - Просмотр баланса"
        )
    else:  # guest
        welcome_message = (
            "Привет, гость!\n\n"
            "Доступные команды:\n"
            "- /help - Помощь"
        )

    await message.reply(welcome_message)

    # Устанавливаем доступные команды для пользователя
    from bot.bot import set_commands_for_user
    await set_commands_for_user(user_id)


async def handle_help(message: types.Message):
    """
    Обрабатывает команду /help.
    """
    user_id = message.from_user.id
    role = permissions_manager.get_role(user_id)  # Получаем роль пользователя

    if not permissions_manager.has_permission(user_id, "help"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    # Формируем сообщение помощи в зависимости от роли
    if role == "admin":
        help_message = (
            "Справка для администратора:\n\n"
            "- /balance - Просмотр баланса\n"
            "- /add_user <user_id> <role> - Добавить нового пользователя\n"
            "- /remove_user <user_id> - Удалить пользователя\n"
            "- /change_role <user_id> <new_role> - Изменить роль пользователя\n"
            "- /list_users - Вывести список всех пользователей"
        )
    elif role == "user":
        help_message = (
            "Справка для пользователя:\n\n"
            "- /balance - Просмотр баланса"
        )
    else:  # guest
        help_message = (
            "Справка для гостя:\n\n"
            "- /start - Начать работу с ботом\n"
            "- /help - Получить помощь"
        )

    await message.reply(help_message)


async def handle_balance(message: types.Message):
    """
    Обрабатывает команду /balance.
    """
    user_id = message.from_user.id
    if not permissions_manager.has_permission(user_id, "balance"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Получаю данные о счетах...")
    raw_data = await api_client.get_balances()

    if not raw_data:
        await message.answer("Не удалось получить данные о балансах.")
        return

    formatted_data = account_manager.process_balances(raw_data)
    await message.answer(formatted_data)


async def handle_add_user(message: types.Message):
    """
    Обрабатывает команду /add_user.
    """
    user_id = message.from_user.id
    if not permissions_manager.has_permission(user_id, "add_user"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.reply("Использование: /add_user <user_id> <role>")
            return

        new_user_id, role = args
        permissions_manager.add_user(new_user_id, role)
        logger.info(f"Администратор (ID={user_id}) добавил пользователя (ID={new_user_id}) с ролью '{role}'.")
        await message.reply(f"Пользователь (ID={new_user_id}) успешно добавлен с ролью '{role}'.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await message.reply("Произошла ошибка при добавлении пользователя.")


async def handle_remove_user(message: types.Message):
    """
    Обрабатывает команду /remove_user.
    """
    user_id = message.from_user.id
    if not permissions_manager.has_permission(user_id, "remove_user"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 1:
            await message.reply("Использование: /remove_user <user_id>")
            return

        user_to_remove = args[0]
        permissions_manager.remove_user(user_to_remove)
        logger.info(f"Администратор (ID={user_id}) удалил пользователя (ID={user_to_remove}).")
        await message.reply(f"Пользователь (ID={user_to_remove}) успешно удален.")
    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя: {e}")
        await message.reply("Произошла ошибка при удалении пользователя.")


async def handle_change_role(message: types.Message):
    """
    Обрабатывает команду /change_role.
    """
    user_id = message.from_user.id
    if not permissions_manager.has_permission(user_id, "change_role"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.reply("Использование: /change_role <user_id> <new_role>")
            return

        user_to_update, new_role = args
        permissions_manager.change_role(user_to_update, new_role)
        logger.info(f"Администратор (ID={user_id}) изменил роль пользователя (ID={user_to_update}) на '{new_role}'.")
        await message.reply(f"Роль пользователя (ID={user_to_update}) успешно изменена на '{new_role}'.")
    except Exception as e:
        logger.error(f"Ошибка при изменении роли пользователя: {e}")
        await message.reply("Произошла ошибка при изменении роли пользователя.")


async def handle_list_users(message: types.Message):
    """
    Обрабатывает команду /list_users.
    """
    user_id = message.from_user.id
    if not permissions_manager.has_permission(user_id, "list_users"):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    # Получаем список пользователей и их ролей
    users = permissions_manager.users
    if not users:
        await message.reply("Список пользователей пуст.")
        return

    # Формируем ответ
    response = "Список пользователей:\n"
    for user_id, role in users.items():
        response += f"- ID: {user_id}, Роль: {role}\n"

    await message.reply(response)