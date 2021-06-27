from loader import dp, bot
from aiogram import types


from aiogram.dispatcher.filters import Command
from keyboards.inline.choice_buttons import *
from keyboards.inline.callback_datas import *


    
@dp.message_handler(Command("items"))
async def show_items(message: types.Message):

    await message.answer_photo(photo="https://www.vse-strani-mira.ru/images/stories/picture/000044445/7777777777777ale_1200.jpg",
                               caption="Исландия",
                               reply_markup=create_button("0"))

    await message.answer_photo(photo="https://avatars.mds.yandex.net/get-zen_doc/3337090/pub_5fae852cf2466e1810663c45_5fae9f07f2466e181095339f/scale_1200",
                               caption="Армения",
                               reply_markup=create_button("1"))



@dp.callback_query_handler(buy_data.filter())
async def buy_tour(call: types.CallbackQuery, callback_data: dict):

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_caption(caption=f"Покупай товар номер {callback_data.get('item_id')}")


@dp.callback_query_handler(vote_data.filter(action="up"))
async def vote_up(call: types.CallbackQuery, callback_data: dict):
    await call.answer(text=f"Тебе понравился этот товар")

    #callback_data["amount"] = str(int(callback_data["amount"]) + 1)
    #await call.message.answer(text=f"Вы подняли рейтинг до {callback_data.get('amount')}")


@dp.callback_query_handler(vote_data.filter(action="down"))
async def vote_up(call: types.CallbackQuery, callback_data: dict):
    await call.answer(text=f"Тебе не понравился этот товар")

   # callback_data["amount"] = str(int(callback_data["amount"]) - 1)


