# bot/logger.py

import logging
import os


def setup_logger():
    """
    Настраивает логирование.
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    log_file = os.path.join(logs_dir, "user_logs.log")

    os.makedirs(logs_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),  # Логи в файл
            logging.StreamHandler()  # Логи в консоль
        ]
    )
    return logging.getLogger(__name__)