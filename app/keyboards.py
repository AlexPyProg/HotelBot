from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


points = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На Грибоедова', callback_data='На Грибоедова'),
     InlineKeyboardButton(text='Юсуповский сад', callback_data='Юсуповский сад')],
    [InlineKeyboardButton(text='На Восстания', callback_data='На Восстания'),
     InlineKeyboardButton(text='На Фонтанке', callback_data='На Фонтанке')],
    [InlineKeyboardButton(text='На Московском', callback_data='На Московском'),
     InlineKeyboardButton(text='На Вознесенском', callback_data='На Вознесенском')]
])

point_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Номера', callback_data='rooms')],
    [InlineKeyboardButton(text='Расположение', callback_data='geo')],
    [InlineKeyboardButton(text='Забронировать', callback_data='reserve')],
    [InlineKeyboardButton(text='Назад', callback_data='main_menu')],
])


def pagination(index, total, point):
    if index == 0:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Далее', callback_data='next')],
            [InlineKeyboardButton(text='К информации', callback_data=point),
             InlineKeyboardButton(text='К выбору отелей', callback_data='main_menu')]
        ])
    elif index == total - 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='back')],
            [InlineKeyboardButton(text='К информации', callback_data=point),
             InlineKeyboardButton(text='К выбору отелей', callback_data='main_menu')]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='back'),
             InlineKeyboardButton(text='Далее', callback_data='next')],
            [InlineKeyboardButton(text='К информации', callback_data=point),
             InlineKeyboardButton(text='К выбору отелей', callback_data='main_menu')]
        ])