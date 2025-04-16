# core/account_manager.py

from config.config import ACCOUNT_NAMES, BALANCE_TYPES


class AccountManager:
    @staticmethod
    def process_balances(data):
        """
        Обрабатывает данные о балансах и формирует удобочитаемый вывод.
        :param data: JSON-данные от API.
        :return: Строку с форматированным выводом.
        """
        balances = data.get("Data", {}).get("Balance", [])
        if not balances:
            return "Нет данных о балансах."

        grouped_balances = {}
        for balance in balances:
            account_id = balance.get("accountId", "Неизвестный счет")
            balance_type = balance.get("type", "Неизвестный тип")
            amount = balance.get("Amount", {}).get("amount", 0.0)
            currency = balance.get("Amount", {}).get("currency", "RUB")

            if account_id not in grouped_balances:
                grouped_balances[account_id] = []

            grouped_balances[account_id].append({
                "type": balance_type,
                "amount": amount,
                "currency": currency
            })

        result = []
        for account_id, balance_list in grouped_balances.items():
            account_name = ACCOUNT_NAMES.get(account_id, "Неизвестный счет")
            result.append(f"{account_name} ({account_id})")
            for balance in balance_list:
                balance_type = BALANCE_TYPES.get(balance["type"], "Неизвестный тип")
                amount = f"{balance['amount']:.2f}"
                currency = balance["currency"]
                result.append(f" - {balance_type}: {amount} {currency}")
            result.append("-" * 70)

        return "\n".join(result)