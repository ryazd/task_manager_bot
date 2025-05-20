from aiogram import Router, types

message_router = Router()

@message_router.message()
async def handle_unknown_message(message: types.Message):
    await message.answer(
        "🤖 Я не понимаю ваше сообщение. Используйте команды:\n"
        "/add - добавить задачу\n"
        "/addMany - добавить задачу\n"
        "/list - список задач"
    )