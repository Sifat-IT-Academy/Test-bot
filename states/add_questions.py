from aiogram.fsm.state import State, StatesGroup

class Questions(StatesGroup):
    test_name = State()
    question = State()
    number_question = State()
    a = State()
    b = State()
    c = State()
    d = State()
    answer = State()