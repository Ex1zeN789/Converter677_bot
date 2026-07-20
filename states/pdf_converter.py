from aiogram.fsm.state import StatesGroup, State


class PdfConverter(StatesGroup):
    waiting_file = State()