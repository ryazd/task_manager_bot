import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from db import async_session, Task
from sqlalchemy import select, func


async def check_deadline(bot: Bot):
    while True:
        async with async_session() as session:
            now = datetime.now()
            soon = now + timedelta(hours=1)
            tasks = await session.execute(
                select(Task)
                .where(Task.dead_line.between(now, soon), Task.is_done==False)
            )
            for task in tasks.scalars().all():
                await bot.send_message(
                    task.user_id, 
                    f"Скоро дедлайн!\nЗадача: {task.text}\nДо: {task.dead_line.strftime('%H:%M %d.%m')}"
                )
            await asyncio.sleep(30*60)