# main.py

import os
from bot.bot import dp


def main():
    """
    Точка входа в проект.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")

    print("Запуск Telegram-бота...")
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()