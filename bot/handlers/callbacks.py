from aiogram import Router, types, F
from db import Task, async_session
from .keyboards import get_task_keyboard
from aiogram.utils.keyboard import InlineKeyboardMarkup
from .commands import cmd_list_tasks


callback_router = Router()


answers = {
    'complete': {
        'message': "Задача выполнена!",
        'status': '✅',
        'rev_text': '❌ Переделать',
        'rev_data': 'uncomplete'
    },
    'delete': {
        'message': "Задача удалена!",
    },
    'uncomplete': {
        'message': "Задача снова активна!",
        'status': '❌',
        'rev_text': '✅ Выполнить',
        'rev_data': 'complete'
    }
}



async def edit_task(callback: types.CallbackQuery, action: str):
    task_id = int(callback.data.split("_")[1])
    
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if task:
            if task.user_id != callback.from_user.id:
                await callback.answer('Не ваша задача!', show_alert=True)
                return False
            if action == 'complete':
                task.is_done = True
            elif action == 'uncomplete':
                task.is_done = False
            elif action == 'delete':
                await session.delete(task)
            else:
                raise ValueError(f'Неизвестное действие: {action}')
            await session.commit()
            await callback.answer(answers[action]['message'])
            return True
        else:
            await callback.answer('Нет такой задачи!', show_alert=True)
            return False


@callback_router.callback_query(F.data.startswith("complete_"))
async def complete_task(callback: types.CallbackQuery):
    edit = await edit_task(callback, 'complete')
    if not edit:
        return
    page = int(callback.data.split('_')[2])
    user_id = callback.from_user.id
    await cmd_list_tasks(callback.message, user_id=user_id, page=page)
    


@callback_router.callback_query(F.data.startswith("uncomplete_"))
async def complete_task(callback: types.CallbackQuery):
    edit = await edit_task(callback, 'uncomplete')
    if not edit:
        return
    page = int(callback.data.split('_')[2])
    user_id = callback.from_user.id
    await cmd_list_tasks(callback.message, user_id=user_id, page=page)


@callback_router.callback_query(F.data.startswith("delete_"))
async def delete_task(callback: types.CallbackQuery):
    edit = await edit_task(callback, 'delete')
    if not edit:
        return
    page = int(callback.data.split('_')[2])
    user_id = callback.from_user.id
    await cmd_list_tasks(callback.message, user_id=user_id, page=page)



@callback_router.callback_query(F.data.startswith('page_'))
async def change_page(callback: types.CallbackQuery):
    page = int(callback.data.split('_')[1])
    user_id = callback.from_user.id
    await cmd_list_tasks(callback.message, user_id=user_id, page=page)