# users/permissions.py

import json
import os


class PermissionsManager:
    def __init__(self, config_path="config/users.json"):
        self.config_path = config_path
        self.users = {}
        self.roles = {}
        self.load_permissions()

    def load_permissions(self):
        """
        Загружает данные о пользователях и ролях из файла.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Файл конфигурации не найден: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.users = data.get("users", {})
            self.roles = data.get("roles", {})

    def get_role(self, user_id):
        """
        Возвращает роль пользователя по его ID.
        Если пользователь не найден, возвращает 'guest'.
        """
        return self.users.get(str(user_id), "guest")

    def has_permission(self, user_id, command):
        """
        Проверяет, имеет ли пользователь право на выполнение команды.
        """
        role = self.get_role(user_id)
        allowed_commands = self.roles.get(role, [])
        return command in allowed_commands

    def add_user(self, user_id, role):
        """
        Добавляет нового пользователя или обновляет роль существующего.
        """
        self.users[str(user_id)] = role
        self.save_permissions()

    def remove_user(self, user_id):
        """
        Удаляет пользователя из списка.
        """
        if str(user_id) in self.users:
            del self.users[str(user_id)]
            self.save_permissions()

    def change_role(self, user_id, new_role):
        """
        Изменяет роль пользователя.
        """
        if str(user_id) in self.users:
            self.users[str(user_id)] = new_role
            self.save_permissions()

    def save_permissions(self):
        """
        Сохраняет данные о пользователях и ролях в файл.
        """
        data = {"users": self.users, "roles": self.roles}
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)