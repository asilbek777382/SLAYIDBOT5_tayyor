from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Router, F


router = Router()
from loader import  bot, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from states.state import Admin, kanallar_sozlamalari


@router.message(F.text=="🕹 Majburiy a'zolik",StateFilter(Admin.admin_tanlov))
async def bot_start(message: types.Message,state: FSMContext):
    await message.delete()
    await state.set_state(kanallar_sozlamalari.kanallar_sozlamalari)
    ol = await state.get_data()
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Kanallar ro'yxati")],
            [KeyboardButton(text="➕ Kanallar qo'shish"), KeyboardButton(text="Kanallar o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m = await message.answer(text='Tanlang', reply_markup=reply_buttons)
    await state.update_data({'m_id': m.message_id})


# Ortga
@router.message(F.text=="🔙 Ortga",StateFilter(kanallar_sozlamalari.kanallar_sozlamalari, ))
async def bot_start(message: types.Message, state: FSMContext):
    ol = await state.get_data()
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    await message.delete()
    tg_user = db.select_kanallar(tg_user=message.from_user.id)
    await state.set_state(Admin.admin_tanlov)
    user_ismi = db.select_admin(username=message.from_user.username)
    if tg_user or f'@{user_ismi}':
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
    else:
        pass


@router.message(F.text=="➕ Kanallar qo'shish",StateFilter(kanallar_sozlamalari.kanallar_sozlamalari))
async def bot_start(message: types.Message, state: FSMContext):
    ol = await state.get_data()
    await state.set_state(kanallar_sozlamalari.kanallar_qoshish)
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    await message.delete()
    await message.answer('Kanal manzilini yuboring:')
    await state.set_state(kanallar_sozlamalari.kanallar_manzil_olish)


@router.message(StateFilter(kanallar_sozlamalari.kanallar_manzil_olish))
async def bot_start(message: types.Message, state: FSMContext):
    manzil=message.text
    if manzil[:5] == 'https':
        await message.answer('Kanal ismini yuboring:')
        await state.update_data({'admin_manzili': f"@{manzil[13:]}"})
        await state.set_state(kanallar_sozlamalari.kanallar_ismi_olish)

    else:
        await message.answer('Kanal manzilini qaytatdan yuboring:\n\n'
                             'Misol uchun https://t.me/botsavdosi_devseclab')


@router.message(StateFilter(kanallar_sozlamalari.kanallar_ismi_olish))
async def bot_start(message: types.Message, state: FSMContext):
    olish = await state.get_data()
    admin_manzili = olish.get('admin_manzili')

    db.add_kanallar(tg_user=message.from_user.id, username=admin_manzili, ismi=message.text)

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Kanallar ro'yxati")],
            [KeyboardButton(text="➕ Kanallar qo'shish"), KeyboardButton(text="Kanallar o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m = await message.answer(text='Kanal muvaffaqiyatli qoshildi.', reply_markup=reply_buttons)
    await state.set_state(kanallar_sozlamalari.kanallar_sozlamalari)
    await state.update_data({'m_id': m.message_id})


@router.message(F.text=="Kanallar o'chirish ➖",StateFilter(kanallar_sozlamalari.kanallar_sozlamalari))
async def bot_start(message: types.Message, state: FSMContext):
    ol = await state.get_data()
    await state.set_state(kanallar_sozlamalari.kanallar_ochirish)
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    await message.delete()
    ol = db.select_kanallars()

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    def create_admin_buttons(admins):
        buttons = []

        for idd, tg_user, username, ismi in admins:

                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                         callback_data=str(idd)  # faqat URL bilan
                    )
                ])


        buttons.append([
            InlineKeyboardButton(
                text='🔙 Ortga',
                callback_data=f"ortga"  # faqat callback_data
            )
        ])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    if not ol:
        def create_admin_buttons(admins):
            buttons2 = []
            buttons2.append([
                InlineKeyboardButton(
                    text='🔙 Ortga',
                    callback_data=f"ortga"  # faqat callback_data
                )
            ])
            return InlineKeyboardMarkup(inline_keyboard=buttons2)

        await state.set_state(kanallar_sozlamalari.kanallar_royxati)
        keyboard2 = create_admin_buttons(ol)
        m = await message.answer("Kanallar topilmadi.", reply_markup=keyboard2)
        await state.update_data({'m_id': m.message_id})
    else:

        keyboard = create_admin_buttons(ol)
        m = await message.answer("Kanallar ro‘yxati:", reply_markup=keyboard)
        await state.update_data({'m_id': m.message_id})


# Ortga & tanlaganini ochirish
@router.callback_query(StateFilter(kanallar_sozlamalari.kanallar_ochirish))
async def bot_start(message: CallbackQuery, state: FSMContext):
    mal = message.data
    if mal == 'ortga':
        await state.set_state(kanallar_sozlamalari.kanallar_sozlamalari)
        ol = await state.get_data()
        m_id = ol.get('m_id')
        await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
        reply_buttons = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🗓 Kanallar ro'yxati")],
                [KeyboardButton(text="➕ Kanallar qo'shish"), KeyboardButton(text="Kanallar o'chirish ➖")],
                [KeyboardButton(text="🔙 Ortga")]
            ],
            resize_keyboard=True
        )

        m = await message.message.answer(text='Tanlang', reply_markup=reply_buttons)
        await state.update_data({'m_id': m.message_id})

    else:
        db.delete_kanallar(id=mal)
        ol = await state.get_data()
        await state.set_state(kanallar_sozlamalari.kanallar_royxati)
        m_id = ol.get('m_id')
        await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)

        ol = db.select_kanallars()

        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

        def create_admin_buttons(admins):
            buttons = []

            for idd, tg_user, username, ismi in admins:

                    buttons.append([
                        InlineKeyboardButton(
                            text=ismi,
                              # faqat URL bilan
                        )
                    ])


            buttons.append([
                InlineKeyboardButton(
                    text='🔙 Ortga',
                    callback_data=f"ortga"  # faqat callback_data
                )
            ])
            return InlineKeyboardMarkup(inline_keyboard=buttons)

        if not ol:
            def create_admin_buttons(admins):
                buttons2 = []
                buttons2.append([
                    InlineKeyboardButton(
                        text='🔙 Ortga',
                        callback_data=f"ortga"  # faqat callback_data
                    )
                ])
                return InlineKeyboardMarkup(inline_keyboard=buttons2)


            keyboard2 = create_admin_buttons(ol)
            m = await message.message.answer("Kanallar topilmadi.", reply_markup=keyboard2)
            await state.update_data({'m_id': m.message_id})
        else:

            keyboard = create_admin_buttons(ol)
            m = await message.message.answer("Kanallar ro‘yxati:", reply_markup=keyboard)
            await state.update_data({'m_id': m.message_id})


