import asyncio
import logging
from aiogram import Router, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loader import bot, db  # Bot va db import qilish
from aiogram import Bot

from states.state import Admin

logging.basicConfig(level=logging.INFO)

router = Router()
