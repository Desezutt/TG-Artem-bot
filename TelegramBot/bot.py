import os
import asyncio
import re
from random import *
from time import sleep
from urllib.error import HTTPError
import datetime

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from urllib.request import urlopen, Request
from bs4 import *
from dotenv import load_dotenv

from handlers import callback,commands

FOXES_DIR_LINK = "https://wohlsoft.ru/images/foxybot/foxes/"
bot = Bot(token='7852413770:AAGvS6GCvcbadVS6OsxvXIuwKGW98HjNZA8')

def http_get(url: str):
    request = Request(url)
    try:
        with urlopen(request) as response:
            data = response.read()
            return {
                "data": data,
                "status": response.status,
                "url": response.url
            }
    except HTTPError as error:
        return {
            "status": error.code,
        }


def get_foxes():
    data = http_get(FOXES_DIR_LINK)["data"]
    parsed_html = BeautifulSoup(data)
    links = []
    for link in parsed_html.body.find_all('td', attrs={'class':'indexcolname'})[1:]:
        links.append(FOXES_DIR_LINK + link.a.get("href"))
    return links


dp = Dispatcher()

async def main():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)

    @dp.message(Command('foxpic'))
    async def foxpic(message: types.Message):
        print(f'[{datetime.datetime.now()}] foxpic')
        await bot.send_photo(chat_id=message.chat.id,
                             photo=choice(get_foxes()))
        print(f'[{datetime.datetime.now()}] send photo')

    @dp.message(CommandStart())
    async def cmd_start(message: Message):
        print(f'[{datetime.datetime.now()}] /start')
        await message.answer('Hi!')
        print(f'[{datetime.datetime.now()}] ответ \'Hi!\'')

    @dp.message(Command('help'))
    async def fiffif(message: Message):
        await message.reply("restart...")
        print(f"[{datetime.datetime.now()}] restart...")
        sleep(5)
        await message.reply("done")
        print(f'[{datetime.datetime.now()}] done')
    #этому куску кода есть адекватное объявление!!!


    @dp.message(Command('1or2'))
    async def fiffif(message: Message):
        print(f"[{datetime.datetime.now()}] 1 or 2")
        fif = str(randint(1, 2))
        await message.reply(fif)
        print(f'[{datetime.datetime.now()}] ответ {fif}')


    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        dp.include_router(commands.router)
        dp.include_router(callback.router)
        print(f"[{datetime.datetime.now()}] Bot Start")
        await dp.start_polling(bot)
        await bot.session.close()
    except Exception as ex:
        print(f"There is an Exeption: {ex}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'[{datetime.datetime.now()}] Exit')