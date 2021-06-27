from aiogram.utils.callback_data import CallbackData

buy_data = CallbackData("buy", "item_id")

vote_data = CallbackData("vote", "action", "amount", "item_id")