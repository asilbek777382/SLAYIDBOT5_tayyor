import asyncio
import logging
from aiogram import Router, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from loader import bot, db  # Bot va db import qilish
from aiogram import Bot

from states.state import Admin

logging.basicConfig(level=logging.INFO)

router = Router()

class settings(StatesGroup):
    settings = State()
    til_tanla=State()
import random
@router.callback_query(F.data.startswith("til_ozgar_"))
async def send_tutorial_video(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(settings.settings)
    m_ol=await state.get_data()
    til = db.select_user(tg_user=callback.from_user.id)[4]
    await callback.message.delete()
    text = ('🇺🇿 Tugmalar, va boshqaruv xabarlari tilini tanlash uchun quyidagi tugmalardan foydalaning.\n'
            '🇷🇺 Используйте следующие кнопки для выбора языка интерфейса.\n'
            '🇺🇸 Use the following buttons to select the interface language.')

    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
         InlineKeyboardButton(text="🇺🇸 English", callback_data="en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")]
    ])
    m = await callback.message.answer(text, reply_markup=inline_buttons)
    await state.update_data({'m': m.message_id})
    await state.set_state(settings.til_tanla)

@router.callback_query(settings.til_tanla)
async def send_tutorial_video(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    til = callback.data
    if til == 'uz':
        db.update_user_lang2(tg_user=callback.from_user.id,til='uz')

        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Taqdimot", callback_data="taqdimot"),
             InlineKeyboardButton(text="📘Referat/Mustaqil ish", callback_data="referat")],
            [InlineKeyboardButton(text="🧾 Kurs ishi", callback_data="kurs_ishi"),
             InlineKeyboardButton(text="📃Qo'llanma", callback_data="qollanma")],
            [InlineKeyboardButton(text="💰Balans", callback_data="balans")],
            [InlineKeyboardButton(text="🇺🇿 Tilni o'zgartirish", callback_data="til_ozgar_uz")]
        ])
        text = ('Assalomu alaykum!\n\n'
                '🆕 Yangi Taqdimot (Slayd) - tugmasini bosib taqdimot(slayd) yaratishni boshlashingiz mumkin!\n'
                '📚 Yangi Refarat - Tugmasini bosish orqali referat yaratishingiz mumkin!\n'
                '📑 Yangi Mustaqil ish - Tugmasini bosish orqali mustaqil ish yaratishingiz mumkin!\n'
                "🖼 Rasm Yaratish (Ai) - Tugmasini bosish orqali sun'iy intellekt yordamida turli rasmlar yaratish mumkin!\n\n"
                "/help - Botdan qanday foydalanish haqida ma'lumot. Iltimos, avval shu bo'lim bilan tanishib chiqing.\n\n"
                "❗️Botga tez-tez yangiliklar qo'shmoqdamiz. Yangiliklar uchun @aislide kanaliga obuna bo'ling!\n\n"
                "Savol va takliflar: @Slaydai_bot")
        m = await callback.message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m_id': m.message_id})

        await state.clear()

    if til == 'en':
        db.update_user_lang2(tg_user=callback.from_user.id,til='en')
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Presentation", callback_data="taqdimot_en"),
             InlineKeyboardButton(text="📘Essay/Independent Work", callback_data="referat_en")],
            [InlineKeyboardButton(text="🧾 Course Paper", callback_data="kurs_ishi_en"),
             InlineKeyboardButton(text="📃Guide", callback_data="qollanma_en")],
            [InlineKeyboardButton(text="💰Balance", callback_data="balans_en")],
            [InlineKeyboardButton(text="🇺🇸 Change language", callback_data="til_ozgar_en")]
        ])

        text = ('Hello!\n\n'
                '🆕 Click the "New Presentation (Slide)" button to start creating a presentation (slide)!\n'
                '📚 Click the "New Essay" button to create an essay!\n'
                '📑 Click the "New Independent Work" button to create independent work!\n'
                '🖼 Create Image (AI) — this button allows you to generate various images using artificial intelligence!\n\n'
                '/help — information on how to use the bot. Please read this section first.\n\n'
                '❗️We regularly add new features to the bot. Subscribe to @aislide to stay updated with the latest news!\n\n'
                'Questions and suggestions: @Slaydai_bot')

        m = await callback.message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m_id': m.message_id})
        await state.clear()
    if til == 'ru':
        db.update_user_lang2(tg_user=callback.from_user.id,til='ru')
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Презентация", callback_data="taqdimot_ru"),
             InlineKeyboardButton(text="📘Эссе/Самостоятельная работа", callback_data="referat_ru")],
            [InlineKeyboardButton(text="🧾 Курсовая работа", callback_data="kurs_ishi_ru"),
             InlineKeyboardButton(text="📃Руководство", callback_data="qollanma_ru")],
            [InlineKeyboardButton(text="💰Баланс", callback_data="balans_ru")],
            [InlineKeyboardButton(text="🇷🇺 Изменить язык", callback_data="til_ozgar_ru")]
        ])

        text = ('Здравствуйте!\n\n'
                '🆕 Нажмите кнопку «Новая презентация (слайды)», чтобы начать создание презентации (слайдов)!\n'
                '📚 Нажмите кнопку «Новое эссе», чтобы создать эссе!\n'
                '📑 Нажмите кнопку «Новая самостоятельная работа», чтобы создать самостоятельную работу!\n'
                '🖼 Создать изображение (ИИ) — эта кнопка позволяет генерировать различные изображения с помощью искусственного интеллекта!\n\n'
                '/help — информация о том, как пользоваться ботом. Пожалуйста, сначала ознакомьтесь с этим разделом.\n\n'
                '❗️Мы регулярно добавляем в бота новые функции. Подпишитесь на @aislide, чтобы быть в курсе всех новостей!\n\n'
                'Вопросы и предложения: @Slaydai_bot')

        m = await callback.message.answer(text, reply_markup=inline_buttons)
        await state.update_data({'m_id': m.message_id})
        await state.clear()

    # if til=='uz':
    #     db.update_user_lang2(tg_user=callback.from_user.id,til='ru')
    #     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="📕Презентация", callback_data="taqdimot_ru"),
    #          InlineKeyboardButton(text="📘Эссе/Самостоятельная работа", callback_data="referat_ru")],
    #         [InlineKeyboardButton(text="🧾 Курсовая работа", callback_data="kurs_ishi_ru"),
    #          InlineKeyboardButton(text="📃Руководство", callback_data="qollanma_ru")],
    #         [InlineKeyboardButton(text="💰Баланс", callback_data="balans_ru")],
    #             [InlineKeyboardButton(text="🇷🇺 Изменить язык", callback_data="til_ozgar_ru")]
    #     ])
    #
    #     text = ('Здравствуйте!\n\n'
    #             '🆕 Нажмите кнопку «Новая презентация (слайды)», чтобы начать создание презентации (слайдов)!\n'
    #             '📚 Нажмите кнопку «Новое эссе», чтобы создать эссе!\n'
    #             '📑 Нажмите кнопку «Новая самостоятельная работа», чтобы создать самостоятельную работу!\n'
    #             '🖼 Создать изображение (ИИ) — эта кнопка позволяет генерировать различные изображения с помощью искусственного интеллекта!\n\n'
    #             '/help — информация о том, как пользоваться ботом. Пожалуйста, сначала ознакомьтесь с этим разделом.\n\n'
    #             '❗️Мы регулярно добавляем в бота новые функции. Подпишитесь на @aislide, чтобы быть в курсе всех новостей!\n\n'
    #             'Вопросы и предложения: @Slaydai_bot')
    #
    #     m = await callback.message.answer(text, reply_markup=inline_buttons)
    #     await state.update_data({'m_id': m.message_id})
    #     await state.clear()
    #
    #
    # if til=='ru':
    #     db.update_user_lang2(tg_user=callback.from_user.id, til='en')
    #     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="📕Presentation", callback_data="taqdimot_en"),
    #          InlineKeyboardButton(text="📘Essay/Independent Work", callback_data="referat_en")],
    #         [InlineKeyboardButton(text="🧾 Course Paper", callback_data="kurs_ishi_en"),
    #          InlineKeyboardButton(text="📃Guide", callback_data="qollanma_en")],
    #         [InlineKeyboardButton(text="💰Balance", callback_data="balans_en")],
    #         [InlineKeyboardButton(text="🇺🇸 Change language", callback_data="til_ozgar_en")]
    #     ])
    #
    #     text = ('Hello!\n\n'
    #             '🆕 Click the "New Presentation (Slide)" button to start creating a presentation (slide)!\n'
    #             '📚 Click the "New Essay" button to create an essay!\n'
    #             '📑 Click the "New Independent Work" button to create independent work!\n'
    #             '🖼 Create Image (AI) — this button allows you to generate various images using artificial intelligence!\n\n'
    #             '/help — information on how to use the bot. Please read this section first.\n\n'
    #             '❗️We regularly add new features to the bot. Subscribe to @aislide to stay updated with the latest news!\n\n'
    #             'Questions and suggestions: @Slaydai_bot')
    #
    #     m = await callback.message.answer(text, reply_markup=inline_buttons)
    #     await state.update_data({'m_id': m.message_id})
    #     await state.clear()
    # if til=='en':
    #     db.update_user_lang2(tg_user=callback.from_user.id, til='uz')
    #     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="📕Taqdimot", callback_data="taqdimot"),
    #          InlineKeyboardButton(text="📘Referat/Mustaqil ish", callback_data="referat")],
    #         [InlineKeyboardButton(text="🧾 Kurs ishi", callback_data="kurs_ishi"),
    #          InlineKeyboardButton(text="📃Qo'llanma", callback_data="qollanma")],
    #         [InlineKeyboardButton(text="💰Balans", callback_data="balans")],
    #         [InlineKeyboardButton(text="🇺🇿 Tilni o'zgartirish", callback_data="til_ozgar_uz")]
    #     ])
    #     text = ('Assalomu alaykum!\n\n'
    #             '🆕 Yangi Taqdimot (Slayd) - tugmasini bosib taqdimot(slayd) yaratishni boshlashingiz mumkin!\n'
    #             '📚 Yangi Refarat - Tugmasini bosish orqali referat yaratishingiz mumkin!\n'
    #             '📑 Yangi Mustaqil ish - Tugmasini bosish orqali mustaqil ish yaratishingiz mumkin!\n'
    #             "🖼 Rasm Yaratish (Ai) - Tugmasini bosish orqali sun'iy intellekt yordamida turli rasmlar yaratish mumkin!\n\n"
    #             "/help - Botdan qanday foydalanish haqida ma'lumot. Iltimos, avval shu bo'lim bilan tanishib chiqing.\n\n"
    #             "❗️Botga tez-tez yangiliklar qo'shmoqdamiz. Yangiliklar uchun @aislide kanaliga obuna bo'ling!\n\n"
    #             "Savol va takliflar: @Slaydai_bot")
    #     m = await callback.message.answer(text, reply_markup=inline_buttons)
    #     await state.update_data({'m_id': m.message_id})
    #
    #
    #     await state.clear()
    # reply_buttons = ReplyKeyboardMarkup(
    #     keyboard=[
    #         [KeyboardButton(text="🇺🇿 Tilni o'zgartirish"), KeyboardButton(text="⚙️ Admin sozlamalari")],
    #         [KeyboardButton(text="💰 Balans")]
    #     ],
    #     resize_keyboard=True
    # )
    # await callback.message.answer(text='Tanlang', reply_markup=reply_buttons)
