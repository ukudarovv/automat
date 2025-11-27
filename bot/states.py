"""
FSM states for bot flows.
"""
from aiogram.fsm.state import State, StatesGroup


class SchoolFlow(StatesGroup):
    """States for school application flow."""
    waiting_city = State()
    waiting_category = State()
    waiting_format = State()
    waiting_school_selection = State()
    waiting_name = State()
    waiting_phone = State()


class InstructorFlow(StatesGroup):
    """States for instructor application flow."""
    waiting_city = State()
    waiting_auto_type = State()
    waiting_instructor_selection = State()
    waiting_time = State()
    waiting_name = State()
    waiting_phone = State()


class CertificateFlow(StatesGroup):
    """States for certificate flow."""
    waiting_option = State()

