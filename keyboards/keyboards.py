from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants import BUTTONS


upload_btn = KeyboardButton(text=BUTTONS["upload"], callback_data="upload")
keyboard = ReplyKeyboardMarkup(keyboard=[[upload_btn]], resize_keyboard=True)
