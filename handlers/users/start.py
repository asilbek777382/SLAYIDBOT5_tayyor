import asyncio
import logging
from gc import callbacks
from typing import Optional

from aiogram import Router, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from asgiref.sync import sync_to_async

from handlers.users.referal import REFERRAL_REWARD
from loader import bot, db  # Bot va db import qilish
from aiogram import Bot

from myfiles.models import Referal
from states.state import Admin

logging.basicConfig(level=logging.INFO)

router = Router()


# Bot statusini yaratish
class Foydalanuvchi(StatesGroup):
    til = State()
    tek = State()


# Foydalanuvchi boshlang'ich boshlash uchun
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):

    """Handle the /start command with referral system and language-specific menus."""
    await message.delete()
    await state.clear()

    user_id = str(message.from_user.id)
    args = message.text.split()[1] if len(message.text.split()) > 1 else None

    # Process referral system if args exists
    await _process_referral_system(user_id, args)

    # Show appropriate menu based on user's language
    await _show_user_menu(message, state, user_id, args)


async def _process_referral_system(user_id: str, referral_code: Optional[str]):
    """Process referral system logic if referral code exists."""
    if not referral_code or referral_code == user_id:
        return

    try:
        # Get or create new user
        new_user, created = await sync_to_async(Referal.objects.get_or_create)(
            user_id=user_id,
            defaults={'balance': 0}
        )

        if not created or new_user.referal_id is not None:
            return

        try:
            referrer = await sync_to_async(Referal.objects.get)(user_id=referral_code)

            # Update balances
            referrer.balance += REFERRAL_REWARD
            await sync_to_async(referrer.save)()

            new_user.referal_id = referral_code
            await sync_to_async(new_user.save)()

            # Notify referrer
            await _notify_referrer(referral_code)

        except Referal.DoesNotExist:
            print(f"Referrer not found: {referral_code}")
        except Exception as e:
            print(f"Referral system error: {e}")

    except Exception as e:
        print(f"Error in referral processing: {e}")


async def _notify_referrer(referral_code: str):
    """Send notification to referrer about successful referral."""
    try:
        referrer_data = db.select_user(tg_user=referral_code)
        if referrer_data:
            new_balance = int(referrer_data[3]) + REFERRAL_REWARD
            db.update_user_balans(balans=new_balance, tg_user=referral_code)

            await bot.send_message(
                chat_id=int(referral_code),
                text=f"🎉 Congratulations! A new user joined via your referral link!\n"
                     f"💰 {REFERRAL_REWARD} points have been added to your balance!"
            )
    except Exception as e:
        print(f"Error sending notification: {e}")


