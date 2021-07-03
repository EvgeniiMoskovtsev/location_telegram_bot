from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

gps_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Уведомление по геопозиции")
        ]
    ],
    resize_keyboard=True
)

