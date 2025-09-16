import os
import sqlite3
import django
from asgiref.sync import sync_to_async
from loader import bot, db

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangofiles.settings')
django.setup()

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters import CommandStart, Command

router = Router()

REFERRAL_REWARD = 500


def get_db_connection():
    return sqlite3.connect("db.sqlite3")


# Move the inline handler outside of the message handler
@router.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    user_id = inline_query.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user language
    cursor.execute("SELECT language FROM myfiles_referal WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    til = user_data[0] if user_data else 'en'

    me = await bot.get_me()
    bot_username = me.username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    if til == 'uz':
        share_text = "Men sizga bu foydali botni tavsiya qilaman!"
        title = "Do'stlaringizga ulashish"
        description = "Botni do'stlaringizga tavsiya qiling"
    elif til == 'ru':
        share_text = "Я рекомендую вам этого полезного бота!"
        title = "Поделитесь с друзьями"
        description = "Порекомендуйте бота своим друзьям"
    else:
        share_text = "I recommend this useful bot to you!"
        title = "Share with your friends"
        description = "Recommend the bot to your friends"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔗 Botga kirish" if til == 'uz' else "🔗 Войти в бот" if til == 'ru' else "🔗 Login to the bot",
            url=referral_link
        )]
    ])

    await bot.answer_inline_query(
        inline_query.id,
        results=[
            InlineQueryResultArticle(
                id="1",
                title=title,
                input_message_content=InputTextMessageContent(
                    message_text=f"{share_text}\n\n👉 {referral_link}",
                    parse_mode="HTML"
                ),
                reply_markup=keyboard,
                description=description
            )
        ],
        cache_time=1
    )


@router.message(Command("referal"))
async def referral_info(message: Message):
    ol = db.select_user(tg_user=message.from_user.id)
    til = ol[4]

    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()

    # Balansni olish
    cursor.execute("SELECT balance, referal_id FROM myfiles_referal WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
        if til == 'uz':
            await message.answer("Siz ro'yxatdan o'tmagansiz.")
        elif til == 'ru':
            await message.answer("Вы не зарегистрированы.")
        else:
            await message.answer("You are not registered.")
        return

    balance, invited_by = user_data

    # Siz taklif qilgan foydalanuvchilar soni va IDlari
    cursor.execute("SELECT user_id FROM myfiles_referal WHERE referal_id = ?", (user_id,))
    invited_users = cursor.fetchall()
    invited_count = len(invited_users)
    invited_ids = ", ".join(str(u[0]) for u in invited_users) if invited_users else "Yo'q"

    conn.close()

    user_id_str = str(message.from_user.id)
    me = await bot.get_me()
    bot_username = me.username
    referral_link = f"https://t.me/{bot_username}?start={user_id_str}"

    if til == 'uz':
        share_text = "Men sizga bu foydali botni tavsiya qilaman!"
        text = (
            f"📊 Referal ma'lumotlaringiz:\n"
            f"👥 Taklif qilganlar soni: {invited_count}\n"
            f"💰 Umumiy toplangan balans: {balance}\n"
            f"📋 Siz taklif qilganlar IDlari: {invited_ids}\n"
            f"📌 Sizning referal havolangiz:\n"
            f"<code>{referral_link}</code>\n\n"
            f"Quyidagi tugma orqali do'stlaringizga yuborishingiz mumkin:"
        )
        button_text = "📤 Do'stlarga ulashish"
    elif til == 'ru':
        share_text = "Я рекомендую вам этого полезного бота!"
        text = (
            f"📊 Ваша реферальная информация:\n"
            f"👥 Количество участников торгов: {invited_count}\n"
            f"💰 Общий накопленный баланс: {balance}\n"
            f"📋 ID приглашенных вами людей: {invited_ids}\n"
            f"📌 Ваша реферальная ссылка:\n"
            f"<code>{referral_link}</code>\n\n"
            f"Вы можете отправить его своим друзьям, используя кнопку ниже:"
        )
        button_text = "📤 Поделиться с друзьями"
    else:
        share_text = "I recommend this useful bot to you!"
        text = (
            f"📊 Your referral information:\n"
            f"👥 Number of bidders: {invited_count}\n"
            f"💰 Total accumulated balance: {balance}\n"
            f"📋 IDs of those you invited: {invited_ids}\n"
            f"📌 Your referral link:\n"
            f"<code>{referral_link}</code>\n\n"
            f"You can send it to your friends using the button below:"
        )
        button_text = "📤 Share with friends"

    # Share tugmasi
    share_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=button_text,
            switch_inline_query=f"{share_text} {referral_link}"
        )]
    ])

    await message.answer(
        text=text,
        reply_markup=share_keyboard,
        parse_mode="HTML"
    )