async def _show_user_menu(message: Message, state: FSMContext, user_id: str, referral_code: Optional[str]):
    """Show appropriate menu based on user's language settings."""
    user_data = db.select_user(tg_user=message.from_user.id)

    if not user_data:
        await _show_language_selection(message, state)
        return

    lang = user_data[4]
    menu_config = {
        'uz': {
            'buttons': [
                [("📕Taqdimot", "taqdimot"), ("📘Referat/Mustaqil ish", "referat")],
                [("🧾 Kurs ishi", "kurs_ishi"), ("📃 Qo'llanma", "qollanma")],
                [("💰 Balans", "balans")],
                [("📑 Boshqa xizmatlar", "boshqa_xizmatlar"),("🔗 Referal tizim","referal_tizim")],
                [("🇺🇿 Tilni o'zgartirish", "til_ozgar_uz")]
            ],
            'text': (
                'Assalomu alaykum!\n\n'
                '🆕 Yangi Taqdimot (Slayd) - tugmasini bosib taqdimot(slayd) yaratishni boshlashingiz mumkin!\n'
                '📚 Yangi Refarat - Tugmasini bosish orqali referat yaratishingiz mumkin!\n'
                '📑 Yangi Mustaqil ish - Tugmasini bosish orqali mustaqil ish yaratishingiz mumkin!\n'
                "🖼 Rasm Yaratish (Ai) - Tugmasini bosish orqali sun'iy intellekt yordamida turli rasmlar yaratish mumkin!\n\n"
                "/help - Botdan qanday foydalanish haqida ma'lumot. Iltimos, avval shu bo'lim bilan tanishib chiqing.\n\n"
                "❗️Botga tez-tez yangiliklar qo'shmoqdamiz. Yangiliklar uchun @aislide kanaliga obuna bo'ling!\n\n"
                "Savol va takliflar: @Slaydai_bot"
            )
        },
        'en': {
            'buttons': [
                [("📕Presentation", "taqdimot_en"), ("📘Essay/Independent Work", "referat_en")],
                [("🧾 Course Paper", "kurs_ishi_en"), ("📃Guide", "qollanma_en")],
                [("💰Balance", "balans_en")],

            [("📑 Other services", "boshqa_xizmatlar"), ("🔗 Referral system", "referal_tizim")],
                [("🇺🇸 Change language", "til_ozgar_en")]
            ],
            'text': (
                'Hello!\n\n'
                '🆕 Click the "New Presentation (Slide)" button to start creating a presentation (slide)!\n'
                '📚 Click the "New Essay" button to create an essay!\n'
                '📑 Click the "New Independent Work" button to create independent work!\n'
                '🖼 Create Image (AI) - this button allows you to generate various images using artificial intelligence!\n\n'
                '/help - information on how to use the bot. Please read this section first.\n\n'
                '❗️We regularly add new features to the bot. Subscribe to @aislide to stay updated with the latest news!\n\n'
                'Questions and suggestions: @Slaydai_bot'
            )
        },
        'ru': {
            'buttons': [
                [("📕Презентация", "taqdimot_ru"), ("📘Эссе/Самостоятельная работа", "referat_ru")],
                [("🧾 Курсовая работа", "kurs_ishi_ru"), ("📃Руководство", "qollanma_ru")],
                [("💰Баланс", "balans_ru")],
                [("📑 Другие услуги", "boshqa_xizmatlar"), ("🔗 Реферальная система", "referal_tizim")],
                [("🇷🇺 Изменить язык", "til_ozgar_ru")]
            ],
            'text': (
                'Здравствуйте!\n\n'
                '🆕 Нажмите кнопку «Новая презентация (слайды)», чтобы начать создание презентации (слайдов)!\n'
                '📚 Нажмите кнопку «Новое эссе», чтобы создать эссе!\n'
                '📑 Нажмите кнопку «Новая самостоятельная работа», чтобы создать самостоятельную работу!\n'
                '🖼 Создать изображение (ИИ) - эта кнопка позволяет генерировать различные изображения с помощью искусственного интеллекта!\n\n'
                '/help - информация о том, как пользоваться ботом. Пожалуйста, сначала ознакомьтесь с этим разделом.\n\n'
                '❗️Мы регулярно добавляем в бота новые функции. Подпишитесь на @aislide, чтобы быть в курсе всех новостей!\n\n'
                'Вопросы и предложения: @Slaydai_bot'
            )
        }
    }

    config = menu_config.get(lang, menu_config['uz'])

    # Add referral welcome message if applicable
    if referral_code and referral_code != user_id:
        welcome_messages = {
            'uz': "\n\n🎉 Siz {code} foydalanuvchisi orqali botga qo'shildingiz!",
            'en': "\n\n🎉 You joined the bot via user {code}!",
            'ru': "\n\n🎉 Вы присоединились к боту через пользователя {code}!"
        }
        config['text'] += welcome_messages.get(lang, welcome_messages['uz']).format(code=referral_code)

    # Create and send menu
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
            for row in config['buttons']
        ]
    )

    msg = await message.answer(config['text'], reply_markup=keyboard)
    await state.update_data({'m_id': msg.message_id})


