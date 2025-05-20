from aiogram import Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Command
from sqlalchemy import select, func
from db import Task, async_session
from .keyboards import get_task_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import math
from typing import Union
from aiogram.fsm.context import FSMContext
from datetime import datetime


command_router = Router()


class AddTaskState(StatesGroup):
    waiting_for_text = State()
    waiting_for_deadline = State()


@command_router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("""Я бот для управления задачами. Доступные команды:
/add - добавить задачу
/list - список задач
""")


@command_router.message(Command('add'))
async def cmd_add_task(message: types.Message, state: FSMContext):
    await message.answer('Введите текст задачи:')
    await state.set_state(AddTaskState.waiting_for_text)


@command_router.message(AddTaskState.waiting_for_text)
async def process_task_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Укажите дедлайн (или нажмите /skip): \nФормат: ДД.ММ.ГГГГ ЧЧ:ММ\nПример: 25.12.2025 10:00")
    await state.set_state(AddTaskState.waiting_for_deadline)


@command_router.message(AddTaskState.waiting_for_deadline, Command('skip'))
async def skip_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await create_task(message.from_user.id, data['text'], None)
    await message.answer("✅ Задача добавлена без дедлайна")


@command_router.message(AddTaskState.waiting_for_deadline)
async def process_task_deadline(message: types.Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        data = await state.get_data()
        await create_task(message.from_user.id, data['text'], deadline)
        await message.answer(f"✅ Задача добавлена, дедлайн: {deadline.strftime('%d.%m.%Y %H:%M')}")
    except ValueError:
        await message.answer('❌ Неверный формат даты. Попробуйте снова.')
    await state.clear()


async def create_task(user_id: int, text: str, deadline: Union[datetime, None] = None):
    async with async_session() as session:
        task = Task(
            user_id=user_id,
            text=text,
            dead_line=deadline
        )
        session.add(task)
        await session.commit()


@command_router.message(Command('list'))
async def cmd_list_tasks(message: types.Message, user_id: Union[int, None] = None,page: int = 1, limit: int = 5):
    async with async_session() as session:
        total_tasks = await session.scalar(
            select(func.count(Task.id))\
            .where(Task.user_id==(message.from_user.id if not user_id else user_id))
        )
        if page > 1 and (page - 1) * limit >= total_tasks:
            page -= 1
        query = select(Task)\
            .where(Task.user_id==(message.from_user.id if not user_id else user_id))\
            .order_by(Task.id)\
            .offset((page-1)*limit)\
            .limit(limit)
        result = await session.execute(query)
        tasks = result.scalars().all()

    if not tasks:
        if user_id:
            await message.edit_text('Ваш список задач пуст.')    
        else:
            await message.answer('Ваш список задач пуст.')
        return
    
    now = datetime.now()
    tasks_text = "📋 Ваши задачи:\n\n" + "\n".join(
        f"{'✅' if task.is_done else '❌' if not task.dead_line or now < task.dead_line else '🔴'} {i+1 + (page-1)*limit}. {task.text} {task.dead_line if task.dead_line else ''}"
        for i, task in enumerate(tasks)
    )
    
    builder = InlineKeyboardBuilder()
    for i, task in enumerate(tasks):
        if not task.is_done:
            builder.button(
                text=f"✅ Выполнить {i+1 + (page-1)*limit}", 
                callback_data=f"complete_{task.id}_{page}"
            )
        else:
            builder.button(
                text=f"❌ Переделать {i+1 + (page-1)*limit}", 
                callback_data=f"uncomplete_{task.id}_{page}"
            )
        builder.button(
            text=f"❌ Удалить {i+1 + (page-1)*limit}", 
            callback_data=f"delete_{task.id}_{page}"
        )
    
    # Кнопки пагинации
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text="◀ Назад", callback_data=f"page_{page - 1}")
        )
    if (page * limit) < total_tasks:
        pagination_buttons.append(
            InlineKeyboardButton(text="Вперёд ▶", callback_data=f"page_{page + 1}")
        )
    
    if pagination_buttons:
        builder.row(*pagination_buttons)
    
    builder.adjust(2)
    if user_id:
        await message.edit_text(
            f"{tasks_text}\n\nСтраница {page}/{math.ceil(total_tasks / limit)}",
            reply_markup=builder.as_markup()
        )
    else:
        await message.answer(
            f"{tasks_text}\n\nСтраница {page}/{math.ceil(total_tasks / limit)}",
            reply_markup=builder.as_markup()
        )

