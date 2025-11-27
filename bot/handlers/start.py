"""
Start command and main menu handlers.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import get_start_keyboard, get_certificate_options_keyboard
from bot.states import SchoolFlow, InstructorFlow, CertificateFlow

router = Router()


@router.message(CommandStart())
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Start command handler."""
    await state.clear()
    from bot.config import MINI_APP_URL
    from aiogram.types import WebAppInfo
    
    # Create Web App button
    web_app_button = InlineKeyboardButton(
        text="🚀 Открыть приложение",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    
    welcome_text = (
        "👋 Добро пожаловать в AvtoMat!\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:"
    )
    await message.answer(welcome_text, reply_markup=keyboard)


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    """Return to start menu."""
    await state.clear()
    welcome_text = (
        "👋 Добро пожаловать в AvtoMat!\n\n"
        "Выберите подходящий вариант:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_start_keyboard())
    await callback.answer()


@router.callback_query(F.data == "flow_school")
async def start_school_flow(callback: CallbackQuery, state: FSMContext):
    """Start school application flow."""
    from bot.keyboards.inline import get_cities_keyboard
    await state.set_state(SchoolFlow.waiting_city)
    await callback.message.edit_text(
        "🏙 Выберите город:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "flow_instructor")
async def start_instructor_flow(callback: CallbackQuery, state: FSMContext):
    """Start instructor application flow."""
    from bot.keyboards.inline import get_cities_keyboard
    await state.set_state(InstructorFlow.waiting_city)
    await callback.message.edit_text(
        "🏙 Выберите город:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "flow_certificate")
async def start_certificate_flow(callback: CallbackQuery, state: FSMContext):
    """Start certificate flow."""
    await state.set_state(CertificateFlow.waiting_option)
    await callback.message.edit_text(
        "📜 Выберите опцию:",
        reply_markup=get_certificate_options_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "cert_practice")
async def cert_practice(callback: CallbackQuery, state: FSMContext):
    """Certificate: practice only -> instructor flow."""
    from bot.keyboards.inline import get_cities_keyboard
    await state.set_state(InstructorFlow.waiting_city)
    await callback.message.edit_text(
        "🏙 Выберите город:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "cert_full")
async def cert_full(callback: CallbackQuery, state: FSMContext):
    """Certificate: full course -> school flow."""
    from bot.keyboards.inline import get_cities_keyboard
    await state.set_state(SchoolFlow.waiting_city)
    await callback.message.edit_text(
        "🏙 Выберите город:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "cert_tests")
async def cert_tests(callback: CallbackQuery, state: FSMContext):
    """Certificate: tests only -> under development."""
    await callback.message.edit_text(
        "⏳ Функция 'Только тесты' находится в разработке.\n"
        "Мы скоро добавим эту возможность!"
    )
    await callback.answer()