async def _show_language_selection(message: Message, state: FSMContext):
    """Show language selection menu for new users."""
    text = ('🇺🇿 Tugmalar, va boshqaruv xabarlari tilini tanlash uchun quyidagi tugmalardan foydalaning.\n'
            '🇷🇺 Используйте следующие кнопки для выбора языка интерфейса.\n'
            '🇺🇸 Use the following buttons to select the interface language.')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
         InlineKeyboardButton(text="🇺🇸 English", callback_data="en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")]
    ])

    msg = await message.answer(text, reply_markup=keyboard)
    await state.update_data({'m': msg.message_id})
    await state.set_state(Foydalanuvchi.til)


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@router.callback_query(Foydalanuvchi.til)
async def send_tutorial_video(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Foydalanuvchi.tek)
    await callback.message.delete()
    til = callback.data  # Tilni callback.data dan olamiz

    # Guruhlarni tilga qarab olish
    guruxlar = db.select_kanallars()  # Masalan, til bo'yicha guruhlar

    user_id = callback.from_user.id

    # InlineKeyboardMarkup yaratish, inline_keyboard bo'sh ro'yxat bilan
    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])  # 1 ta tugma qatoriga joylashadi

    for gurux in guruxlar:
        channel_username = gurux[2]  # Guruh username'si

        obuna = await check_subscription(user_id, channel_username)

        # Agar obuna bo'lmagan bo'lsa, tugma qo'shamiz
        if not obuna:
            # Tilga qarab ogohlantirish matnini tanlaymiz
            if til == 'uz':
                matn = f"Iltimos, quyidagi kanalga obuna bo'ling:"
            elif til == 'en':
                matn = f"Please subscribe to the channel:"
            elif til == 'ru':
                matn = f"Пожалуйста, подпишитесь на канал:"
            else:
                matn = f"Please subscribe to the channel:"

            # Kanalga obuna bo'lish tugmasi
            obuna_tugma = InlineKeyboardButton(
                text=f"{channel_username}",
                callback_data=f"{channel_username}",  # callback_data ni o'zgartirdim
                url=f"https://t.me/{channel_username[1:]}"  # Kanal URL'ini aniq berish
            )

            # Tugmani inline_keyboard ro'yxatiga qo'shish
            keyboard.inline_keyboard.append([obuna_tugma])  # Har bir tugma alohida qatorga joylanadi

        # Agar hech bo'lmaganda bitta tugma bo'lsa, matn va tugmalarni yuboramiz
    if keyboard.inline_keyboard:
        if til == 'uz':

            tekshir = InlineKeyboardButton(
                text=f"Obuna bo'ldim",
                callback_data=f"subscribe_uz",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])
        elif til == 'en':
            tekshir = InlineKeyboardButton(
                text=f"I subscribed.",
                callback_data=f"subscribe_rn",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])

        elif til == 'ru':
            tekshir = InlineKeyboardButton(
                text=f"Я подписался.",
                callback_data=f"subscribe_ru",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])
            matn = f"Пожалуйста, подпишитесь на канал:"

        await callback.message.answer(matn, reply_markup=keyboard)
        return

    # Agar foydalanuvchi barcha guruhlarga obuna bo'lsa
    if til == 'uz':

                db.add_user(tg_user=callback.from_user.id,user_ismi=callback.from_user.first_name ,balans=0,til='uz')
                db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")
                inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📕Taqdimot", callback_data="taqdimot"),
                     InlineKeyboardButton(text="📘Referat/Mustaqil ish", callback_data="referat")],
                    [InlineKeyboardButton(text="🧾 Kurs ishi", callback_data="kurs_ishi"),
                     InlineKeyboardButton(text="📃Qo'llanma", callback_data="qollanma")],
                [("📑 Boshqa xizmatlar", "boshqa_xizmatlar"),("🔗 Referal tizim","referal_tizim")],
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
        db.add_user(tg_user=callback.from_user.id, user_ismi=callback.from_user.first_name , balans=0,til='en')
        db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Presentation", callback_data="taqdimot_en"),
             InlineKeyboardButton(text="📘Essay/Independent Work", callback_data="referat_en")],
            [InlineKeyboardButton(text="🧾 Course Paper", callback_data="kurs_ishi_en"),
             InlineKeyboardButton(text="📃Guide", callback_data="qollanma_en")],
            [InlineKeyboardButton(text="💰Balance", callback_data="balans_en")],
            [InlineKeyboardButton(text="📑 Other services", callback_data="boshqa_xizmatlar"),InlineKeyboardButton(text="🔗 Referral system", callback_data="referal_tizim")],
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
        db.add_user(tg_user=callback.from_user.id, user_ismi=callback.from_user.first_name , balans=0,til='ru')
        db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📕Презентация", callback_data="taqdimot_ru"),
             InlineKeyboardButton(text="📘Эссе/Самостоятельная работа", callback_data="referat_ru")],
            [InlineKeyboardButton(text="🧾 Курсовая работа", callback_data="kurs_ishi_ru"),
             InlineKeyboardButton(text="📃Руководство", callback_data="qollanma_ru")],
            [InlineKeyboardButton(text="💰Баланс", callback_data="balans_ru")],
            [InlineKeyboardButton(text="📑 Другие услуги", callback_data="boshqa_xizmatlar"),InlineKeyboardButton(text="🔗 Реферальная система", callback_data="referal_tizim")],
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




