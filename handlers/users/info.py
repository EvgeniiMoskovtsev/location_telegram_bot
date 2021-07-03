import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from aiogram import types


from aiogram.dispatcher.filters import Command
from keyboards.inline.choice_buttons import *
from keyboards.inline.callback_datas import *

from keyboards.default.gps import *
from states.gps import GpsState
from utils.calculate_meters_from_gps import get_meters


@dp.message_handler(Command("start"))
@dp.message_handler(Text(equals='старт', ignore_case=True), state='*')
async def create_notification_buttons(message: types.Message):
    await message.answer(
        text="Привет, нажмите на 'Уведомление по геопозиции', и следуй инструкциям.\n"
             "Помни, погрешность в вычислениях около 1%.\n"
             "Если вы что-то ввели неправильно напишите 'отмена', а потом 'старт'", reply_markup=gps_button
    )


@dp.message_handler(text="Уведомление по геопозиции")
async def get_target_place(message: types.Message):
    #await message.answer(text="Вы выбрали 'Уведомление по геопозиции'", reply_markup=ReplyKeyboardRemove())

    await GpsState.choose_location_state.set()

    await message.answer(text="Напишите цифрами радиус в метрах от точки, около которой вам прислать уведомление.", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message: not message.text.isdigit(), state=GpsState.choose_location_state)
async def wrong_get_target_place(message: types.Message):
    await message.answer(text="Цифрами пожалуйста)")


@dp.message_handler(lambda message: message.text.isdigit(), state=GpsState.choose_location_state)
async def get_target_place(message: types.Message, state: FSMContext):
    radius = message.text
    await state.update_data(radius=radius)

    await message.answer(text="Выберите локацию в настройках, около которой вам прислать уведомление.\n"
                              "(Нажмите на скрепку, в зеленом окошке 'Геопозиция', перемещайте карту "
                              "и нажмите синюю кнопку 'Отправить выбранную геопозицию'")


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=GpsState.choose_location_state)
async def get_target_place(message: types.Message, state: FSMContext):
    target_location = message.location
    await state.update_data(target_location=target_location)

    await message.answer(text="А теперь включите трансляцию геопозиции\n"
                              "(Она находится там же, только зеленая кнопка)")
    await GpsState.working_state.set()


@dp.edited_message_handler(content_types=types.ContentTypes.LOCATION, state=GpsState.working_state)
async def loc(message: types.Message, state: FSMContext):

    #updates = await bot.get_updates() #локацию можно и из сообщения вытаскивать

    state_data = await state.get_data()

    radius = int(state_data["radius"])
    target_location = [state_data["target_location"]["latitude"], state_data["target_location"]["longitude"]]
    current_location = [message.location["latitude"], message.location["longitude"]]

    meters = await get_meters(target_location, current_location)

    if meters < radius:
        await message.answer(f"Вы почти на месте! \n"
                             f"До места вам {radius} метров\т"
                             f"Не забудьте отключить трансляцию геопозиции")
        await state.finish()

    await asyncio.sleep(5)




@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer(text="Отмена", reply_markup=ReplyKeyboardRemove())