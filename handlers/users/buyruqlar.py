import asyncio
import os
import re
import logging
import types

import aiohttp
from io import BytesIO
import textwrap
from aiogram.types import Message, FSInputFile, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from loader import bot, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logging.basicConfig(level=logging.INFO)
# API keys


router = Router()
# Bot setup

from pathlib import Path
from aiogram import types
from aiogram.exceptions import TelegramBadRequest


@router.message(F.text == '/vid')
async def send_tutorial_video(message: types.Message):
    ol = db.select_user(tg_user=message.from_user.id)
    print(ol, 'olllllllllllll')
    til = ol[4]
    if til == 'uz':
        try:
            # Specify the video file path
            video_path = Path(r"./handlers/users/video.mp4")

            # Verify the file exists and is accessible
            if not video_path.exists():
                await message.answer("❌ Video fayli topilmadi! Iltimos, texnik yordamga murojaat qiling.")
                logging.error(f"Video file not found at: {video_path.absolute()}")
                return

            # Create FSInputFile with proper path
            video = FSInputFile(video_path)

            # Send video with caption
            await bot.send_video(
                chat_id=message.from_user.id,
                video=video,
                caption="✅ Ushbu videoda: Bot orqali slayd tayorlash to'liq tushuntirilgan.",
                supports_streaming=True  # Allows for streaming playback
            )

            logging.info(f"Video sent successfully to {message.from_user.id}")

        except TelegramBadRequest as e:
            await message.answer("❌ Video yuborishda xatolik yuz berdi. Video formati yoki hajmi noto'g'ri.")
            logging.error(f"Telegram API error: {e}")

        except Exception as e:
            await message.answer(
                "❌ Video yuborishda kutilmagan xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
            logging.error(f"Unexpected error sending video: {e}")
    if til == "ru":
        await message.answer('salom')
        try:
            # Fayl manzili
            video_path = Path("./handlers/users/video.mp4")

            # Fayl mavjudligini tekshirish
            if not video_path.is_file():
                await message.answer("❌ Видеофайл не найден! Обратитесь в службу технической поддержки.")
                logging.error(f"Video file not found: {video_path.resolve()}")
                return

            # FSInputFile orqali yuklash
            video = FSInputFile(video_path)

            # Video yuborish
            await bot.send_video(
                chat_id=message.chat.id,  # message.from_user.id ham ishlaydi
                video=video,
                caption="✅ В этом видео подробно объясняется создание слайда с помощью бота.",
                supports_streaming=True
            )

            logging.info(f"Video sent successfully to {message.from_user.id}")

        except TelegramBadRequest as e:
            await message.answer(
                "❌ Ошибка при отправке видео. Возможно, неправильный формат или слишком большой размер.")
            logging.error(f"Telegram API error: {e}")

        except Exception as e:
            await message.answer("❌ При отправке видео произошла непредвиденная ошибка. Попробуйте позже.")
            logging.error(f"Unexpected error sending video: {e}")
    if til == 'en':
        try:
            # Specify the video file path
            video_path = Path(r"./handlers/users/video.mp4")
            # Verify the file exists and is accessible
            if not video_path.exists():
                await message.answer("❌ Video file not found! Please contact technical support.")
                logging.error(f"Video file not found at: {video_path.absolute()}")
                return

            # Create FSInputFile with proper path
            video = FSInputFile(video_path)

            # Send video with caption
            await bot.send_video(
                chat_id=message.from_user.id,
                video=video,
                caption="✅ This video explains in detail how to create a slide using a bot.",
                supports_streaming=True  # Allows for streaming playback
            )

            logging.info(f"Video sent successfully to {message.from_user.id}")

        except TelegramBadRequest as e:
            await message.answer("❌ There was an error sending the video. Invalid video format or size.")
            logging.error(f"Telegram API error: {e}")

        except Exception as e:
            await message.answer(
                "❌ There was an unexpected error sending your video. Please try again later.")
            logging.error(f"Unexpected error sending video: {e}")


# @router.message(F.text=='/my')
# async def user_start(message: types.Message):
#     text=(f"💰Balansingiz: \n"
#           f"📚Taqdimotlaringiz soni:\n"
#           f"💵To'lovlaringiz miqdori: \n"
#
#           )
#     await message.answer(text)


# @router.message(F.text=='/help')
# async def user_start(message: types.Message):
#     text=("❗️Sizga qanday yordam berishim mumkinligini to'liq matn ko'rinishida adminga yuboring!\n"
#           "☎️ Admin: @slaydai_admin\n"
#           "Chat - @slaydai_chat\n"
#           "Bot yangilanishlari - @slaydai_news")


class tolov(StatesGroup):
    tanlov = State()
    payme = State()
    click = State()
    karta = State()
    chek = State()
    summa = State()


class tolov_ru(StatesGroup):
    tanlov_ru = State()
    payme_ru = State()
    click_ru = State()
    karta_ru = State()
    summa = State()
    chek_ru = State()


class tolov_en(StatesGroup):
    tanlov_en = State()
    payme_en = State()
    click_en = State()
    karta_en = State()
    chek_en = State()
    summa = State()


@router.message(F.text == '/bue')
async def user_start(message: types.Message, state: FSMContext):
    ol = db.select_user(tg_user=message.from_user.id)
    til = ol[4]
    if til == 'uz':
        await state.set_state(tolov.tanlov)
        text = "Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇"
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme"),
             InlineKeyboardButton(text="🔵 CLICK", callback_data="click")],
            [InlineKeyboardButton(text="💳 KARTA ORQALI", callback_data="karta")]])
        m = await message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m': m.message_id})
    if til == 'ru':
        await state.set_state(tolov_ru.tanlov_ru)
        text = "Какой способ оплаты вы предпочитаете? Воспользуйтесь кнопками ниже👇"
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme_ru"),
             InlineKeyboardButton(text="🔵 CLICK", callback_data="click_ru")],
            [InlineKeyboardButton(text="💳 КАРТОЙ", callback_data="karta_ru")]])
        m = await message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m': m.message_id})

    if til == 'en':
        await state.set_state(tolov_en.tanlov_en)
        text = "Which payment method do you prefer? Use the buttons below👇"
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme_en"),
             InlineKeyboardButton(text="🔵 CLICK", callback_data="click_en")],
            [InlineKeyboardButton(text="💳 BY MAP", callback_data="karta_en")]])
        m = await message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m': m.message_id})


