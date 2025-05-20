from .callbacks import callback_router
from .messages import message_router
from .errors import error_router
from .commands import command_router


routers = [
    command_router,
    callback_router,
    error_router,
    message_router,
]