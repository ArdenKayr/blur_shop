import hashlib
import json
import requests
from django.conf import settings

class TinkoffPayment:
    def __init__(self):
        self.terminal_key = settings.TINKOFF_TERMINAL_KEY
        self.password = settings.TINKOFF_PASSWORD
        self.url = settings.TINKOFF_API_URL

    def _generate_token(self, params):
        """
        Генерация подписи (Token) для запроса.
        Алгоритм:
        1. Добавить пароль к параметрам.
        2. Отсортировать по ключу.
        3. Склеить значения в одну строку.
        4. Захешировать SHA-256.
        """
        # Удаляем вложенные объекты (Receipt, Data), они не участвуют в подписи
        safe_params = {k: v for k, v in params.items() if k not in ['Receipt', 'DATA']}
        
        safe_params['Password'] = self.password
        
        # Сортировка и склеивание
        sorted_params = sorted(safe_params.items())
        concatenated_values = ''.join(str(value) for key, value in sorted_params)
        
        # Хеширование
        return hashlib.sha256(concatenated_values.encode('utf-8')).hexdigest()

    def init_payment(self, order, items, success_url, fail_url):
        """
        Инициализация платежа (метод Init).
        Принимает объект заказа, список товаров и URL возврата.
        """
        amount_kopecks = int(order.total_cost * 100) # Сумма в копейках

        # Формируем чек (Receipt) для 54-ФЗ
        receipt_items = []
        for item in items:
            receipt_items.append({
                "Name": item.product.name[:64], # Т-Банк ограничивает длину названия
                "Price": int(item.price * 100),
                "Quantity": item.quantity,
                "Amount": int(item.price * item.quantity * 100),
                "Tax": "none" # Без НДС (или укажите vat20 и т.д.)
            })

        params = {
            "TerminalKey": self.terminal_key,
            "Amount": amount_kopecks,
            "OrderId": str(order.id),
            "Description": f"Заказ №{order.id} в Blyur",
            "SuccessURL": success_url,
            "FailURL": fail_url,
            "Receipt": {
                "Email": order.email,
                "Phone": order.phone,
                "Taxation": "usn_income", # УСН доход (поменяйте на свою систему!)
                "Items": receipt_items
            }
        }

        # Генерируем токен (без Receipt внутри генератора)
        params["Token"] = self._generate_token(params)

        # Отправляем запрос (Receipt уже есть в params)
        response = requests.post(f"{self.url}/Init", json=params)
        return response.json()