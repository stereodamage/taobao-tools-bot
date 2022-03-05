import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.utils.executor import start_webhook

from utils import convert_url


WEBHOOK_HOST = ''
WEBHOOK_PATH = ''
WEBHOOK_URL = ''
PROXY = 'http://proxy.server:3128'

bot = Bot(token=os.getenv('TOKEN', ''), proxy=PROXY)
dp = Dispatcher(bot)


@dp.message_handler(
    regexp='((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([taobao]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
async def echo_message(msg: types.Message):
    await msg.reply(convert_url(msg.text))


async def on_startup(dp):
    logging.warning('Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.storage.close()
    await dp.storage.wait_closed()


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(dispatcher=dp,
                  webhook_path=WEBHOOK_PATH,
                  skip_updates=True,
                  on_startup=on_startup,
                  on_shutdown=on_shutdown,
                  host='0.0.0.0',
                  port=3001,
                  )
    webhook = await bot.get_webhook_info()

    # If URL is bad
    if webhook.url != WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


if __name__ == '__main__':
    main()

