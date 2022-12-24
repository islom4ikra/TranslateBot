from aiogram.dispatcher.filters.state import State, StatesGroup


class Translate(StatesGroup):
    lang = State()
    text = State()
    speech = State()