# Karta uz
@router.callback_query(F.data == 'karta', tolov.tanlov)
async def user_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(tolov.karta)
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    text = (f"❗️Eng kamida 5000 so'm to'lov qiling, 5000 dan kam summalar bilan muammo bo'lishi mumkin.\n\n"
            f"💳 8600 0417 7483 8644\n"
            f"👤 Abdualiev Boburmirzo\n"
            f"Ushbu karta raqamiga to'lov qiling va quyidagi tugmani bosing yoki /chek ni yuboring!")
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Chekni yuborish", callback_data="chek_yubor")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="ortga")]])

    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


# Karta ru
@router.callback_query(F.data == 'karta_ru', tolov_ru.tanlov_ru)
async def user_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(tolov_ru.karta_ru)
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    text = (f"❗️Платите минимум 5000 сумов, с суммами меньше 5000 могут возникнуть проблемы.\n\n"
            f"💳 8600 0417 7483 8644\n"
            f"👤 Абдуалиев Бабурмирзо\n"
            f"Совершите платеж на этот номер карты и нажмите кнопку ниже или отправьте /chek")
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить чек", callback_data="chek_yubor_ru")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="ortga_ru")]])

    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


# Karta en
@router.callback_query(F.data == 'karta_en', tolov_en.tanlov_en)
async def user_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(tolov_en.karta_en)
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    text = (f"❗️Pay at least 5,000 soums, there may be problems with amounts less than 5,000.\n\n"
            f"💳 8600 0417 7483 8644\n"
            f"👤 Abdualiev Boburmirzo\n"
            f"Make a payment to this card number and click the button below or send /chek")
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Send a chek", callback_data="chek_yubor_en")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="ortga_en")]])

    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


