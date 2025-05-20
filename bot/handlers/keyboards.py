from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_task_keyboard(task_id: int, is_done: bool):
    builder = InlineKeyboardBuilder()
    if not is_done:
        builder.button(
            text='Выполнить', 
            callback_data=f'complete_{task_id}'
        )
    builder.button(
        text='Удалить',
        callback_data=f'delete_{task_id}'
    )
    builder.adjust(1)
    return builder.as_markup()