@router.message(F.text=="🗓 Kanallar ro'yxati",StateFilter(kanallar_sozlamalari.kanallar_sozlamalari))
async def bot_start(message: types.Message, state: FSMContext):
    ol = await state.get_data()
    await state.set_state(kanallar_sozlamalari.kanallar_royxati)
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    await message.delete()
    ol = db.select_kanallars()

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    def create_admin_buttons(admins):
        buttons = []

        for idd, tg_user, username, ismi in admins:

                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                        url=f"https://t.me/{username[1:]}"  # faqat URL bilan
                    )
                ])


        buttons.append([
            InlineKeyboardButton(
                text='🔙 Ortga',
                callback_data=f"ortga"  # faqat callback_data
            )
        ])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    if not ol:
        def create_admin_buttons(admins):
            buttons2 = []
            buttons2.append([
                InlineKeyboardButton(
                    text='🔙 Ortga',
                    callback_data=f"ortga"  # faqat callback_data
                )
            ])
            return InlineKeyboardMarkup(inline_keyboard=buttons2)

        await state.set_state(kanallar_sozlamalari.kanallar_royxati)
        keyboard2 = create_admin_buttons(ol)
        m=await message.answer("Kanallar topilmadi.",reply_markup=keyboard2)
        await state.update_data({'m_id': m.message_id})
    else:

        keyboard = create_admin_buttons(ol)
        m = await message.answer("Kanallar ro‘yxati:", reply_markup=keyboard)
        await state.update_data({'m_id': m.message_id})


# Ortga
@router.callback_query(StateFilter(kanallar_sozlamalari.kanallar_royxati))
async def bot_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(kanallar_sozlamalari.kanallar_sozlamalari)
    ol = await state.get_data()
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Kanallar ro'yxati")],
            [KeyboardButton(text="➕ Kanallar qo'shish"), KeyboardButton(text="Kanallar o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m = await message.message.answer(text='Tanlang', reply_markup=reply_buttons)
    await state.update_data({'m_id': m.message_id})
