"""
Reply keyboards for bot.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_phone_keyboard():
    """Request phone number keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_main_menu_keyboard():
    """Main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

