import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile

from app import keyboards as kb
from app.google.google_auth import get_row
from config import BOT_TOKEN, locations, texts

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

dev_id = 694693497
admin_id = 1320327228
admin_ids = [dev_id, admin_id]
users = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(FSInputFile(path=r'C:\Users\Александр\PycharmProjects\HotelBot\app\static\logo.png'),
                               f'Добро пожаловать в сеть отелей Laika в Санкт-Петербурге! '
                               f'Мы предлагаем комфорт и стиль по '
                               f'доступной цене, идеально подходящие для тех, кто ценит уют и удобство. Наши отели '
                               f'расположены в центре города, что позволяет гостям легко добираться до главных '
                               f'достопримечательностей, деловых центров и транспортных узлов. '
                               f'\n\nКаждый адрес отличается '
                               f'современным дизайном, где каждая деталь продумана для вашего комфорта. Мы предлагаем '
                               f'уютные номера с эргономичной мебелью, качественным постельным бельем и всем '
                               f'необходимым'
                               f'для отдыха после насыщенного дня. В наших отелях вы найдете все, что нужно для '
                               f'комфортного'
                               f'пребывания: бесплатный Wi-Fi, зоны для работы и отдыха, а также дружелюбный сервис.')
    await message.answer('Вот адреса отелей Laika: ',
                         reply_markup=kb.points)


@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    print(callback.data)
    await callback.answer('')
    uid = callback.from_user.id
    if callback.data in ['На Грибоедова', 'Юсуповский сад', 'На Восстания',
                         'На Фонтанке', 'На Московском', 'На Вознесенском']:
        point = callback.data
        if users.get(uid):
            if users[uid].get('msg_photo'):
                try:
                    for msg_id in users[uid]['msg_photo']:
                        await bot.delete_message(callback.message.chat.id, msg_id)
                except Exception:
                    pass
            if users[uid].get('msg_text'):
                try:
                    await bot.delete_message(callback.message.chat.id, users[uid]['msg_text'])
                except Exception:
                    pass

        users[uid] = {
            'index': 0,
            'point': point,
            'categories': [],
            'captions': [],
            'links_list': [],
            'msg_photo': None,  # ID сообщения с фото
            'msg_text': None  # ID сообщения с текстом
        }

        try:
            msg_text = await callback.message.edit_text(texts[point],
                                                        reply_markup=kb.point_info)
            users[uid]['msg_text'] = msg_text.message_id

        except TelegramBadRequest:
            msg_text = await callback.message.answer(texts[point],
                                                     reply_markup=kb.point_info)
            users[uid]['msg_text'] = msg_text.message_id

        users[uid]['categories'], users[uid]['captions'], users[uid]['links_list'] = get_row(point)

    if callback.data in {'rooms', 'back', 'next'}:
        if users[uid]['links_list'] == [] or users[uid]['captions'] == []:
            await callback.message.answer('Нет информации для выбранного отеля\n\nВыберите другой отель',
                                          reply_markup=kb.points)
            return
        await callback.message.delete()
        if callback.data == 'back':
            users[uid]['index'] -= 1
        elif callback.data == 'next':
            users[uid]['index'] += 1

        index = users[uid]['index']
        # print(users[uid])
        media_group = [InputMediaPhoto(media=link) for link in users[uid]['links_list'][index]]
        print(media_group, '\n\n')
        if users[uid].get('msg_photo'):
            try:
                for msg_id in users[uid]['msg_photo']:
                    await bot.delete_message(callback.message.chat.id, msg_id)
            except Exception:
                pass
        if users[uid].get('msg_text'):
            try:
                await bot.delete_message(callback.message.chat.id, users[uid]['msg_text'])
            except Exception:
                pass
        print(index, users[uid]['categories'][index], '\n\n')
        text = users[uid]['categories'][index] + '\n\n' + users[uid]['captions'][index]
        print(text)
        msg_photo = await callback.message.answer_media_group(media_group)
        msg_text = await callback.message.answer(text, reply_markup=kb.pagination(index, len(users[uid]['captions']),
                                                                                  users[uid]['point']))

        users[uid]['msg_photo'] = [msg.message_id for msg in msg_photo] if msg_photo else []
        users[uid]['msg_text'] = msg_text.message_id

    elif callback.data == 'geo':
        lat, lon = locations[users[uid]['point']].split()
        await callback.message.answer_location(lat, lon)
    elif callback.data == 'reserve':
        await callback.message.answer('Вот ссылка для бронирования: \n'
                                      '*Ссылка*')
    elif callback.data == 'main_menu':
        if users.get(uid):
            if users[uid].get('msg_photo'):
                try:
                    for msg_id in users[uid]['msg_photo']:
                        await bot.delete_message(callback.message.chat.id, msg_id)
                except Exception:
                    pass
            if users[uid].get('msg_text'):
                try:
                    await bot.delete_message(callback.message.chat.id, users[uid]['msg_text'])
                except Exception:
                    pass
        await callback.message.answer('Вернуться к выбору отеля', reply_markup=kb.points)


async def main():
    await dp.start_polling(bot)
