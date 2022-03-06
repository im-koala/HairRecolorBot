from aiogram import Dispatcher
from aiogram.types import Message
from aiogram import html 

async def get_start_message(m: Message):
    await m.answer_sticker("CAACAgIAAxkBAAENnrxh7UpI-RgEmNkUhvUqV27L5-cZiQAChwIAAladvQpC7XQrQFfQkCME")
    await m.answer(
        f'Привет =) Этот бот поможет тебе в пару кликов поменять цвет своих волос на фото! Просто отправь мне свою фоточку\nP.S чуть больше о боте можешь узнать в /help{html.link("&#8288;", "https://telegra.ph/file/1126ea02a1caccdd8480f.jpg")}', disable_web_page_preview=False,
    )


def setup(dp: Dispatcher):
    dp.message.register(get_start_message, commands="start")
