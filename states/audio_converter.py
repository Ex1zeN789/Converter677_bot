from aiogram.fsm.state import StatesGroup, State


class AudioConverter(StatesGroup):
    waiting_format = State()
    waiting_audio = State()