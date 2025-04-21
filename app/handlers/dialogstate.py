from aiogram.fsm.state import State, StatesGroup


class LinkAccount(StatesGroup):
    waiting_for_name = State()

class WaitGrades(StatesGroup):
    waiting_for_grading = State()