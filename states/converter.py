from aiogram.fsm.state import StatesGroup, State


class ImageConverter(StatesGroup):
    waiting_image = State()
    waiting_action = State()