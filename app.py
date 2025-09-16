import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from loader import bot  # loader.py dan botni import qiling
from handlers import users
from utils.set_bot_commands import set_default_commands


dp = Dispatcher()

async def on_startup():
    await set_default_commands(bot)  # Botni boshlashda kerakli komandalarni sozlash

async def main():
    dp.include_router(users.router)  # Faqat bitta router, lekin u ichida barcha kerakli handlerlar bor!
    await on_startup()  # Botni ishga tushirishdan oldin komandalarni sozlash
    await dp.start_polling(bot)  # Pollingni boshlash

if __name__ == "__main__":
    asyncio.run(main())
