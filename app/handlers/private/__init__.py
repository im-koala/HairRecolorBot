from aiogram import Dispatcher

from app.handlers.private import default, start, help_, photo


def setup(dp: Dispatcher):
    for module in (start, photo, help_, default):
        module.setup(dp)
