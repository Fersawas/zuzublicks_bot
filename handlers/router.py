from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from keyboards.keyboards import keyboard
from constants import MESSAGES


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    kb = keyboard
    await message.answer(MESSAGES["WELCOME"], reply_markup=kb)


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(MESSAGES["HELP"])
