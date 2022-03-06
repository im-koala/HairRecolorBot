from aiogram import Dispatcher
from aiogram.types import Message


async def get_help_message(m: Message):
    await m.answer_sticker("CAACAgEAAxkBAAEOdftiIk6QncRZt54nTUb_7BFLg7p84wACwwADewoQR2GwJX8IurkbIwQ")
    await m.answer("Приветик =)\nЯ ботик, который может поменять цвет твоих волос в 1 клик!\nПредпочтения по фотке, что бы получить наилучший результат: желательно, что бы волосы были хорошо видны + не были сильно засвечены. Если что, пиши моему создателю - @just_kkoala\n")


def setup(dp: Dispatcher):
    dp.message.register(get_help_message, commands="help")
