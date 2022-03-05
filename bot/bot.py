import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import requests

from utils import convert_url

bot = Bot(token=os.getenv('TOKEN', None))
dp = Dispatcher(bot)


@dp.message_handler(
    regexp='((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([taobao]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
async def echo_message(msg: types.Message):
    await msg.reply(convert_url(msg.text))


if __name__ == '__main__':
    executor.start_polling(dp)

