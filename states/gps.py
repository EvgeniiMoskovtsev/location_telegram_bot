from aiogram.dispatcher.filters.state import StatesGroup, State

class GpsState(StatesGroup):
    choose_location_state = State()
    working_state = State()



