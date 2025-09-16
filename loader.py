from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties  # Import DefaultBotProperties
from data import config  # token shu faylda bo‘lishi kerak

# Botni yaratishda DefaultBotProperties orqali parse_mode belgilash
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

from utils.db_api.sqlite import Database
db = Database(path_to_db="db.sqlite3")
