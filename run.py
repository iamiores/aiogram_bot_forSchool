import asyncio
# import logging
from aiogram import Dispatcher

from bot import bot
from app.handlers import router

# logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Exit")
    finally:
        loop.close()

