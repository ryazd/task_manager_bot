from aiogram import Router
from aiogram.types import ErrorEvent

error_router = Router()

@error_router.error()
async def handle_errors(event: ErrorEvent):
    try:
        await event.update.message.answer(
            "⚠️ Произошла ошибка. Попробуйте позже или обратитесь к разработчику."
        )
    except:
        print('Ошибка')
    print(f"Ошибка: {event.exception}")