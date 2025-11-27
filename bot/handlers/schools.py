"""
School application flow handlers.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import SchoolFlow
from bot.keyboards.inline import (
    get_cities_keyboard, get_categories_keyboard, 
    get_formats_keyboard, get_schools_keyboard
)
from bot.keyboards.reply import get_phone_keyboard
from bot.services.school_service import get_schools_by_city
from bot.services.application_service import create_school_application
from bot.services.analytics_service import track_event
from bot.services.messaging import send_auto_response_to_user
import re

router = Router()


@router.callback_query(F.data.startswith("city_"), SchoolFlow.waiting_city)
async def process_city_selection(callback: CallbackQuery, state: FSMContext):
    """Process city selection for school flow."""
    import logging
    logger = logging.getLogger(__name__)
    
    city_name = callback.data.replace("city_", "")
    logger.info(f"Saving city: {city_name} for user {callback.from_user.id}")
    
    await state.update_data(city=city_name)
    
    # Verify data was saved
    data = await state.get_data()
    logger.info(f"Data after city save: {data}")
    
    await state.set_state(SchoolFlow.waiting_category)
    
    await callback.message.edit_text(
        "🚗 Выберите категорию прав:",
        reply_markup=get_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("category_"), SchoolFlow.waiting_category)
async def process_category_selection(callback: CallbackQuery, state: FSMContext):
    """Process category selection."""
    import logging
    logger = logging.getLogger(__name__)
    
    category = callback.data.replace("category_", "")
    logger.info(f"Saving category: {category} for user {callback.from_user.id}")
    
    # Get current data first
    current_data = await state.get_data()
    logger.info(f"Current data before category save: {current_data}")
    
    await state.update_data(category=category)
    
    # Verify data was saved
    data_after = await state.get_data()
    logger.info(f"Data after category save: {data_after}")
    
    # Explicitly set state
    await state.set_state(SchoolFlow.waiting_format)
    logger.info(f"State set to waiting_format after category selection: {category}")
    
    # Verify state was set
    verify_state = await state.get_state()
    logger.info(f"Verified state after setting: {verify_state}")
    
    await callback.message.edit_text(
        "📚 Выберите формат обучения:",
        reply_markup=get_formats_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("format_"))
async def process_format_selection(callback: CallbackQuery, state: FSMContext):
    """Process format selection and show schools - NO STATE FILTER to catch all format callbacks."""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Extract format from callback (now uses English keys: online, offline, hybrid)
        format_key = callback.data.replace("format_", "")
        # Map back to Russian for display/storage
        format_map = {
            'online': 'Онлайн',
            'offline': 'Оффлайн',
            'hybrid': 'Гибрид',
            # Legacy support for old Cyrillic callbacks (if any cached)
            'Онлайн': 'Онлайн',
            'Оффлайн': 'Оффлайн',
            'Гибрид': 'Гибрид'
        }
        format_type = format_map.get(format_key, 'Оффлайн')  # Default to offline if not found
        
        # Get state first
        current_state = await state.get_state()
        logger.info(f"Current state before format processing: {current_state}")
        
        data = await state.get_data()
        city = data.get('city')
        category = data.get('category')
        
        logger.info(f"Format selection: callback_data={callback.data}, format_key={format_key}, format_type={format_type}")
        logger.info(f"State data: city={city}, category={category}")
        logger.info(f"Full state data: {data}")
        logger.info(f"User ID: {callback.from_user.id}")
        
        # Check if we have required data instead of strict state check
        if not city or not category:
            logger.warning(f"Missing data: city={city}, category={category}")
            # Try to get data from callback if possible (fallback)
            # But this shouldn't happen - data should be in state
            logger.error(f"CRITICAL: State data lost! User {callback.from_user.id} has no city/category")
            await callback.answer(
                "⚠️ Данные не сохранены. Пожалуйста, начните заново: /start\n\n"
                "Это может произойти, если вы нажали на старую кнопку.",
                show_alert=True
            )
            await state.clear()
            return
        
        await state.update_data(format=format_type)
        logger.info(f"Format saved: {format_type}")
        
        # Get schools for the city
        logger.info(f"Fetching schools for city: {city}")
        schools = await get_schools_by_city(city)
        logger.info(f"Found {len(schools)} schools")
        
        if not schools:
            logger.warning(f"No schools found for city: {city}")
            await callback.message.edit_text(
                f"😔 В городе {city} пока нет доступных автошкол.\n"
                "Попробуйте выбрать другой город."
            )
            await callback.answer()
            return
        
        # Set state to waiting for school selection
        await state.set_state(SchoolFlow.waiting_school_selection)
        logger.info("State set to waiting_school_selection")
        
        # Track event (with error handling)
        try:
            await track_event(
                user_id=callback.from_user.id,
                event_type='step_completed',
                step_name='school_selection',
                event_data={'city': city, 'category': category, 'format': format_type}
            )
        except Exception as e:
            logger.warning(f"Failed to track event: {e}")
        
        schools_text = "🏫 Доступные автошколы:\n\n"
        for school in schools[:5]:  # Show first 5
            schools_text += (
                f"• {school.name}\n"
                f"  ⭐ Рейтинг: {school.rating}\n"
                f"  📍 {school.address}\n"
                f"  💰 Цена: уточняйте\n\n"
            )
        
        logger.info(f"Prepared schools text, length: {len(schools_text)}")
        logger.info(f"Creating keyboard for {len(schools)} schools")
        
        try:
            keyboard = get_schools_keyboard(schools)
            logger.info("Keyboard created successfully")
            
            await callback.message.edit_text(
                schools_text + "Выберите автошколу:",
                reply_markup=keyboard
            )
            await callback.answer()
            logger.info(f"Successfully showed {len(schools)} schools for city {city}")
        except Exception as e:
            # If edit fails, send new message
            logger.error(f"Error editing message: {e}", exc_info=True)
            try:
                keyboard = get_schools_keyboard(schools)
                await callback.message.answer(
                    schools_text + "Выберите автошколу:",
                    reply_markup=keyboard
                )
                await callback.answer()
                logger.info("Sent new message instead of editing")
            except Exception as e2:
                logger.error(f"Failed to send new message: {e2}", exc_info=True)
                await callback.answer(f"Ошибка: {str(e)}", show_alert=True)
    except Exception as e:
        logger.error(f"Error in process_format_selection: {e}", exc_info=True)
        import traceback
        logger.error(traceback.format_exc())
        await callback.answer(f"Произошла ошибка: {str(e)}. Попробуйте еще раз.", show_alert=True)


@router.callback_query(F.data.startswith("school_"), SchoolFlow.waiting_school_selection)
async def process_school_selection(callback: CallbackQuery, state: FSMContext):
    """Process school selection and ask for name."""
    school_id = int(callback.data.replace("school_", ""))
    await state.update_data(school_id=school_id)
    await state.set_state(SchoolFlow.waiting_name)
    
    await callback.message.edit_text(
        "📝 Введите ваше имя:"
    )
    await callback.answer()


@router.message(SchoolFlow.waiting_name)
async def process_name(message: Message, state: FSMContext):
    """Process student name."""
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("❌ Имя слишком короткое. Введите корректное имя:")
        return
    
    await state.update_data(name=name)
    await state.set_state(SchoolFlow.waiting_phone)
    
    await message.answer(
        "📱 Отправьте ваш номер телефона:",
        reply_markup=get_phone_keyboard()
    )


@router.message(SchoolFlow.waiting_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone from contact."""
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    await process_phone(message, state, phone)


@router.message(SchoolFlow.waiting_phone)
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
    application = await create_school_application(
        telegram_id=message.from_user.id,
        name=data.get('name'),
        phone=phone,
        city=data.get('city'),
        category=data.get('category'),
        format_type=data.get('format'),
        school_id=data.get('school_id')
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
        "Автошкола свяжется с вами в ближайшее время.",
        reply_markup=None
    )
    
    await state.clear()

