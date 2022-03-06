import os 
import uuid
import tempfile
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from aiogram.types import FSInputFile
from aiogram.dispatcher.filters import Text

from app.keyboards.private.inline import CancelMarkup, ColorsMarkup
from app.constants import COLORS
from app.services.makeup import recolor_hair
from app.utils.sync import run_sync

async def start_photo_coloring(m: Message, bot: Bot):
    user_id = m.from_user.id
    files = os.listdir('images')
    for file in files:
        if str(user_id) in file:
            await m.answer("Так, похоже ты уже отправлял фото и забыл нажать кнопку \"Закрыть\", если не хочешь искать прошлое сообщение, то просто нажми на эту кнопку ниже и еще раз отправь фотку, которую хочешь обработать =)", reply_markup=CancelMarkup().get())
            return 
            
    photo = m.photo[-1]
    photo_path = f"./images/{uuid.uuid4()}{user_id}.jpg" 
    await bot.download(photo, photo_path)
    await m.answer_photo(FSInputFile(photo_path), caption="Выбери цвет, в который хочешь покрасить волосы:", reply_markup=ColorsMarkup().get())

async def cancel_photo_coloring(c: CallbackQuery):
    files = os.listdir('images')
    for file in files:
        if str(c.from_user.id) in file:
            os.remove(f"./images/{file}")
    await c.message.delete() #type: ignore
    
async def process_photo(c: CallbackQuery):
    c.answer(cache_time=20)
    files = os.listdir('images')
    for file in files:
        if str(c.from_user.id) in file:
            photo_path = f"./images/{file}"
            break

    color: str = c.data
    rgb_color: list = COLORS[color]
    await c.message.edit_caption("Подожди чуток...", reply_markup=None)

    with tempfile.NamedTemporaryFile(suffix=".jpg", prefix="bot_file") as f:
        output_photo_path = f.name
        try:
            await run_sync(recolor_hair, photo_path, output_photo_path, rgb_color)
        except Exception as e:
            logging.error(e)
            await c.message.edit_caption("Что-то пошло не так, попробуй отправить другое фото =(", reply_markup=None)
            return 
        await c.message.delete() #type: ignore
        await c.message.answer_photo(FSInputFile(output_photo_path), caption="Выбери цвет в который хочешь покрасить волосы:",reply_markup=ColorsMarkup().get())

def setup(dp: Dispatcher):
    dp.callback_query.register(cancel_photo_coloring, text="cancel_photo")
    dp.callback_query.register(process_photo, Text(text=list(COLORS.keys())))
    dp.message.register(start_photo_coloring, ContentTypesFilter(content_types=["photo"]))
