"""
Конфигурационный файл для дашборда склада
"""

# Настройки приложения
APP_CONFIG = {
    'title': 'Дашборд склада',
    'icon': '📦',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Настройки данных
DATA_CONFIG = {
    'data_path': 'data/',
    'cache_ttl': 300,  # время кэширования в секундах
    'auto_refresh': True
}

# Настройки фильтров
FILTER_CONFIG = {
    'periods': ['день', 'неделя', 'месяц', 'год', 'весь период'],
    'abc_categories': ['Все', 'A', 'B', 'C'],
    'sizes': ['Все', 'XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    'default_period': 'месяц',
    'default_abc': 'A',
    'default_size': 'M'
}

# Настройки графиков
CHART_CONFIG = {
    'color_scheme': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    'background_color': 'rgba(0,0,0,0)',
    'grid_color': '#e0e0e0',
    'font_family': 'Arial, sans-serif'
}

# Настройки метрик
METRICS_CONFIG = {
    'currency_symbol': '₽',
    'number_format': '{:,}',
    'percentage_format': '{:.1f}%',
    'date_format': '%d.%m.%Y'
}

# Цветовая схема для календаря наличия
CALENDAR_COLORS = {
    0: '#ff4444',  # красный - нет товара
    1: '#ffaa00',  # желтый - мало товара
    2: '#44ff44'   # зеленый - достаточно товара
}

# Настройки обновления данных
UPDATE_CONFIG = {
    'auto_update_interval': 300,  # секунды
    'show_last_update': True,
    'update_format': '%d.%m.%Y %H:%M'
}

# Настройки экспорта
EXPORT_CONFIG = {
    'formats': ['CSV', 'Excel', 'JSON'],
    'default_format': 'Excel'
}

# Сообщения и тексты
MESSAGES = {
    'loading': 'Загрузка данных...',
    'no_data': 'Данные не найдены',
    'error': 'Произошла ошибка при загрузке данных',
    'last_update': 'Последнее обновление: {}',
    'data_updated': 'Данные обновлены: {}'
}

