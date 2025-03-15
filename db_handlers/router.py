import logging

from collections import defaultdict

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy.future import select

from tabulate import tabulate

from db.database import async_session_maker
from db.models import TableModel

from web_scrapping.web_scrapper import parse_url

from keyboards.keyboards import keyboard as kb
from data_utils.data_processing import validate_data
from custom_exceptions import (
    ColumnsDoNotMatch,
    InvalidUrlFormat,
    InvalidXPathFormat,
    EmptyData,
)

from constants import MESSAGES, COLUMNS, ERRORS, LOGGER

router = Router()


async def save_to_db(df, session):
    try:
        for _, row in df.iterrows():
            table = TableModel(**row.to_dict())
            session.add(table)
        await session.commit()
    except Exception as e:
        logging.error(e)
        raise


@router.message(F.text == "Загрузить")
async def upload(message: Message):
    await message.answer(MESSAGES["UPLOAD"])


@router.message(F.document)
async def doc_handler(message: Message):
    try:
        document = message.document

        if document.file_name.endswith(".xlsx"):
            logging.info(f"File name: {document.file_name}")
            file_id = document.file_id
            file_info = await message.bot.get_file(file_id)
            file_data = await message.bot.download_file(file_info.file_path)
            try:
                data = validate_data(file_data, COLUMNS)
                table = tabulate(data, headers="keys", tablefmt="simple")

                await message.answer(
                    f"<pre>{table}</pre>", reply_markup=kb, parse_mode="HTML"
                )

                async with async_session_maker() as session:
                    await save_to_db(data, session)
            except ColumnsDoNotMatch as e:
                await message.answer(str(e))
            except InvalidUrlFormat as e:
                await message.answer(str(e))
            except InvalidXPathFormat as e:
                await message.answer(str(e))
            except EmptyData as e:
                await message.answer(str(e))
            except Exception as e:
                await message.answer(ERRORS["db"])

        else:
            await message.answer(MESSAGES["WRONG_FILE_TYPE"], reply_markup=kb)
    except Exception as e:
        logging.error(e)
        raise


@router.message(Command("parse"))
async def parse(message: Message):
    async with async_session_maker() as session:
        result = await session.execute(
            select(TableModel.title, TableModel.url, TableModel.xpath)
        )
        all_prices = defaultdict(list)
        data = result.all()
        logging.info(LOGGER["parse"])
        _price_dict = {}
        _message = ""
        for title, url, xpath in data:
            try:
                price = await parse_url(url, xpath)
                if price is not None:
                    all_prices[title].extend(price)
            except Exception as e:
                logging.error(str(e))
        for title, price in all_prices.items():
            _price_dict[title] = round(sum(price) / len(price), 2)
            _message += f"Сайт - {title}: средняя цена {_price_dict[title]}\n"
        await message.answer(_message, reply_markup=kb)