# Foydalanuvchi "Obuna bo'ldim" tugmasini bosganida
@router.callback_query(F.data.startswith('subscribe_'),StateFilter(Foydalanuvchi.tek))
async def subscribe_confirmation(callback: types.CallbackQuery,state:FSMContext):

    til = callback.data.split('_')[1]
   # Tilni callback.data dan olamiz

    # Guruhlarni tilga qarab olish
    guruxlar = db.select_kanallars()  # Masalan, til bo'yicha guruhlar

    user_id = callback.from_user.id

    # InlineKeyboardMarkup yaratish, inline_keyboard bo'sh ro'yxat bilan
    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])  # 1 ta tugma qatoriga joylashadi

    for gurux in guruxlar:
        channel_username = gurux[2]  # Guruh username'si

        obuna = await check_subscription(user_id, channel_username)

        # Agar obuna bo'lmagan bo'lsa, tugma qo'shamiz
        if not obuna:
            # Tilga qarab ogohlantirish matnini tanlaymiz
            if til == 'uz':
                matn = f"Iltimos, quyidagi kanalga obuna bo'ling:"
            elif til == 'en':
                matn = f"Please subscribe to the channel:"
            elif til == 'ru':
                matn = f"Пожалуйста, подпишитесь на канал:"
            else:
                matn = f"Please subscribe to the channel:"

            # Kanalga obuna bo'lish tugmasi
            obuna_tugma = InlineKeyboardButton(
                text=f"{channel_username}",
                callback_data=f"{channel_username}",  # callback_data ni o'zgartirdim
                url=f"https://t.me/{channel_username[1:]}"  # Kanal URL'ini aniq berish
            )

            # Tugmani inline_keyboard ro'yxatiga qo'shish
            keyboard.inline_keyboard.append([obuna_tugma])  # Har bir tugma alohida qatorga joylanadi

        # Agar hech bo'lmaganda bitta tugma bo'lsa, matn va tugmalarni yuboramiz
    if keyboard.inline_keyboard:
        if til == 'uz':

            tekshir = InlineKeyboardButton(
                text=f"Obuna bo'ldim",
                callback_data=f"subscribe_uz",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])
        elif til == 'en':
            tekshir = InlineKeyboardButton(
                text=f"I subscribed.",
                callback_data=f"subscribe_rn",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])

        elif til == 'ru':
            tekshir = InlineKeyboardButton(
                text=f"Я подписался.",
                callback_data=f"subscribe_ru",  # callback_data ni o'zgartirdim
                # Kanal URL'ini aniq berish
            )
            keyboard.inline_keyboard.append([tekshir])
            matn = f"Пожалуйста, подпишитесь на канал:"

        await callback.message.answer(matn, reply_markup=keyboard)
        return

    # Agar foydalanuvchi barcha guruhlarga obuna bo'lsa
    if til == 'uz':

                db.add_user(tg_user=callback.from_user.id,user_ismi=callback.from_user.first_name ,balans=0,til='uz')
                db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")

                inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📕Taqdimot", callback_data="taqdimot"),
                     InlineKeyboardButton(text="📘Referat/Mustaqil ish", callback_data="referat")],
                    [InlineKeyboardButton(text="🧾 Kurs ishi", callback_data="kurs_ishi"),
                     InlineKeyboardButton(text="📃Qo'llanma", callback_data="qollanma")],
                    [InlineKeyboardButton(text="💰Balans", callback_data="balans")],
                [("📑 Boshqa xizmatlar", "boshqa_xizmatlar"),("🔗 Referal tizim","referal_tizim")],
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
        db.add_user(tg_user=callback.from_user.id, user_ismi=callback.from_user.first_name , balans=0,til='en')
        db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")
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
        db.add_user(tg_user=callback.from_user.id, user_ismi=callback.from_user.first_name , balans=0,til='ru')
        db.ad_referal(user_id=callback.from_user.id, referal_id=None, balance="0")
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


