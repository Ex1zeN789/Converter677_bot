from aiogram.fsm.state import StatesGroup, State


class BackgroundRemover(StatesGroup):
    waiting_image = State()