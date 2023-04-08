from aiogram.fsm.state import StatesGroup, State


class FSMlowprice(StatesGroup):

    fill_city = State()
    fill_hotels_count = State()
    fill_photo = State()
    fill_photo_count = State()
    fill_ckeckIn = State()
    fill_ckeckOut = State()
    fill_adults = State()


class FSMhighprice(StatesGroup):

    fill_city = State()
    fill_hotels_count = State()
    fill_photo = State()
    fill_photo_count = State()
    fill_ckeckIn = State()
    fill_ckeckOut = State()
    fill_adults = State()


class FSMbestdeal(StatesGroup):

    fill_city = State()
    fill_adults = State()
    fill_hotels_count = State()
    fill_photo = State()
    fill_photo_count = State()
    fill_ckeckIn = State()
    fill_ckeckOut = State()
    fill_price = State()
    fill_distance = State()


class FSMchoice(StatesGroup):

    get_choice = State()



