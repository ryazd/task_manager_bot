from aiogram import Bot, Dispatcher
from handlers import routers
from db import create_tables, async_session
from dotenv import load_dotenv
import os
from notifier import check_deadline
import asyncio
from datetime import datetime


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


for router in routers:
    dp.include_router(router)


async def on_startup():
    await create_tables()
    asyncio.create_task(check_deadline(bot))
    print("БОТ ЗАПУЩЕН", datetime.now())


async def main():
    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())