"""
Inline keyboards for bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import CITIES, CATEGORIES, FORMATS, AUTO_TYPES


def get_start_keyboard():
    """Start menu keyboard."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❗ Нет водительских прав — хочу стать водителем",
                callback_data="flow_school"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Есть водительские права — хочу освежить знания",
                callback_data="flow_instructor"
            )
        ],
        [
            InlineKeyboardButton(
                text="📜 Есть сертификат, но не сдал экзамен",
                callback_data="flow_certificate"
            )
        ]
    ])
    return keyboard


def get_cities_keyboard():
    """Cities selection keyboard."""
    buttons = []
    for i in range(0, len(CITIES), 2):
        row = []
        if i < len(CITIES):
            row.append(InlineKeyboardButton(text=CITIES[i], callback_data=f"city_{CITIES[i]}"))
        if i + 1 < len(CITIES):
            row.append(InlineKeyboardButton(text=CITIES[i+1], callback_data=f"city_{CITIES[i+1]}"))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_categories_keyboard():
    """License categories keyboard."""
    buttons = []
    for i in range(0, len(CATEGORIES), 3):
        row = []
        for j in range(3):
            if i + j < len(CATEGORIES):
                row.append(InlineKeyboardButton(
                    text=CATEGORIES[i+j], 
                    callback_data=f"category_{CATEGORIES[i+j]}"
                ))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_formats_keyboard():
    """Training formats keyboard."""
    # Use English keys for callback_data to avoid encoding issues
    format_map = {
        'online': FORMATS[0],  # 'Онлайн'
        'offline': FORMATS[1],  # 'Оффлайн'
        'hybrid': FORMATS[2]   # 'Гибрид'
    }
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=FORMATS[0], callback_data="format_online")],
        [InlineKeyboardButton(text=FORMATS[1], callback_data="format_offline")],
        [InlineKeyboardButton(text=FORMATS[2], callback_data="format_hybrid")]
    ])
    return keyboard


def get_auto_types_keyboard():
    """Auto types keyboard."""
    # Use English keys for callback_data to avoid encoding issues
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=AUTO_TYPES[0], callback_data="auto_automatic")],  # 'Автомат'
        [InlineKeyboardButton(text=AUTO_TYPES[1], callback_data="auto_manual")]      # 'Механика'
    ])
    return keyboard


def get_schools_keyboard(schools):
    """Schools list keyboard."""
    buttons = []
    for school in schools:
        buttons.append([
            InlineKeyboardButton(
                text=f"{school.name} ⭐{school.rating}",
                callback_data=f"school_{school.id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_instructors_keyboard(instructors):
    """Instructors list keyboard."""
    buttons = []
    for instructor in instructors:
        buttons.append([
            InlineKeyboardButton(
                text=f"{instructor.name} ({instructor.get_auto_type_display()}) ⭐{instructor.rating}",
                callback_data=f"instructor_{instructor.id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_certificate_options_keyboard():
    """Certificate flow options keyboard."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Только практика",
                callback_data="cert_practice"
            )
        ],
        [
            InlineKeyboardButton(
                text="Полный курс заново",
                callback_data="cert_full"
            )
        ],
        [
            InlineKeyboardButton(
                text="Только тесты",
                callback_data="cert_tests"
            )
        ]
    ])
    return keyboard


def get_whatsapp_keyboard(phone, text=""):
    """WhatsApp deep link button."""
    phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '')
    url = f"https://wa.me/{phone_clean}?text={text}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Написать в WhatsApp", url=url)]
    ])
    return keyboard