async def check_subscription(user_id: int, channel_username: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        if member.status in ['member', 'creator', 'administrator']:
            return True
        else:
            return False
    except Exception:
        return False
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
@router.message(F.text=='/panel',StateFilter(None))
async def bot_start(message: types.Message,state: FSMContext):
    await message.delete()
    ol_id=db.select_admin(tg_user=message.from_user.id)
    ol_username=db.select_admin(username=f"@{message.from_user.username}")
    if ol_id or ol_username:
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish",
                                  callback_data="bot_azolariga_xabar_yuborish")],
            [InlineKeyboardButton(text="ℹ🗞 Forward xabar yuborish", callback_data="forward_xabar_yuborish")],
            [InlineKeyboardButton(text="👥 Guruxlarga xabar yuborish", callback_data="guruxlarga_xabar_yuborish")],
            [InlineKeyboardButton(text="📨 Bitta a'zoga xabar yuborish", callback_data="bitta_azoga_xabar_yuborish")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="statistika")],

        ])
        reply_buttons = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=" 🕹 Majburiy a'zolik"), KeyboardButton(text="⚙️ Admin sozlamalari")],
                [KeyboardButton(text="💰 Balans")]
            ],
            resize_keyboard=True
        )

        m = await message.answer(text='Tanlang', reply_markup=inline_buttons)
        await state.update_data({'m_id': m.message_id})
        await message.answer(text='Quyidagilardan tugmalardan birini tanlang:', reply_markup=reply_buttons)
        await state.set_state(Admin.admin_tanlov)

    else:
        await message.delete()




@router.callback_query(F.data=='boshqa_xizmatlar')
async def bot_start(message: types.CallbackQuery,state: FSMContext):
    ol=db.select_user(tg_user=message.from_user.id)
    til=ol[4]
    if til=='uz':
        await message.message.answer("Biz 7 yildan ortiq tajribaga ega professional mutaxassis xizmatlarini taklif etamiz:\n\n✅ Slaydlar (taqdimotlar)\n✅ Kurs ishi\n✅ Mustaqil ish\n✅ Maqola, tezislar va insholar\nDiplom ishi (BMI)\n✅ Dissertatsiya (PhD)\n✅ Testlar va krossvordlar\n\n⚠️ Taqdim etilgan xizmatlar bot emas, balki inson tomonidan amalga oshiriladi.\n\n📨 Bog'lanish uchun: @Slaydai_bot")
    if til=='ru':
        await message.message.answer(
            "Мы предлагаем услуги профессиональных специалистов с более чем 7-летним опытом работы:\n\n✅ Слайды (презентации)\n✅ Курсовые работы\n✅ Самостоятельные работы\n✅ Статьи, диссертации и эссе\n✅ Диссертации (БМИ)\n✅ Диссертации (кандидатские)\n✅ Контрольные работы и кроссворды\n\n⚠️ Услуги предоставляются человеком, а не ботом.\n\n📨 Для связи: @Slaydai_bot")
    if til == 'en':
            await message.message.answer(
                "We offer professional specialist services with over 7 years of experience:\n\n✅ Slides (presentations)\n✅ Coursework\nIndependent work\n✅ Articles, theses and essays\n✅ Thesis (BMI)\n✅ Dissertation (PhD)\n✅ Tests and crosswords\n\n⚠️ The services provided are performed by a human, not a bot.\n\n📨 To contact: @Slaydai_bot")
