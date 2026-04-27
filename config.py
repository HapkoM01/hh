import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация базы данных
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'hh_parser'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# Список компаний для парсинга (ID компаний на hh.ru)
COMPANIES = [
    '1740',   # Яндекс
    '3529',   # Сбербанк
    '80',     # Mail.ru Group
    '39305',  # Газпромбанк
    '2180',   # Ozon
    '15478',  # Wildberries
    '87021',  # Тинькофф
    '3776',   # МТС
    '1057',   # Билайн
    '2381',   # Ростелеком
]

# URL для API
HH_API_URL = 'https://api.hh.ru'
