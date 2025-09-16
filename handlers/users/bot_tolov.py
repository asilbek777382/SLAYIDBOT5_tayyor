import logging
from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.types import (
    CallbackQuery, Message,
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from loader import bot, db
from handlers.users.buyruqlar import tolov

router = Router()
logging.basicConfig(level=logging.INFO)

# Test token (o'zgartiring productionga o'tganda)
PAYMENTS_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'

# 💳 Narx obyektini tayyorlab qo'yamiz (rubl formatida, 100 ga ko'paytirilgan)
def get_price(amount: int):
    return [LabeledPrice(label="To'lov:", amount=amount * 100)]

# ▶️ CLICK tanlanganda
@router.callback_query(F.data == 'click', StateFilter(tolov.tanlov))
async def click_payment_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(tolov.click)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5000 so'm", callback_data="5000")],
        [InlineKeyboardButton(text="10000 so'm", callback_data="10000")],
        [InlineKeyboardButton(text="20000 so'm", callback_data="20000"),
         InlineKeyboardButton(text="50000 so'm", callback_data="50000")],
        [InlineKeyboardButton(text="Ortga 🔙", callback_data="ortga")]
    ])
    msg = await callback.message.answer("✅To'lov shakli: 🔵Click\nQancha to'lov qilmoqchisiz?", reply_markup=keyboard)
    await state.update_data(m=msg.message_id)

# 🔙 Ortga qaytish
@router.callback_query(F.data == 'ortga', StateFilter(tolov.click))
async def back_to_payment_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("m")
    if msg_id:
        try:
            await bot.delete_message(callback.from_user.id, msg_id)
        except:
            pass

    await state.set_state(tolov.tanlov)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 PAYME", callback_data="payme"),
         InlineKeyboardButton(text="🔵 CLICK", callback_data="click")],
        [InlineKeyboardButton(text="💳 KARTA ORQALI", callback_data="karta")]
    ])
    msg = await callback.message.answer("Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇", reply_markup=keyboard)
    await state.update_data(m=msg.message_id)

# 💸 CLICK summani tanlaganda
@router.callback_query(StateFilter(tolov.click))
async def process_amount_callback(callback: CallbackQuery, state: FSMContext):
    amount_text = callback.data.strip()
    if not amount_text.isdigit():
        await callback.answer("Noto'g'ri to'lov summasi!")
        return

    amount = int(amount_text)
    data = await state.get_data()
    msg_id = data.get("m")
    if msg_id:
        try:
            await bot.delete_message(callback.from_user.id, msg_id)
        except:
            pass

    if "TEST" in PAYMENTS_TOKEN:
        await bot.send_message(callback.from_user.id, "💡 Bu test to'lov hisobidir.")

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Premium obuna",
        description=f"{amount} so'mlik to'lov",
        provider_token=PAYMENTS_TOKEN,
        currency="UZS",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=get_price(amount),
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

# 🧾 To'lov oldidan tasdiq (majburiy)
@router.pre_checkout_query()
async def pre_checkout_query_handler(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

# ✅ To'lov muvaffaqiyatli bo'lsa
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: Message):
    payment = message.successful_payment
    amount = payment.total_amount // 100
    currency = payment.currency

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"✅ To'lov {amount} {currency} miqdorida muvaffaqiyatli amalga oshirildi!"
    )
