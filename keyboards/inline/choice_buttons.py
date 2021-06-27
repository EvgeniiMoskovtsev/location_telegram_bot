from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_data, vote_data
from aiogram.utils.emoji import emojize

def create_button(item_id):

    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить тур", callback_data=buy_data.new(item_id=item_id))],

    [InlineKeyboardButton(text=emojize(":thumbs_up:"), callback_data=vote_data.new(action="up", amount="0", item_id=item_id)),
     InlineKeyboardButton(text=emojize(":thumbs_down:"), callback_data=vote_data.new(action="down", amount="0", item_id=item_id))],

    [InlineKeyboardButton(text="Поделиться с друзьями", switch_inline_query=item_id)]
])