@router.callback_query(F.data==("referal_tizim"))
async def referral_info(message: CallbackQuery):
    ol = db.select_user(tg_user=message.from_user.id)
    til = ol[4]

    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()

    # Balansni olish
    cursor.execute("SELECT balance, referal_id FROM myfiles_referal WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
        if til == 'uz':
            await message.message.answer("Siz ro'yxatdan o'tmagansiz.")
        elif til == 'ru':
            await message.message.answer("Вы не зарегистрированы.")
        else:
            await message.message.answer("You are not registered.")
        return

    balance, invited_by = user_data

    # Siz taklif qilgan foydalanuvchilar soni va IDlari
    cursor.execute("SELECT user_id FROM myfiles_referal WHERE referal_id = ?", (user_id,))
    invited_users = cursor.fetchall()
    invited_count = len(invited_users)
    invited_ids = ", ".join(str(u[0]) for u in invited_users) if invited_users else "Yo'q"

    conn.close()

    user_id_str = str(message.from_user.id)
    me = await bot.get_me()
    bot_username = me.username
    referral_link = f"https://t.me/{bot_username}?start={user_id_str}"

    if til == 'uz':
        share_text = "Men sizga bu foydali botni tavsiya qilaman!"
        text = (
            f"📊 Referal ma'lumotlaringiz:\n"
            f"👥 Taklif qilganlar soni: {invited_count}\n"
            f"💰 Umumiy toplangan balans: {balance}\n"
            f"📋 Siz taklif qilganlar IDlari: {invited_ids}\n"
            f"📌 Sizning referal havolangiz:\n"
            f"<code>{referral_link}</code>\n\n"
            f"Quyidagi tugma orqali do'stlaringizga yuborishingiz mumkin:"
        )
        button_text = "📤 Do'stlarga ulashish"
    elif til == 'ru':
        share_text = "Я рекомендую вам этого полезного бота!"
        text = (
            f"📊 Ваша реферальная информация:\n"
            f"👥 Количество участников торгов: {invited_count}\n"
            f"💰 Общий накопленный баланс: {balance}\n"
            f"📋 ID приглашенных вами людей: {invited_ids}\n"
            f"📌 Ваша реферальная ссылка:\n"
            f"<code>{referral_link}</code>\n\n"
            f"Вы можете отправить его своим друзьям, используя кнопку ниже:"
        )
        button_text = "📤 Поделиться с друзьями"
    else:
        share_text = "I recommend this useful bot to you!"
        text = (
            f"📊 Your referral information:\n"
            f"👥 Number of bidders: {invited_count}\n"
            f"💰 Total accumulated balance: {balance}\n"
            f"📋 IDs of those you invited: {invited_ids}\n"
            f"📌 Your referral link:\n"
            f"<code>{referral_link}</code>\n\n"
            f"You can send it to your friends using the button below:"
        )
        button_text = "📤 Share with friends"

    # Share tugmasi
    share_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=button_text,
            switch_inline_query=f"{share_text} {referral_link}"
        )]
    ])

    await message.message.answer(
        text=text,
        reply_markup=share_keyboard,
        parse_mode="HTML"
    )