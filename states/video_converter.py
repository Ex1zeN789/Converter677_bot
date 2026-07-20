from aiogram.fsm.state import StatesGroup, State


class VideoConverter(StatesGroup):
    waiting_video = State()
    waiting_action = State()