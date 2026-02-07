import hashlib
import json
import requests
import time  # <--- ДОБАВЛЯЕМ ИМПОРТ
from django.conf import settings

class TinkoffPayment:
    def __init__(self):
        self.terminal_key = settings.TINKOFF_TERMINAL_KEY
        self.password = settings.TINKOFF_PASSWORD
        self.url = settings.TINKOFF_API_URL

    def _generate_token(self, params):
        # Удаляем вложенные объекты и пустые поля
        safe_params = {k: v for k, v in params.items() if k not in ['Receipt', 'DATA'] and v is not None}
        
        safe_params['Password'] = self.password
        
        sorted_params = sorted(safe_params.items())
        concatenated_values = ''.join(str(value) for key, value in sorted_params)
        
        return hashlib.sha256(concatenated_values.encode('utf-8')).hexdigest()

    def init_payment(self, order, items, success_url, fail_url):
        amount_kopecks = int(order.total_cost * 100)

        receipt_items = []
        for item in items:
            receipt_items.append({
                "Name": item.product.name[:64],
                "Price": int(item.price * 100),
                "Quantity": item.quantity,
                "Amount": int(item.price * item.quantity * 100),
                "Tax": "none"
            })

        # --- ГЕНЕРИРУЕМ УНИКАЛЬНЫЙ ID ЗАКАЗА ---
        # Например: 7_1707234567 (ID заказа + текущее время)
        unique_order_id = f"{order.id}_{int(time.time())}"

        params = {
            "TerminalKey": self.terminal_key,
            "Amount": amount_kopecks,
            "OrderId": unique_order_id,  # <--- ИСПОЛЬЗУЕМ УНИКАЛЬНЫЙ ID
            "Description": f"Заказ №{order.id} в Blyur",
            "SuccessURL": success_url,
            "FailURL": fail_url,
            "Receipt": {
                "Email": order.email,
                "Phone": order.phone,
                "Taxation": "usn_income",
                "Items": receipt_items
            }
        }

        params["Token"] = self._generate_token(params)

        response = requests.post(f"{self.url}/Init", json=params)
        return response.json()