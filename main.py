import requests
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.utils import executor
from typing import Dict
from metod import *
import traceback
import random
import signal
import pickle


bot = Bot(token="5144779060:AAGbUSrMa7nFVifzbXR7v97bfdWUOm7v-0I")
cb = CallbackData("prefics", "act", "p")
dp = Dispatcher(bot)

users: Dict[int, User]
tasks: list[Task]
users, tasks = load_all()


# ОСТАНОВКА
def handler_stop_signals(_, __):
    with open('Pythonist_database.pkl', 'wb') as f:
        pickle.dump([users, tasks], f)
    print('Данные сохранены')


# СТАРТ
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):

    if users.get(message.chat.id) is None:
        users[message.chat.id] = User(message.chat.id)
    user = users[message.chat.id]

    keyboard = types.InlineKeyboardMarkup()
    levels = ["Новичок", "Любитель", "Продвинутый", "Эксперт", "Гуру"]
    buttons = []
    for i, level in enumerate(levels):
        buttons.append(types.InlineKeyboardButton(text=level, callback_data=cb.new(act='level', p=i)))
    keyboard.add(*buttons)

    user.dlt = (await message.answer("Привет! Я - бот Питонист, помогу тебе в обучении языку Python. "
                                     "Для начала выбери свой уровень программирования",
                                     reply_markup=keyboard)).message_id


# МЕНЮ
@dp.callback_query_handler(cb.filter(act='menu'))
async def menu(call: types.CallbackQuery):
    user = users[call.message.chat.id]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Решение задач', callback_data=cb.new(act='task', p='')))
    keyboard.add(types.InlineKeyboardButton(text='Что выведет программа', callback_data=cb.new(act='', p='')))
    keyboard.add(types.InlineKeyboardButton(text='Уроки по темам', callback_data=cb.new(act='', p='')))
    keyboard.add(types.InlineKeyboardButton(text='Уроки по библиотекам', callback_data=cb.new(act='', p='')))

    await bot.delete_message(call.message.chat.id, user.dlt)
    user.dlt = (await call.message.answer("Меню", reply_markup=keyboard)).message_id


# ФУНКЦИЯ В РАЗРАБОТКЕ
@dp.callback_query_handler(cb.filter(act=''))
async def none_page(message):
    await message.answer("Функция в разработке")


# ВЫБОР УРОВНЯ
@dp.callback_query_handler(cb.filter(act='level'))
async def set_level(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    user.level = int(callback_data['p'])
    await menu(call)


# ОТЛОВ ОШИБОК
@dp.errors_handler()
async def errors(update, exception):

    err = traceback.format_exc()
    print('Error main line:', err[err.find('main.py') + 15:].split(',')[0], '-', exception)
    if exception != 'Message to delete not found':
        await bot.send_message(update.callback_query.message.chat.id, 'Что-то пошло не так 😦')
    users[update.callback_query.message.chat.id].varls['mes'] = []


# ВЫВОД ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='task'))
async def send_task(call: types.CallbackQuery):
    user = users[call.message.chat.id]

    inds = [i for i, t in enumerate(tasks) if t.level == user.level]
    if inds:
        ind = random.choice(inds)
        task = tasks[ind]
        text = task.name + '\n' + task.text + '\nПримеры:\n' + '\n'.join([e[0] + ' -> ' + e[1] for e in task.exemples])

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Проверка", callback_data=cb.new(act='check', p=ind)))
        if task.answer is not None:
            keyboard.add(types.InlineKeyboardButton(text="Решение", callback_data=cb.new(act='answer', p=ind)))
        keyboard.add(types.InlineKeyboardButton(text="Следующая задача", callback_data=cb.new(act='task', p='')))
        keyboard.add(types.InlineKeyboardButton(text="Меню", callback_data=cb.new(act='menu', p='')))

        await bot.delete_message(call.message.chat.id, user.dlt)
        user.dlt = (await call.message.answer(text, reply_markup=keyboard)).message_id
    else:
        await call.answer('Подходящих задач не найдено')


# ПРОВЕРКА ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='check'))
async def check_task(call: types.CallbackQuery, callback_data: dict):
    # user = users[call.message.chat.id]
    # if user.varls.get('code') is None:
    #     await call.answer('Пришли решение задачи текстом или файлом')
    #     return 0

    await call.answer('Функция временно недоступна')
    # await call.answer('Идёт проверка...')
    # link = tasks[int(callback_data['p'])].link
    # res = parser_ACMP.check_task(int(link[link.rfind('=')+1:]))
    #
    # await call.message.answer(f'Результат: {res}')



# ВЫВОД ОТВЕТА НА ЗАДАЧУ
@dp.callback_query_handler(cb.filter(act='answer'))
async def send_answer(call: types.CallbackQuery, callback_data: dict):

    response = requests.get(tasks[int(callback_data['p'])].answer)
    response.encoding = 'cp1251'

    with open('answer.txt', 'w') as f:
        f.write(response.text)

    with open('answer.txt', 'rb') as f:
        await bot.send_document(call.message.chat.id, document=f,
                                caption=f'Решение задачи {tasks[int(callback_data["p"])].name}')
    await call.answer()


# ОБРАБОТКА ТЕКСТА
@dp.message_handler(content_types=["text"])
async def get_text(message: types.Message):
    user = users[message.chat.id]
    user.varls['code'] = True
    with open('input.py', 'w') as f:
        f.write(message.text)


# ОБРАБОТКА ФАЙЛА
@dp.message_handler(content_types=["document"])
async def get_text(message: types.Message):
    user = users[message.chat.id]
    user.varls['code'] = True
    with open('input.py', 'wb') as f:
        f.write((await message.document.download()).read())

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

print('Start')
if __name__ == "__main__":
    executor.start_polling(dp)
