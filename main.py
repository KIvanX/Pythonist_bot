import requests
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.utils import executor
from typing import Dict
from temp import parser_ACMP
from metod import *
import traceback
import random
import signal
import pickle

with open('token.key') as f:
    bot = Bot(token=f.read())
cb = CallbackData("prefics", "act", "p")
dp = Dispatcher(bot)

users: Dict[int, User]
tasks: list[Task]
lessons: Dict[int, Lesson]
users, tasks, lessons = load_all()


# ОСТАНОВКА
def handler_stop_signals(_, __):
    with open('Pythonist_database.pkl', 'wb') as f:
        pickle.dump([users, tasks, lessons], f)


# УДАЛЕНИЕ СТАРОГО СООБЩЕНИЯ
async def del_message(message_id, chat_id):
    try:
        if message_id is not None:
            await bot.delete_message(chat_id, message_id)
    except:
        pass


# СТАРТ
@dp.message_handler(commands="start")
async def func_start(message: types.Message):
    if users.get(message.chat.id) is None:
        users[message.chat.id] = User(message.chat.id)
    user = users[message.chat.id]

    keyboard = types.InlineKeyboardMarkup()
    levels = ["🥉 Новичок", "🥈 Любитель", "🥇Продвинутый", "🎖Эксперт", "🏆Гуру"]
    buttons = []
    for i, level in enumerate(levels):
        buttons.append(types.InlineKeyboardButton(text=level, callback_data=cb.new(act='level', p=i)))
    keyboard.add(*buttons)

    user.dlt = (await message.answer("🤖 Привет! Я - бот Питонист, \n"
                                     "помогу тебе в обучении языку 🐍Python. \n\n"
                                     "💪 Для начала выбери свой уровень программирования:",
                                     reply_markup=keyboard)).message_id


# АДМИНИСТРАТОР
@dp.message_handler(commands="kUtx0d")
async def admin(message: types.Message):
    user = users[message.chat.id]
    if not user.admin:
        user.admin = True
        await message.answer('😎 Ты получил права администратора')
    else:
        user.admin = False
        await message.answer('🙂 Ты отказался от прав администратора')


# МЕНЮ
@dp.callback_query_handler(cb.filter(act='menu'))
async def func_menu(call: types.CallbackQuery):
    user = users[call.message.chat.id]

    keyboard = types.InlineKeyboardMarkup()
    but = [types.InlineKeyboardButton(text='📝 Решение задач', callback_data=cb.new(act='task', p='')),
           types.InlineKeyboardButton(text='🔎 Что выведет программа', callback_data=cb.new(act='result', p='')),
           types.InlineKeyboardButton(text='📚 Уроки по темам', callback_data=cb.new(act='lessons', p='topic')),
           types.InlineKeyboardButton(text='📜 Уроки по библиотекам', callback_data=cb.new(act='lessons', p='lib'))]
    for b in but:
        keyboard.row(b)

    await del_message(user.dlt, call.message.chat.id)
    user.dlt = (await call.message.answer("Меню", reply_markup=keyboard)).message_id
    user.varls = {}


