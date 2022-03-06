from aiogram.dispatcher.filters.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor
from app.constants import COLORS

class ExampleMarkup(InlineMarkupConstructor):
    class CD(CallbackData, prefix='test'):
        number: str

    def get(self):
        schema = [3, 2]
        actions = [
            {'text': '1', 'callback_data': self.CD(number='1')},
            {'text': '2', 'callback_data': self.CD(number='2').pack()},
            {'text': '3', 'callback_data': '3'},
            {'text': '4', 'callback_data': self.CD(number='4').pack()},
            {'text': '6', 'callback_data': '6'},
        ]
        return self.markup(actions, schema)

class ColorsMarkup(InlineMarkupConstructor):
    def get(self):
        schema =  [2] * (len(COLORS) // 2) + [1]
        actions = [
            {'text': key, 'callback_data': key} for key in COLORS.keys()] + [{"text": "Закрыть", "callback_data": "cancel_photo"}]
        return self.markup(actions, schema)

class CancelMarkup(InlineMarkupConstructor):
    def get(self):
        schema = [1]
        actions = [
            {"text": "Закрыть", "callback_data": "cancel_photo"}]
        return self.markup(actions, schema)
