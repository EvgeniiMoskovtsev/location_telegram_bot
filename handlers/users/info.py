import asyncio

from loader import dp, bot
from aiogram import types


from aiogram.dispatcher.filters import Command
from keyboards.inline.choice_buttons import *
from keyboards.inline.callback_datas import *

from keyboards.default.gps import *
from states.gps import GpsState


@dp.message_handler(Command("start"))
async def create_notification_buttons(message: types.Message):
    await message.answer(
        text="Привет", reply_markup=gps_button
    )


@dp.message_handler(text="Уведомление по геопозиции")
async def get_target_place(message: types.Message):
    await message.answer(text="Вы выбрали 'Уведомление по геопозиции'", reply_markup=ReplyKeyboardRemove())

    await GpsState.choose_location_state.set()

    await message.answer(text="Напишите радиус в метрах от точки, около которой вам прислать уведомление.")


@dp.message_handler(state=GpsState.choose_location_state)
async def get_target_place(message: types.Message):
    radius = message.text

    await message.answer(text="Выберите локацию в настройках, около которой вам прислать уведомление.")


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=GpsState.choose_location_state)
async def get_target_place(message: types.Message):
    target_location = message.location

    await message.answer(text="А теперь включите трансляцию локации")
    await GpsState.working_state.set()


@dp.edited_message_handler(content_types=types.ContentTypes.LOCATION, state=GpsState.working_state)
async def loc(message: types.Message):
    location = message.location
    updates = await bot.get_updates()
    print(location)




#Попросить транслировать локацию,