import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class DataHandler:
    """
    Класс для обработки данных дашборда склада
    """
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.products_data = self._load_products_data()
        self.sales_data = self._load_sales_data()
        self.inventory_data = self._load_inventory_data()
        self.payments_data = self._load_payments_data()
    
    def _load_products_data(self):
        """Загрузка данных о товарах"""
        try:
            # Попытка загрузить из файла
            file_path = os.path.join(self.data_path, 'products.json')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        # Возврат примера данных, если файл не найден
        return {
            "tshirtwhite": {
                "title": "Футболка хлопок однотонная базовая",
                "article": "tshirtwhite",
                "quantity_in_set": 1,
                "wb_code": "76280452",
                "orders": 5046,
                "orders_change": 347,
                "sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"],
                "default_size": "M",
                "monthly_plan": None,
                "daily_plan": None,
                "abc_category": "A",
                "cost_price": 495.00,
                "photo_url": "https://via.placeholder.com/150x150?text=Футболка"
            }
        }
    
    def _load_sales_data(self):
        """Загрузка данных о продажах"""
        try:
            file_path = os.path.join(self.data_path, 'sales.csv')
            if os.path.exists(file_path):
                return pd.read_csv(file_path)
        except:
            pass
        
        # Генерация примера данных о продажах
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        sales_data = []
        
        for date in dates:
            daily_sales = np.random.randint(20, 60)
            sales_data.append({
                'date': date,
                'sales': daily_sales,
                'product_id': 'tshirtwhite',
                'size': np.random.choice(['XS', 'S', 'M', 'L', 'XL']),
                'abc_category': 'A'
            })
        
        return pd.DataFrame(sales_data)
    
    def _load_inventory_data(self):
        """Загрузка данных об остатках"""
        try:
            file_path = os.path.join(self.data_path, 'inventory.json')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "tshirtwhite": {
                "name": "Футболки",
                "cost_price": 495.00,
                "wb_warehouse": 0,
                "to_client": 1577,
                "from_client": 566,
                "own_warehouses": 3500,
                "in_transit": 15510,
                "expected_delivery": "30.08.25",
                "total_value": 14975221,
                "avg_sales_period": "день",
                "days_remaining": 1497,
                "end_date": "08.04.2029",
                "last_update": "23 минуты назад"
            }
        }
    
    def _load_payments_data(self):
        """Загрузка данных об оплатах"""
        try:
            file_path = os.path.join(self.data_path, 'payments.csv')
            if os.path.exists(file_path):
                return pd.read_csv(file_path)
        except:
            pass
        
        # Генерация примера данных об оплатах
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        payments_data = []
        
        for date in dates:
            payment_amount = np.random.randint(50000, 200000)
            payments_data.append({
                'date': date,
                'amount': payment_amount,
                'type': np.random.choice(['Поставщик', 'Логистика', 'Маркетплейс'])
            })
        
        return pd.DataFrame(payments_data)
    
    def get_sales_by_period(self, period="месяц", abc_filter="A", size_filter="Все"):
        """Получение данных о продажах за период"""
        filtered_data = self.sales_data.copy()
        
        # Фильтрация по ABC категории
        if abc_filter != "Все":
            filtered_data = filtered_data[filtered_data['abc_category'] == abc_filter]
        
        # Фильтрация по размеру
        if size_filter != "Все":
            filtered_data = filtered_data[filtered_data['size'] == size_filter]
        
        # Фильтрация по периоду
        end_date = datetime.now()
        if period == "день":
            start_date = end_date - timedelta(days=1)
        elif period == "неделя":
            start_date = end_date - timedelta(weeks=1)
        elif period == "месяц":
            start_date = end_date - timedelta(days=30)
        elif period == "год":
            start_date = end_date - timedelta(days=365)
        else:  # весь период
            start_date = filtered_data['date'].min()
        
        filtered_data = filtered_data[
            (filtered_data['date'] >= start_date) & 
            (filtered_data['date'] <= end_date)
        ]
        
        return filtered_data
    
    def get_sales_metrics(self, period="месяц"):
        """Получение основных метрик продаж"""
        sales_data = self.get_sales_by_period(period)
        
        total_sales = sales_data['sales'].sum()
        
        # Расчет изменения по сравнению с предыдущим периодом
        if period == "месяц":
            prev_start = datetime.now() - timedelta(days=60)
            prev_end = datetime.now() - timedelta(days=30)
        else:
            prev_start = datetime.now() - timedelta(days=60)
            prev_end = datetime.now() - timedelta(days=30)
        
        prev_sales = self.sales_data[
            (self.sales_data['date'] >= prev_start) & 
            (self.sales_data['date'] <= prev_end)
        ]['sales'].sum()
        
        change_percent = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
        
        return {
            'total_sales': total_sales,
            'change_percent': round(change_percent, 1),
            'missed_sales': 570,  # Примерное значение
            'current_stock': 13454,
            'recommended_stock': 16000
        }
    
    def get_inventory_info(self, product_id="tshirtwhite"):
        """Получение информации об остатках товара"""
        return self.inventory_data.get(product_id, {})
    
    def get_product_info(self, product_id="tshirtwhite"):
        """Получение информации о товаре"""
        return self.products_data.get(product_id, {})
    
    def get_forecast_data(self):
        """Получение данных прогнозов"""
        return [
            {'SKU': 'S10', 'avg_rating': 3.8, 'days_out': '-', 'missed_sales': 66},
            {'SKU': 'S11', 'avg_rating': 3.8, 'days_out': 3, 'missed_sales': 119},
            {'SKU': 'S21', 'avg_rating': 5.9, 'days_out': 1, 'missed_sales': 188},
            {'SKU': 'S22', 'avg_rating': 6.8, 'days_out': 8, 'missed_sales': 228},
            {'SKU': 'S23', 'avg_rating': 5.7, 'days_out': 3, 'missed_sales': 328},
            {'SKU': 'S24', 'avg_rating': 5.1, 'days_out': 8, 'missed_sales': 528}
        ]
    
    def get_size_distribution(self):
        """Получение распределения по размерам"""
        return {
            'XS': 15,
            'S': 35,
            'M': 33,
            'L': 18,
            'XL': 14,
            'XXL': 5
        }
    
    def get_missed_sales_distribution(self):
        """Получение распределения упущенных продаж"""
        return {
            'SS': 35,
            'M': 33,
            'XL': 16,
            'XXL': 14,
            'XXXL': 5
        }
    
    def get_payment_metrics(self):
        """Получение метрик по оплатам"""
        total_payments = self.payments_data['amount'].sum()
        avg_monthly = self.payments_data['amount'].mean()
        
        return {
            'total_payments': total_payments,
            'avg_monthly': avg_monthly,
            'next_payment_date': "15.08.2024"
        }
    
    def get_calendar_data(self, days=35):
        """Получение данных для календаря наличия товара"""
        # Генерация случайных данных для календаря (0 - нет, 1 - мало, 2 - достаточно)
        return np.random.choice([0, 1, 2], size=(5, 7), p=[0.1, 0.3, 0.6])
    
    def get_transit_info(self):
        """Получение информации о товарах в пути"""
        return {
            'supplier_name': "Фабрика текстиля №1",
            'quantity': 15510,
            'arrival_date': "30.08.25",
            'status': "В пути"
        }

