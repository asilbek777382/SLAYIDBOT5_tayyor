from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta
from typing import Callable, Dict, Any, Awaitable


class SimpleThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        super().__init__()
        self.rate_limit = rate_limit
        self.users_time: Dict[int, datetime] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        now = datetime.now()
        last_time = self.users_time.get(user_id)

        if last_time and now - last_time < timedelta(seconds=self.rate_limit):
            await event.answer("❗ Juda tez yuboryapsiz, biroz kuting.")
            return  # Aiogram 3.x da CancelHandler ishlatilmaydi, shunchaki `return` qilinadi

        self.users_time[user_id] = now
        return await handler(event, data)
