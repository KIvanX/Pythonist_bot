
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import aiogram.utils.markdown as fmt
from bs4 import BeautifulSoup
from parsers import checkACMP
from random import randint
import requests
import traceback

bot = Bot(token="5144779060:AAGbUSrMa7nFVifzbXR7v97bfdWUOm7v-0I")

dp = Dispatcher(bot)
Menu = CallbackData("prefics", "act", "by_id")
varls = {'mes': []}


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):

    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Проверить", callback_data=Menu.new(act='check', by_id=0)),
               types.InlineKeyboardButton(text="Задача по номеру", callback_data=Menu.new(act='task', by_id=1)),
               types.InlineKeyboardButton(text="Рандомная номеру", callback_data=Menu.new(act='task', by_id=0))]
    keyboard.add(*buttons)

    await message.answer("Меню", reply_markup=keyboard)


@dp.errors_handler()
async def error_bot_blocked(_, exception):
    err = traceback.format_exc()
    print(err)
    print('Error main line:', err[err.find('main.py') + 15:].split(',')[0], '-', exception)
    await bot.send_message(1914011859, 'Что-то пошло не так 😦')
    return True


@dp.callback_query_handler(Menu.filter(act='task'))
async def send_random_value(call: types.CallbackQuery, callback_data: dict):
    if int(callback_data['by_id']) and varls.get('id') is None:
        await call.answer('Введи номер задачи')
        return 0

    for message_id in varls['mes']:
        await bot.delete_message(call.message.chat.id, message_id)
    varls['mes'] = []

    if not int(callback_data['by_id']):
        varls['id'] = randint(1, 1000)
    response = requests.get(f'https://acmp.ru/index.asp?main=task&id_task={varls["id"]}')
    response.encoding = 'cp1251'
    soup = BeautifulSoup(response.text, 'lxml')
    task_text = soup.find_all('p', class_='text')
    head = ' ' * 10 + soup.find_all('h1')[0].text
    head = fmt.quote_html(head + '   ' + soup.find_all('i')[0].text + '\n')
    text = head + '<i>' + fmt.quote_html(''.join([t.text for t in task_text])) + '</i>'
    varls['mes'].append((await call.message.answer(text, parse_mode="html")).message_id)
    await call.answer()


@dp.callback_query_handler(Menu.filter(act='check'))
async def send_random_value(call: types.CallbackQuery):
    if varls.get('id') is None:
        await call.answer('Нет задачи для проверки')
        return 0
    if varls.get('code') is None:
        await call.answer('Пришли решение задачи')
        return 0

    await call.answer('Идёт проверка...')
    await call.message.answer('Результат: ' + checkACMP(varls['id'], varls['code']))


@dp.message_handler(content_types=["text"])
async def cmd_test1(message: types.Message):
    if message.text.isdigit():
        varls['id'] = int(message.text)
    else:
        varls['code'] = message.text


print('Start')
if __name__ == "__main__":
    executor.start_polling(dp)

