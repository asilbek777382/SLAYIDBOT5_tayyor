from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="✅Botni ishga tushurish"),
            BotCommand(command="bye", description="💰Tolov orqali balansni toldirish"),
            BotCommand(command="check", description="🪪To'lovingizni tastiqlovchi skrenshotni yuboring"),
            BotCommand(command="help", description="🆘Yordam kerak bo'lsa"),

            # Qo‘shimcha komandalar...
        ]
    )