# Ortga uz
@router.callback_query(F.data == 'ortga', tolov.karta)
async def user_start(message: CallbackQuery, state: FSMContext):
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    await state.set_state(tolov.tanlov)
    text = "Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇"
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme"),
         InlineKeyboardButton(text="🔵 CLICK", callback_data="click")],
        [InlineKeyboardButton(text="💳 KARTA ORQALI", callback_data="karta")]])
    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


#  Ortga ru
@router.callback_query(F.data == 'ortga_ru', tolov_ru.karta_ru)
async def user_start(message: CallbackQuery, state: FSMContext):
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    await state.set_state(tolov_ru.tanlov_ru)
    text = "Какой способ оплаты вы предпочитаете? Воспользуйтесь кнопками ниже👇"
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme_ru"),
         InlineKeyboardButton(text="🔵 CLICK", callback_data="click_ru")],
        [InlineKeyboardButton(text="💳 КАРТОЙ", callback_data="karta_ru")]])
    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


#  Ortga en
@router.callback_query(F.data == 'ortga_en', tolov_en.karta_en)
async def user_start(message: CallbackQuery, state: FSMContext):
    ol = await state.get_data()
    m = ol.get('m')
    await bot.delete_message(message.from_user.id, m)
    await state.set_state(tolov.tanlov)
    text = "Which payment method would you like to use? Use the buttons below👇"
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme_en"),
         InlineKeyboardButton(text="🔵 CLICK", callback_data="click_en")],
        [InlineKeyboardButton(text="💳 BY CARD", callback_data="karta_en")]])
    m = await message.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})


# chek_yubor uz
@router.callback_query(F.data == 'chek_yubor', tolov.karta)
async def user_start(message: CallbackQuery, state: FSMContext):
    m = await message.message.answer("To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:")
    await state.update_data({'m': m.message_id})
    await state.set_state(tolov.chek)


# Chek_yubor en
@router.callback_query(F.data == 'chek_yubor_en', tolov_en.karta_en)
async def user_start(message: CallbackQuery, state: FSMContext):
    m = await message.message.answer("Send a screenshot or file of the receipt confirming your payment:")
    await state.update_data({'m': m.message_id})
    await state.set_state(tolov_en.chek_en)


# Chek_yubor ru
@router.callback_query(F.data == 'chek_yubor_ru', tolov_ru.karta_ru)
async def user_start(message: CallbackQuery, state: FSMContext):
    m = await message.message.answer("Отправьте скриншот или файл чека, подтверждающего оплату:")
    await state.update_data({'m': m.message_id})
    await state.set_state(tolov_ru.chek_ru)


# /chek uz
@router.message(F.text == "/chek")
async def user_start(message: types.Message, state: FSMContext):
    ol = db.select_user(tg_user=message.from_user.id)
    til = ol[4]
    if til == 'uz':
        m = await message.answer("To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:")
        await state.update_data({'m': m.message_id})
        await state.set_state(tolov.chek)
    if til == 'ru':
        m = await message.answer("Отправьте скриншот или файл чека, подтверждающего оплату:")
        await state.update_data({'m': m.message_id})
        await state.set_state(tolov_ru.chek_ru)
    if til == 'en':
        m = await message.answer("Send a screenshot or file of the receipt confirming your payment:")
        await state.update_data({'m': m.message_id})
        await state.set_state(tolov_en.chek_en)


