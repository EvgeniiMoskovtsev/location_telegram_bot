from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton(text="Напомнить"), KeyboardButton(text="Парсинг блогеров")]
    ],
    resize_keyboard=True,
)