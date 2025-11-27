"""
Instructor application flow handlers.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import InstructorFlow
from bot.keyboards.inline import (
    get_cities_keyboard, get_auto_types_keyboard,
    get_instructors_keyboard
)
from bot.keyboards.reply import get_phone_keyboard
from bot.services.instructor_service import get_instructors_by_city_and_type
from bot.services.application_service import create_instructor_application
from bot.services.analytics_service import track_event
from bot.services.messaging import send_auto_response_to_user
import re

router = Router()


@router.callback_query(F.data.startswith("city_"), InstructorFlow.waiting_city)
async def process_city_selection(callback: CallbackQuery, state: FSMContext):
    """Process city selection for instructor flow."""
    city_name = callback.data.replace("city_", "")
    await state.update_data(city=city_name)
    await state.set_state(InstructorFlow.waiting_auto_type)
    
    await callback.message.edit_text(
        "🚗 Выберите тип автомобиля:",
        reply_markup=get_auto_types_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("auto_"), InstructorFlow.waiting_auto_type)
async def process_auto_type_selection(callback: CallbackQuery, state: FSMContext):
    """Process auto type selection and show instructors."""
    # Extract auto type key (now uses English: automatic/manual)
    auto_type_key = callback.data.replace("auto_", "")
    # Map to model values
    auto_type_map = {
        'automatic': 'automatic',
        'manual': 'manual',
        # Legacy support for Cyrillic (if any old callbacks exist)
        'Автомат': 'automatic',
        'Механика': 'manual'
    }
    auto_type = auto_type_map.get(auto_type_key, 'automatic')
    
    data = await state.get_data()
    city = data.get('city')
    
    await state.update_data(auto_type=auto_type)
    
    # Get instructors for the city and auto type
    instructors = await get_instructors_by_city_and_type(city, auto_type)
    
    if not instructors:
        await callback.message.edit_text(
            f"😔 В городе {city} пока нет доступных инструкторов для {auto_type_text}.\n"
            "Попробуйте выбрать другой город или тип автомобиля."
        )
        await callback.answer()
        return
    
    # Track event
    await track_event(
        user_id=callback.from_user.id,
        event_type='step_completed',
        step_name='instructor_selection',
        event_data={'city': city, 'auto_type': auto_type}
    )
    
    instructors_text = "👨‍🏫 Доступные инструкторы:\n\n"
    for instructor in instructors[:5]:  # Show first 5
        instructors_text += (
            f"• {instructor.name}\n"
            f"  🚗 {instructor.get_auto_type_display()}\n"
            f"  ⭐ Рейтинг: {instructor.rating}\n"
            f"  📞 {instructor.phone}\n\n"
        )
    
    await callback.message.edit_text(
        instructors_text + "Выберите инструктора:",
        reply_markup=get_instructors_keyboard(instructors)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("instructor_"), InstructorFlow.waiting_instructor_selection)
async def process_instructor_selection(callback: CallbackQuery, state: FSMContext):
    """Process instructor selection and ask for time."""
    instructor_id = int(callback.data.replace("instructor_", ""))
    await state.update_data(instructor_id=instructor_id)
    await state.set_state(InstructorFlow.waiting_time)
    
    await callback.message.edit_text(
        "📅 Введите желаемое время для урока (например: 2024-01-15 14:00):\n"
        "Или отправьте 'любое' для свободного времени."
    )
    await callback.answer()


@router.message(InstructorFlow.waiting_time)
async def process_time(message: Message, state: FSMContext):
    """Process time selection and ask for name."""
    time_text = message.text.strip().lower()
    
    # For MVP, we'll accept "любое" or parse datetime
    if time_text == 'любое':
        time_slot = None
    else:
        # Simple datetime parsing (can be improved)
        from datetime import datetime
        try:
            time_slot = datetime.strptime(time_text, "%Y-%m-%d %H:%M")
        except ValueError:
            await message.answer(
                "❌ Неверный формат времени. Используйте: YYYY-MM-DD HH:MM\n"
                "Или отправьте 'любое'."
            )
            return
    
    await state.update_data(time_slot=time_slot)
    await state.set_state(InstructorFlow.waiting_name)
    
    await message.answer("📝 Введите ваше имя:")


@router.message(InstructorFlow.waiting_name)
async def process_name(message: Message, state: FSMContext):
    """Process student name."""
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("❌ Имя слишком короткое. Введите корректное имя:")
        return
    
    await state.update_data(name=name)
    await state.set_state(InstructorFlow.waiting_phone)
    
    await message.answer(
        "📱 Отправьте ваш номер телефона:",
        reply_markup=get_phone_keyboard()
    )


@router.message(InstructorFlow.waiting_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone from contact."""
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    await process_phone(message, state, phone)


@router.message(InstructorFlow.waiting_phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Process phone from text."""
    phone = message.text.strip()
    # Validate phone format
    if not re.match(r'^\+?7\d{10}$', phone.replace(' ', '').replace('-', '')):
        await message.answer(
            "❌ Неверный формат телефона. Используйте формат: +7XXXXXXXXXX\n"
            "Или отправьте контакт через кнопку."
        )
        return
    
    if not phone.startswith('+'):
        phone = '+7' + phone.replace('+7', '').replace('7', '', 1)
    
    await process_phone(message, state, phone)


async def process_phone(message: Message, state: FSMContext, phone: str):
    """Process phone number and create application."""
    data = await state.get_data()
    
    # Create application
    application = await create_instructor_application(
        telegram_id=message.from_user.id,
        name=data.get('name'),
        phone=phone,
        city=data.get('city'),
        auto_type=data.get('auto_type'),
        instructor_id=data.get('instructor_id'),
        time_slot=data.get('time_slot')
    )
    
    # Track event
    await track_event(
        user_id=message.from_user.id,
        event_type='application_created',
        step_name='application_completed',
        event_data={'application_id': application.id}
    )
    
    # Send auto-response
    await send_auto_response_to_user(message.from_user.id, application)
    
    await message.answer(
        "✅ Спасибо! Ваша заявка отправлена.\n"
        "Инструктор свяжется с вами в ближайшее время.",
        reply_markup=None
    )
    
    await state.clear()

