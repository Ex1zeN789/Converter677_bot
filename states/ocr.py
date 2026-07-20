from aiogram.fsm.state import StatesGroup, State


class OCR(StatesGroup):
    waiting_image = State()