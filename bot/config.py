"""
Bot configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Cities in Kazakhstan
CITIES = [
    'Atyrau', 'Kulsary', 'Almaty', 'Astana', 'Aktau', 'Aktobe', 
    'Shymkent', 'Karaganda', 'Pavlodar', 'Taraz', 'Turkestan', 
    'Semey', 'Oral', 'Kostanay', 'Kyzylorda', 'Taldykorgan', 
    'Petropavlovsk', 'Oskemen'
]

# Regional districts (can be added later)
REGIONAL_DISTRICTS = [
    'Жылыойский', 'Индерский'
]

# License categories
CATEGORIES = ['A', 'B', 'BE', 'C', 'CE', 'D', 'DE', 'A1', 'C1', 'D1']

# Training formats
FORMATS = ['Онлайн', 'Оффлайн', 'Гибрид']

# Auto types
AUTO_TYPES = ['Автомат', 'Механика']

# Mini App URL (update in production)
MINI_APP_URL = os.getenv('MINI_APP_URL', 'http://localhost:3000')