# uz
@router.message(StateFilter(tolov.chek),
                F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'}))
async def bot_start(message: types.Message, state: FSMContext):
    tugma = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5000", callback_data="5000"),
         InlineKeyboardButton(text="6000", callback_data="6000")],
        [InlineKeyboardButton(text="7000", callback_data="7000"),
         InlineKeyboardButton(text="8000", callback_data="8000")],
        [InlineKeyboardButton(text="10 000", callback_data="10000"),
         InlineKeyboardButton(text="15000", callback_data="15000")],
        [InlineKeyboardButton(text="20 000", callback_data="20000"),
         InlineKeyboardButton(text="30 000", callback_data="30000")],
        [InlineKeyboardButton(text="40 000", callback_data="40000"),
         InlineKeyboardButton(text="50000", callback_data="50000")]])
    await message.answer("Tugmalardan birini tanlang.", reply_markup=tugma)
    await state.set_state(tolov.summa)
    await state.update_data(mes_id=message.message_id)


from aiogram import F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


@router.callback_query(StateFilter(tolov.summa))
async def bot_start(call: CallbackQuery, state: FSMContext):
    ol = await state.get_data()
    mes_id = ol.get("mes_id")  # foydalanuvchi yuborgan chek xabari ID

    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Tastiqlash ✅",
                callback_data=f"tashtiqlash_chek::{call.from_user.id}"
            )
        ],
        [
            InlineKeyboardButton(text="Boshqa ❓", callback_data="boshqa"),
            InlineKeyboardButton(text="Qaytarish 🚫", callback_data="qaytarish")
        ]
    ])

    caption = (
        f"Tolov: {call.data}\n"
        f"User: {call.from_user.full_name} ({call.from_user.id})\n"
        f"Tugmalardan birini bosing:"
    )

    try:
        # Foydalanuvchi yuborgan original chekni olish
        original = await call.bot.forward_message(
            chat_id=5528965178,
            from_chat_id=call.from_user.id,
            message_id=mes_id
        )

        # Forward qilingan xabarni caption bilan qaytadan yuborish
        if call.message.photo:
            await call.bot.send_photo(
                chat_id=5528965178,
                photo=call.message.photo[-1].file_id,
                caption=caption,
                reply_markup=inline_buttons
            )
        elif call.message.document:
            await call.bot.send_document(
                chat_id=5528965178,
                document=call.message.document.file_id,
                caption=caption,
                reply_markup=inline_buttons
            )
        elif call.message.video:
            await call.bot.send_video(
                chat_id=5528965178,
                video=call.message.video.file_id,
                caption=caption,
                reply_markup=inline_buttons
            )
        elif call.message.text:
            await call.bot.send_message(
                chat_id=5528965178,
                text=f"{call.message.text}\n\n{caption}",
                reply_markup=inline_buttons
            )
        # boshqa turlar uchun ham xuddi shunday yozib chiqish mumkin

        await call.message.answer("Tolovingizni tastiqlashlarini kuting.⏳")

    except Exception as e:
        print(f"❌ 5528965178 ga yuborilmadi: {e}")