# ВЫБОР УРОВНЯ
@dp.callback_query_handler(cb.filter(act='level'))
async def func_level(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    user.level = int(callback_data['p'])
    await func_menu(call)


# ОТЛОВ ОШИБОК
@dp.errors_handler()
async def errors(update, exception):
    err = traceback.format_exc()
    print('Error main line:', err[err.find('main.py') + 15:].split(',')[0], '-', exception)
    if users[update.callback_query.message.chat.id].user_id == 1914011859:
        await bot.send_message(update.callback_query.message.chat.id, 'Что-то пошло не так 😦')
    users[update.callback_query.message.chat.id].varls['mes'] = []


# ВЫВОД ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='task'))
async def func_task(call: types.CallbackQuery):
    user = users[call.message.chat.id]
    user.varls['location'] = 'task'
    ind = random.choice([i for i, t in enumerate(tasks) if user.level == t.level])
    if user.varls.get('task') is not None:
        ind = int(user.varls['task'])
        user.varls['task'] = None

    task = tasks[ind]
    exemples = "\n\n".join(["Input:\n" + e[0] + "\nOutput:\n" + e[1] for e in task.exemples])
    text = f'({ind}) {task.name}\n\n{task.text}\nПримеры:\n{exemples}'

    keyboard = types.InlineKeyboardMarkup()
    but = [types.InlineKeyboardButton(text="❓ Проверка", callback_data=cb.new(act='check', p=ind)),
           types.InlineKeyboardButton(text="✳️ Решение", callback_data=cb.new(act='answer', p=ind))]
    buttons = [types.InlineKeyboardButton(text="🔢 Меню", callback_data=cb.new(act='menu', p='')),
               types.InlineKeyboardButton(text="➡️ Дальше", callback_data=cb.new(act='task', p=''))]

    if task.link is None or ind in user.saw_ans:
        but.pop(0)
    if task.answer is None:
        but.pop(0 if len(but) == 1 else 1)
    if but:
        keyboard.add(*but)
    keyboard.add(*buttons)

    await del_message(user.dlt, call.message.chat.id)
    user.dlt = (await call.message.answer(text, reply_markup=keyboard)).message_id


# ЧТО ВЕРНЁТ ПРОГРАММА
@dp.callback_query_handler(cb.filter(act='result'))
async def func_result(call: types.CallbackQuery):
    user = users[call.message.chat.id]
    user.varls['location'] = 'result'

    ind = random.choice([i for i, t in enumerate(tasks) if t.level == user.level and t.answer is not None])
    task = tasks[ind]
    response = requests.get(task.answer)
    response.encoding = 'utf-8'

    with open('temp/answer.txt', 'w', encoding='utf-8') as f:
        f.write(response.text[response.text.find('\ndef '):])

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text="❓ Проверка", callback_data=cb.new(act='checkRes', p=ind)),
                   types.InlineKeyboardButton(text="✳️ Решение", callback_data=cb.new(act='answerRes', p=ind))])
    keyboard.add(*[types.InlineKeyboardButton(text="🔢  Меню", callback_data=cb.new(act='menu', p='')),
                   types.InlineKeyboardButton(text="➡️ Дальше", callback_data=cb.new(act='result', p=''))])

    await del_message(user.dlt, call.message.chat.id)
    with open('temp/answer.txt', 'rb') as f:
        user.dlt = (await bot.send_document(call.message.chat.id,
                                            document=f,
                                            caption=f'Что вернёт эта программа на следущие данные:\n'
                                                    f'{task.exemples[0][0]}',
                                            reply_markup=keyboard)).message_id


