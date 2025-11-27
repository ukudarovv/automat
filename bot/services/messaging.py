"""
Messaging service for auto-responses.
"""
from aiogram import Bot
from bot.config import TELEGRAM_BOT_TOKEN
from bot.services.database import Application
from bot.keyboards.inline import get_whatsapp_keyboard
from typing import Optional
from asgiref.sync import sync_to_async

bot_instance: Optional[Bot] = None


def get_bot() -> Bot:
    """Get bot instance."""
    global bot_instance
    if bot_instance is None:
        bot_instance = Bot(token=TELEGRAM_BOT_TOKEN)
    return bot_instance


@sync_to_async
def _get_school_whatsapp(school):
    """Get school WhatsApp phone synchronously."""
    if not school:
        return None
    try:
        whatsapp = school.whatsapp
        if not whatsapp and school.user:
            whatsapp = school.user.phone
        return whatsapp
    except:
        return None


@sync_to_async
def _format_school_response_sync(application):
    """Format school response synchronously."""
    school = application.school
    city_name = application.city.name if application.city else ""
    message = (
        f"✅ <b>Спасибо за заявку!</b>\n\n"
        f"🏫 <b>Автошкола:</b> {school.name}\n"
        f"📍 <b>Адрес:</b> {school.address}\n"
        f"🏙 <b>Город:</b> {city_name}\n"
        f"🚗 <b>Категория:</b> {application.category}\n"
        f"📚 <b>Формат:</b> {application.get_format_display()}\n"
    )
    
    if school.payment_link_kaspi:
        message += f"\n💳 <b>Оплата Kaspi:</b> {school.payment_link_kaspi}\n"
    if school.payment_link_halyk:
        message += f"💳 <b>Оплата HalykPay:</b> {school.payment_link_halyk}\n"
    
    message += "\nАвтошкола свяжется с вами в ближайшее время!"
    return message


@sync_to_async
def _format_instructor_response_sync(application):
    """Format instructor response synchronously."""
    instructor = application.instructor
    city_name = application.city.name if application.city else ""
    time_info = ""
    if application.time_slot:
        time_info = f"\n📅 <b>Время:</b> {application.time_slot.strftime('%d.%m.%Y %H:%M')}\n"
    
    message = (
        f"✅ <b>Спасибо за заявку!</b>\n\n"
        f"👨‍🏫 <b>Инструктор:</b> {instructor.name}\n"
        f"🏙 <b>Город:</b> {city_name}\n"
        f"🚗 <b>Тип авто:</b> {instructor.get_auto_type_display()}\n"
        f"{time_info}"
    )
    
    if instructor.payment_link_kaspi:
        message += f"\n💳 <b>Оплата Kaspi:</b> {instructor.payment_link_kaspi}\n"
    if instructor.payment_link_halyk:
        message += f"💳 <b>Оплата HalykPay:</b> {instructor.payment_link_halyk}\n"
    
    message += "\nИнструктор свяжется с вами в ближайшее время!"
    return message


async def send_auto_response_to_user(telegram_id: int, application: Application):
    """Send auto-response message to user."""
    bot = get_bot()
    
    if application.school:
        message = await _format_school_response_sync(application)
        whatsapp_phone = await _get_school_whatsapp(application.school)
    elif application.instructor:
        message = await _format_instructor_response_sync(application)
        whatsapp_phone = application.instructor.phone
    else:
        return
    
    # Send message
    if whatsapp_phone:
        keyboard = get_whatsapp_keyboard(
            whatsapp_phone,
            text=f"Здравствуйте! Я оставил(а) заявку через AvtoMat."
        )
    else:
        keyboard = None
    
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=message,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"Error sending message: {e}")


# Legacy functions kept for compatibility, but should use async versions
def format_school_response(application: Application) -> str:
    """Format school auto-response message (sync version - use async version in async context)."""
    # This function should not be used in async context
    # Use _format_school_response_sync instead
    school = application.school
    city_name = application.city.name if application.city else ""
    message = (
        f"✅ <b>Спасибо за заявку!</b>\n\n"
        f"🏫 <b>Автошкола:</b> {school.name}\n"
        f"📍 <b>Адрес:</b> {school.address}\n"
        f"🏙 <b>Город:</b> {city_name}\n"
        f"🚗 <b>Категория:</b> {application.category}\n"
        f"📚 <b>Формат:</b> {application.get_format_display()}\n"
    )
    
    if school.payment_link_kaspi:
        message += f"\n💳 <b>Оплата Kaspi:</b> {school.payment_link_kaspi}\n"
    if school.payment_link_halyk:
        message += f"💳 <b>Оплата HalykPay:</b> {school.payment_link_halyk}\n"
    
    message += "\nАвтошкола свяжется с вами в ближайшее время!"
    return message


def format_instructor_response(application: Application) -> str:
    """Format instructor auto-response message (sync version - use async version in async context)."""
    # This function should not be used in async context
    # Use _format_instructor_response_sync instead
    instructor = application.instructor
    city_name = application.city.name if application.city else ""
    time_info = ""
    if application.time_slot:
        time_info = f"\n📅 <b>Время:</b> {application.time_slot.strftime('%d.%m.%Y %H:%M')}\n"
    
    message = (
        f"✅ <b>Спасибо за заявку!</b>\n\n"
        f"👨‍🏫 <b>Инструктор:</b> {instructor.name}\n"
        f"🏙 <b>Город:</b> {city_name}\n"
        f"🚗 <b>Тип авто:</b> {instructor.get_auto_type_display()}\n"
        f"{time_info}"
    )
    
    if instructor.payment_link_kaspi:
        message += f"\n💳 <b>Оплата Kaspi:</b> {instructor.payment_link_kaspi}\n"
    if instructor.payment_link_halyk:
        message += f"💳 <b>Оплата HalykPay:</b> {instructor.payment_link_halyk}\n"
    
    message += "\nИнструктор свяжется с вами в ближайшее время!"
    return message


async def send_auto_response(application: Application):
    """Send auto-response (used from CRM)."""
    if application.student and application.student.telegram_id:
        await send_auto_response_to_user(application.student.telegram_id, application)