# _ru
@router.message(StateFilter(tolov_ru.chek_ru),
                F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'}))
async def bot_start(message: types.Message, state: FSMContext):
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтверждение ✅", callback_data=f"tashtiqlash_chek_ru::{message.from_user.id}")]])

    try:
        await bot.copy_message(
            chat_id=5528965178,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            caption="Подтвердите выкуп:",
            reply_markup=inline_buttons
        )
        await message.answer('Дождитесь подтверждения вашего платежа..⏳')
    except Exception as e:
        print(f"❌ {5528965178} ga yuborilmadi.{e}")


# _en
@router.message(StateFilter(tolov_en.chek_en),
                F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'}))
async def bot_start(message: types.Message, state: FSMContext):
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Confirmation ✅", callback_data=f"tashtiqlash_chek_en::{message.from_user.id}")]])

    try:
        await bot.copy_message(
            chat_id=5528965178,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            caption="Confirm the ransom:",
            reply_markup=inline_buttons
        )
        await message.answer('Wait for them to confirm your payment.⏳')
    except Exception as e:
        print(f"❌ {5528965178} ga yuborilmadi.{e}")


class tolov_tastiq(StatesGroup):
    tastiq = State()


class tolov_tastiq_ru(StatesGroup):
    tastiq_ru = State()


class tolov_tastiq_en(StatesGroup):
    tastiq_en = State()


@router.callback_query(F.data == "balans_ru")
@router.callback_query(F.data == "balans_en")
@router.callback_query(F.data == "balans")
async def handle_bg_selection(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ol = db.select_user(tg_user=callback.from_user.id)
    til = ol[4]
    pul = ol[3]
    if til == 'uz':
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Taqdimot", callback_data="taqdimot"),
             InlineKeyboardButton(text="📘Referat/Mustaqil ish", callback_data="referat")],
            [InlineKeyboardButton(text="🧾 Kurs ishi", callback_data="kurs_ishi"),
             InlineKeyboardButton(text="📃 Qo'llanma", callback_data="qollanma")],
            [InlineKeyboardButton(text="💰 Balans", callback_data="balans")],
            [InlineKeyboardButton(text="📑 Boshqa xizmatlar", callback_data="boshqa_xizmatlar"),
             InlineKeyboardButton(text="🔗 Referal tizim", callback_data="referal_tizim")],
            [InlineKeyboardButton(text="🇺🇿 Tilni o'zgartirish", callback_data="til_ozgar_uz")]
        ])
        text = (f"💰Balansingiz: {pul} so'm\n\n"
                f"Xisobingizni to'ldirish uchun /bye buyrug'idan foydalaning.\n\n"
                f"💰Bot xizmatlari:\n"
                f"📕 Taqdimoq har bir sahifa uchun: 500 so'm\n"
                f"📘 Referat/Mustaqil ish har bir sahifa uchun: 500 so'm\n"
                f"🧾 Kurs ishi:\n"
                f"25-30 sahifa --- 30 000 so'm\n"
                f"35-40 sahifa --- 40 000 so'm"
                )
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=inline_buttons)

    if til == 'ru':
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Презентация", callback_data="taqdimot_ru"),
             InlineKeyboardButton(text="📘Реферат /Самостоятельная работа", callback_data="referat_ru")],
            [InlineKeyboardButton(text="🧾 Курсовая работа", callback_data="kurs_ishi_ru"),
             InlineKeyboardButton(text="📃Руководство", callback_data="qollanma_ru")],
            [InlineKeyboardButton(text="💰Баланс", callback_data="balans_ru")],
            [InlineKeyboardButton(text="📑 Другие услуги", callback_data="boshqa_xizmatlar"),
             InlineKeyboardButton(text="🔗 Реферальная система", callback_data="referal_tizim")],
            [InlineKeyboardButton(text="🇷🇺 Изменить язык", callback_data="til_ozgar_ru")]
        ])
        text = (f"💰Ваш баланс: {pul} сум\n\n"
                f"Используйте команду /bye, чтобы пополнить счёт.\n\n"
                f"💰Бот-сервисы:\n"
                f"📕 Стоимость публикации за страницу: 500 сумов\n"
                f"📘 Реферат/Самостоятельная работа за страницу: 500 сумов\n"
                f"🧾 Курсовая работа:\n"
                f"25-30 страниц --- 30 000 сум\n"
                f"35-40 страниц --- 40 000 сум")
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=inline_buttons)

    if til == 'en':
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Presentation", callback_data="taqdimot_en"),
             InlineKeyboardButton(text="📘Essay/Independent Work", callback_data="referat_en")],
            [InlineKeyboardButton(text="🧾 Course Paper", callback_data="kurs_ishi_en"),
             InlineKeyboardButton(text="📃Guide", callback_data="qollanma_en")],
            [InlineKeyboardButton(text="💰Balance", callback_data="balans_en")],
            [InlineKeyboardButton(text="📑 Other services", callback_data="boshqa_xizmatlar"),
             InlineKeyboardButton(text="🔗 Referral system", callback_data="referal_tizim")],
            [InlineKeyboardButton(text="🇺🇸 Change language", callback_data="til_ozgar_en")]
        ])
        text = (f"💰Your balance: {pul} soums\n\n"
                f"Use the /bye command to top up your account."
                f"💰Bot services:\n"
                f"📕 Submission per page: 500 soums\n"
                f"📘 AbstEssay/Independent Work per page: 500 soums\n"
                f"🧾 Course Paper:\n"
                f"25-30 pages --- 30 000 sum\n"
                f"35-40 pages --- 40 000 sum")
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=inline_buttons)


