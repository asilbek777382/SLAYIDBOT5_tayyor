# import asyncio
# import os
# import re
# import logging
# import types
#
# import aiohttp
# from io import BytesIO
# import textwrap
# from aiogram.types import Message, FSInputFile, BufferedInputFile
# from aiogram.fsm.state import StatesGroup, State
# from pptx import Presentation
# from pptx.enum.text import PP_ALIGN
# from pptx.util import Inches, Pt
# from pptx.dml.color import RGBColor
# from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram import Router, F,types
# from loader import bot, db
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# logging.basicConfig(level=logging.INFO)
# # API keys
#
#
# router = Router()
# # Bot setup
#
# from pathlib import Path
# from aiogram import types
# from aiogram.exceptions import TelegramBadRequest
#
#
# @router.message(F.text == '/vid')
# async def send_tutorial_video(message: types.Message):
#     try:
#         # Specify the video file path
#         video_path = Path(r".\handlers\users\video.mp4")
#
#         # Verify the file exists and is accessible
#         if not video_path.exists():
#             await message.answer("❌ Video fayli topilmadi! Iltimos, texnik yordamga murojaat qiling.")
#             logging.error(f"Video file not found at: {video_path.absolute()}")
#             return
#
#         # Create FSInputFile with proper path
#         video = FSInputFile(video_path)
#
#         # Send video with caption
#         await bot.send_video(
#             chat_id=message.from_user.id,
#             video=video,
#             caption="✅ Ushbu videoda: Bot orqali slayd tayorlash to'liq tushuntirilgan.",
#             supports_streaming=True  # Allows for streaming playback
#         )
#
#         logging.info(f"Video sent successfully to {message.from_user.id}")
#
#     except TelegramBadRequest as e:
#         await message.answer("❌ Video yuborishda xatolik yuz berdi. Video formati yoki hajmi noto'g'ri.")
#         logging.error(f"Telegram API error: {e}")
#
#     except Exception as e:
#         await message.answer("❌ Video yuborishda kutilmagan xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
#         logging.error(f"Unexpected error sending video: {e}")
#
#
# # @router.message(F.text=='/my')
# # async def user_start(message: types.Message):
# #     text=(f"💰Balansingiz: \n"
# #           f"📚Taqdimotlaringiz soni:\n"
# #           f"💵To'lovlaringiz miqdori: \n"
# #
# #           )
# #     await message.answer(text)
#
#
#
# # @router.message(F.text=='/help')
# # async def user_start(message: types.Message):
# #     text=("❗️Sizga qanday yordam berishim mumkinligini to'liq matn ko'rinishida adminga yuboring!\n"
# #           "☎️ Admin: @slaydai_admin\n"
# #           "Chat - @slaydai_chat\n"
# #           "Bot yangilanishlari - @slaydai_news")
#
#
# class tolov(StatesGroup):
#     tanlov=State()
#     payme=State()
#     click=State()
#     karta=State()
#     chek=State()
#
# @router.message(F.text=='/bye')
# async def user_start(message: types.Message,state: FSMContext):
#     await state.set_state(tolov.tanlov)
#     text="Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇"
#     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme"),InlineKeyboardButton(text="🔵 CLICK", callback_data="click")],
#         [InlineKeyboardButton(text="💳 KARTA ORQALI", callback_data="karta")]])
#     m=await message.answer(text,reply_markup=inline_buttons)
#     await state.update_data({'m':m.message_id })
#
#
#
#
# @router.callback_query(F.data=='karta',tolov.tanlov)
# async def user_start(message: CallbackQuery,state: FSMContext):
#     await state.set_state(tolov.karta)
#     ol=await state.get_data()
#     m=ol.get('m')
#     await bot.delete_message(message.from_user.id, m)
#     text=(f"❗️Eng kamida 5000 so'm to'lov qiling, 5000 dan kam summalar bilan muammo bo'lishi mumkin.\n\n"
#           f"💳 8600 0417 7483 8644\n"
#           f"👤 Abdualiev Boburmirzo\n"
#           f"Ushbu karta raqamiga to'lov qiling va quyidagi tugmani bosing yoki /chek ni yuboring!")
#     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="📨 Chekni yuborish", callback_data="chek_yubor")],
#         [InlineKeyboardButton(text="🔙 Ortga", callback_data="ortga")]])
#
#     m=await message.message.answer(text,reply_markup=inline_buttons)
#     await state.update_data({'m':m.message_id })
#
#
# @router.callback_query(F.data=='ortga',tolov.karta)
# async def user_start(message: CallbackQuery,state: FSMContext):
#     ol=await state.get_data()
#     m=ol.get('m')
#     await bot.delete_message(message.from_user.id, m)
#     await state.set_state(tolov.tanlov)
#     text="Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇"
#     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme"),InlineKeyboardButton(text="🔵 CLICK", callback_data="click ")],
#         [InlineKeyboardButton(text="💳 KARTA ORQALI", callback_data="karta")]])
#     m=await message.message.answer(text,reply_markup=inline_buttons)
#     await state.update_data({'m':m.message_id })
#
#
# @router.callback_query(F.data=='chek_yubor',tolov.karta)
# async def user_start(message: CallbackQuery,state: FSMContext):
#     m=await message.message.answer("To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:")
#     await state.update_data({'m':m.message_id })
#     await state.set_state(tolov.chek)
#
# @router.message(F.text=="/chek")
# async def user_start(message: types.Message,state: FSMContext):
#     m=await message.answer("To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:")
#     await state.update_data({'m':m.message_id })
#     await state.set_state(tolov.chek)
#
# @router.message(
#     StateFilter(tolov.chek),
#     F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'}))
# async def bot_start(message: types.Message, state: FSMContext):
#     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Tastiqlash ✅", callback_data=f"tashtiqlash_chek::{message.from_user.id}")]])
#
#     try:
#         await bot.copy_message(
#             chat_id=5528965178,
#             from_chat_id=message.chat.id,
#             message_id=message.message_id,
#             caption="Tolovni tastiqlang:",
#             reply_markup=inline_buttons
#         )
#         await message.answer('Tolovingizni tastiqlashlarini kuting.⏳')
#     except Exception as e:
#         print(f"❌ {5528965178} ga yuborilmadi.{e}")
#
# class tolov_tastiq(StatesGroup):
#         tastiq = State()
#
# @router.callback_query(F.data.startswith("tashtiqlash_chek"))
# async def handle_bg_selection(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_reply_markup(reply_markup=None)
#     await state.set_state(tolov_tastiq.tastiq)
#     tg_user=callback.data.rsplit("::")[1]
#     await state.update_data({"tg_user":tg_user})
#     await callback.message.answer("Tolov summasini kiriting:")
#
#
#
# @router.message(tolov_tastiq.tastiq)
# async def handle_bg_selection(callback: types.Message, state: FSMContext):
#         if not callback.text.isdigit():
#             await callback.answer("❌ Iltimos, faqat raqam kiriting!")
#             await state.set_state(tolov_tastiq.tastiq)
#             return
#
#         ol=await state.get_data()
#         tg_user=ol.get('tg_user')
#         pul=db.select_user(tg_user=tg_user)
#         qosh=int(pul[3])+int(callback.text)
#         db.update_user_balans(tg_user=tg_user,balans=qosh)
#         await callback.answer("Tolov muvaffaqiyatli tarizda tastiqlandi.✅\n\n"
#                                                     f'Tolov summasi: {callback.text}')
#         await bot.send_message(chat_id=tg_user,text=f'Tolov muvaffaqiyatli tarizda tastiqlandi.✅\n\n'
#                                                     f'Tolov summasi: {callback.text}')
#         await state.clear()