# ПРОВЕРКА РЕШЕНИЯ ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='check'))
async def func_check(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    if user.varls.get('code') is None:
        await call.answer('Пришли решение задачи текстом или файлом')
        return 0

    if user.varls.get('code') is None:
        await call.answer('Ты уже посмотрел решение')
        return 0

    await call.answer('Идёт проверка...')
    link = tasks[int(callback_data['p'])].link
    res = parser_ACMP.check_task(int(link[link.rfind('=') + 1:]))

    await call.message.answer(f'Результат: {res}')


# СПИСОК ЛЕКЦИЙ
@dp.callback_query_handler(cb.filter(act='lessons'))
async def func_lessons(call: types.CallbackQuery, callback_data: dict):
    les_about = callback_data['p']
    user = users[call.message.chat.id]
    user.varls['location'] = 'lessons'
    les_inds = [key for key in lessons.keys() if lessons[key].about == les_about]
    keyboard = types.InlineKeyboardMarkup()
    for key in les_inds:
        keyboard.row(types.InlineKeyboardButton(text=lessons[key].name, callback_data=cb.new(act='lesson',
                                                                                             p=str(key) + ' 0')))
    but = [types.InlineKeyboardButton(text='🔢 Меню', callback_data=cb.new(act='menu', p='')),
           types.InlineKeyboardButton(text='🆕 Добавить', callback_data=cb.new(act='add_les', p=les_about))]
    if not user.admin:
        but.pop(0)
    keyboard.add(*but)

    await del_message(user.dlt, call.message.chat.id)
    by = 'по теме' if les_about == 'topic' else 'по библиотеке'
    user.dlt = (await call.message.answer('Выбери лекцию ' + by, reply_markup=keyboard)).message_id


# ДОБАВИТЬ ЛЕКЦИЮ
@dp.callback_query_handler(cb.filter(act='add_les'))
async def func_add_les(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    if user.varls.get('lesson') is None:
        await call.answer('Пришли лекцию в виде файла(Пример имени: "Строки.txt")')
        return 0

    with open('temp/lesson.txt', 'r', encoding='utf-8') as f:
        key = random.randint(100000, 999999)
        while key in lessons.keys():
            key = random.randint(100000, 999999)
        lessons[key] = Lesson(user.varls['lesson'], callback_data['p'], f.read())

    await call.answer('✅ Лекция добавлена')
    await func_lessons(call, callback_data)


# УДАЛИТЬ ЛЕКЦИЮ
@dp.callback_query_handler(cb.filter(act='del_les'))
async def func_del_les(call: types.CallbackQuery, callback_data: dict):
    about = lessons[int(callback_data['p'])].about
    del lessons[int(callback_data['p'])]
    await call.answer('❎ Лекция удалена')
    await func_lessons(call, {'p': about})


# ЛЕКЦИЯ
@dp.callback_query_handler(cb.filter(act='lesson'))
async def func_lesson(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    ind = int(callback_data['p'].split()[0])
    page = int(callback_data['p'].split()[1])

    keyboard = types.InlineKeyboardMarkup()
    but = []
    if page > 0:
        but.append(types.InlineKeyboardButton(text='⬅️',
                                              callback_data=cb.new(act='lesson', p=f'{ind} {page - 1}')))
    if page < len(lessons[ind]):
        but.append(types.InlineKeyboardButton(text='➡️',
                                              callback_data=cb.new(act='lesson', p=f'{ind} {page + 1}')))
    keyboard.row(*but)

    but = [types.InlineKeyboardButton(text='🔙 Назад', callback_data=cb.new(act='lessons', p=lessons[ind].about)),
           types.InlineKeyboardButton(text='❌ Удалить', callback_data=cb.new(act='del_les', p=ind))]

    if not user.admin:
        but.pop(0)

    keyboard.add(*but)

    await del_message(user.dlt, call.message.chat.id)
    user.dlt = (await call.message.answer(lessons[ind].page(page), reply_markup=keyboard)).message_id


# ПРОВЕРКА ВЫВОДА ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='checkRes'))
async def func_checkRes(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    if user.varls.get('text') is None:
        await call.answer('Пришли текстом то, что вернёт программа')
        return 0

    task = tasks[int(callback_data['p'])]

    if task.exemples[0][1] == user.varls.get('text'):
        await call.message.answer('Это правильный ответ!')
    else:
        await call.message.answer('Программа вернёт что-то другое')


# ВЫВОД РЕШЕНИЯ ЗАДАЧИ
@dp.callback_query_handler(cb.filter(act='answer'))
async def func_answer(call: types.CallbackQuery, callback_data: dict):
    user = users[call.message.chat.id]
    user.saw_ans.append(int(callback_data['p']))

    response = requests.get(tasks[int(callback_data['p'])].answer)
    response.encoding = 'utf-8'

    with open('temp/answer.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

    with open('temp/answer.txt', 'rb') as f:
        await bot.send_document(call.message.chat.id, document=f,
                                caption=f'Решение задачи "{tasks[int(callback_data["p"])].name}"')
    await call.answer()


# ВЫВОД ОТВЕТА НА ВХОДНЫЕ ДАННЫЕ ПРОГРАММЫ
@dp.callback_query_handler(cb.filter(act='answerRes'))
async def func_answerRes(call: types.CallbackQuery, callback_data: dict):
    task = tasks[int(callback_data['p'])]
    await call.message.answer('Правильный ответ:\n' + task.exemples[0][1])


# ОБРАБОТКА ТЕКСТА
@dp.message_handler(content_types=["text"])
async def func_text(message: types.Message):
    user = users[message.chat.id]
    if user.varls.get('location') == 'task':
        user.varls['code'] = True
        with open('temp/input.py', 'w') as f:
            f.write(message.text)

    if user.varls.get('location') == 'result':
        user.varls['text'] = message.text

    if message.text.isdigit() and 0 < int(message.text) < 1499:
        user.varls['task'] = message.text


# ОБРАБОТКА ФАЙЛА
@dp.message_handler(content_types=["document"])
async def func_document(message: types.Message):
    user = users[message.chat.id]
    if user.varls.get('location') == 'task':
        user.varls['code'] = True
        text = (await bot.download_file((await bot.get_file(message.document.file_id)).file_path)).read()
        with open('temp/input.py', 'wb') as f:
            f.write(text)

    if user.varls.get('location') == 'result':
        user.varls['text'] = message.text


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

print('Start')
if __name__ == "__main__":
    executor.start_polling(dp)