# uz
@router.callback_query(F.data.startswith("tashtiqlash_chek"))
async def handle_bg_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(tolov_tastiq.tastiq)
    tg_user = callback.data.rsplit("::")[1]
    await state.update_data({"tg_user": tg_user})
    await callback.message.answer("Tolov summasini kiriting:")


# ru
@router.callback_query(F.data.startswith("tashtiqlash_chek_ru"))
async def handle_bg_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(tolov_tastiq_ru.tastiq_ru)
    tg_user = callback.data.rsplit("::")[1]
    await state.update_data({"tg_user": tg_user})
    await callback.message.answer("Введите сумму выкупа:")


# en
@router.callback_query(F.data.startswith("tashtiqlash_chek_en"))
async def handle_bg_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(tolov_tastiq_en.tastiq_en)
    tg_user = callback.data.rsplit("::")[1]
    await state.update_data({"tg_user": tg_user})
    await callback.message.answer("Enter the ransom amount:")


#  uz
@router.message(tolov_tastiq.tastiq)
async def handle_bg_selection(callback: types.Message, state: FSMContext):
    if not callback.text.isdigit():
        await callback.answer("❌ Iltimos, faqat raqam kiriting!")
        await state.set_state(tolov_tastiq.tastiq)
        return

    ol = await state.get_data()
    tg_user = ol.get('tg_user')
    pul = db.select_user(tg_user=tg_user)
    qosh = int(pul[3]) + int(callback.text)
    db.update_user_balans(tg_user=tg_user, balans=qosh)
    await callback.answer("Tolov muvaffaqiyatli tarizda tastiqlandi.✅\n\n"
                          f'Tolov summasi: {callback.text}')
    await bot.send_message(chat_id=tg_user, text=f'Tolov muvaffaqiyatli tarizda tastiqlandi.✅\n\n'
                                                 f'Tolov summasi: {callback.text}')
    await state.clear()


# en
@router.message(tolov_tastiq_en.tastiq_en)
async def handle_bg_selection(callback: types.Message, state: FSMContext):
    if not callback.text.isdigit():
        await callback.answer("❌ Please enter only a number!")
        await state.set_state(tolov_tastiq.tastiq)
        return

    ol = await state.get_data()
    tg_user = ol.get('tg_user')
    pul = db.select_user(tg_user=tg_user)
    qosh = int(pul[3]) + int(callback.text)
    db.update_user_balans(tg_user=tg_user, balans=qosh)
    await callback.answer("The ransom was successfully confirmed.✅\n\n"
                          f'Amount of compensation: {callback.text}')
    await bot.send_message(chat_id=tg_user, text=f'The ransom was successfully confirmed.✅\n\n'
                                                 f'Amount of compensation: {callback.text}')
    await state.clear()


# ru
@router.message(tolov_tastiq_ru.tastiq_ru)
async def handle_bg_selection(callback: types.Message, state: FSMContext):
    if not callback.text.isdigit():
        await callback.answer("❌ Пожалуйста, введите только одно число!")
        await state.set_state(tolov_tastiq.tastiq)
        return

    ol = await state.get_data()
    tg_user = ol.get('tg_user')
    pul = db.select_user(tg_user=tg_user)
    qosh = int(pul[3]) + int(callback.text)
    db.update_user_balans(tg_user=tg_user, balans=qosh)
    await callback.answer("Выкуп был успешно подтвержден.\n\n"
                          f'Размер компенсации: {callback.text}')
    await bot.send_message(chat_id=tg_user, text=f'Выкуп был успешно подтвержден...✅\n\n'
                                                 f'Размер компенсации: {callback.text}')
    await state.clear()