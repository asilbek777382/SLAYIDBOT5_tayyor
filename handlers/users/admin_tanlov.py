from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Router, F
from aiogram.types import Message


from loader import dp


router = Router()

from loader import  bot, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from states.state import Admin, admin_sozlamalari, bot_azolariga_xabar_yuborish, guruxlarga_xabar_yuborish, \
    bitta_azoga_xabar_yuborish, statistika

from aiogram import Router



router = Router()




@router.message(F.text=='⚙️ Admin sozlamalari',StateFilter(Admin.admin_tanlov))
async def bot_start(message: types.Message,state: FSMContext):
    await message.delete()
    await state.set_state(admin_sozlamalari.admin_sozlamalari)
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Adminlar ro'yxati")],
            [KeyboardButton(text="➕ Admin qo'shish"),KeyboardButton(text="Admin o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m=await message.answer(text='Tanlang', reply_markup=reply_buttons)
    await state.update_data({'m_id': m.message_id})
#Ortga
@router.message(F.text=='🔙 Ortga',StateFilter(admin_sozlamalari.admin_sozlamalari))
async def bot_start(message: types.Message,state: FSMContext):
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    await message.delete()
    tg_user = db.select_admin(tg_user=message.from_user.id)
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


@router.message(F.text=="➕ Admin qo'shish",StateFilter(admin_sozlamalari.admin_sozlamalari))
async def bot_start(message: types.Message,state: FSMContext):

    ol = await state.get_data()
    await state.set_state(admin_sozlamalari.admin_qoshish)
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    await message.delete()
    await message.answer('Admin usernamesini yoki ID raqamini yuboring:')
    await state.set_state(admin_sozlamalari.admin_manzil_olish)

@router.message(StateFilter(admin_sozlamalari.admin_manzil_olish))
async def bot_start(message: types.Message,state: FSMContext):
    await message.answer('Admin ismini kiriting.')
    await state.update_data({'admin_manzili': message.text})
    await state.set_state(admin_sozlamalari.admin_ismi_olish)
@router.message(StateFilter(admin_sozlamalari.admin_ismi_olish))
async def bot_start(message: types.Message,state: FSMContext):
    olish=await state.get_data()
    admin_manzili=olish.get('admin_manzili')

    if admin_manzili[0] == '@':
            db.add_admin(username=admin_manzili,tg_user=None,ismi=message.text)


    else:
        db.add_admin(tg_user=admin_manzili,username=None,ismi=message.text)

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Adminlar ro'yxati")],
            [KeyboardButton(text="➕ Admin qo'shish"), KeyboardButton(text="Admin o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m = await message.answer(text='Admin muvaffaqiyatli qoshildi.', reply_markup=reply_buttons)
    await state.set_state(admin_sozlamalari.admin_sozlamalari)
    await state.update_data({'m_id': m.message_id})


@router.message(F.text=="Admin o'chirish ➖",StateFilter(admin_sozlamalari.admin_sozlamalari))
async def bot_start(message: types.Message,state: FSMContext):
    ol=await state.get_data()
    await state.set_state(admin_sozlamalari.admin_ochirish)
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    await message.delete()
    ol = db.select_admins()

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    def create_admin_buttons(admins):
        buttons = []

        for idd, tg_user, username, ismi in admins:
            if username:  # Agar username mavjud bo‘lsa (None emas, bo‘sh emas)
                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                        url=f"https://t.me/{username.lstrip('@')}",callback_data=idd  # faqat URL bilan
                    )
                ])
            else:
                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                        callback_data=f"{idd}"  # faqat callback_data
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
        m = await message.answer("Adminlar topilmadi.", reply_markup=keyboard2)
        await state.update_data({'m_id': m.message_id})
    else:

        keyboard = create_admin_buttons(ol)
        m=await message.answer("Adminlar ro‘yxati:", reply_markup=keyboard)
        await state.update_data({'m_id': m.message_id})
# Ortga & tanlaganini ochirish
@router.callback_query(StateFilter(admin_sozlamalari.admin_ochirish))
async def bot_start(message: CallbackQuery,state: FSMContext):
    mal=message.data
    if mal == 'ortga':
        await state.set_state(admin_sozlamalari.admin_sozlamalari)
        ol=await state.get_data()
        m_id=  ol.get('m_id')
        await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
        reply_buttons = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🗓 Adminlar ro'yxati")],
                [KeyboardButton(text="➕ Admin qo'shish"),KeyboardButton(text="Admin o'chirish ➖")],
                [KeyboardButton(text="🔙 Ortga")]
            ],
            resize_keyboard=True
        )

        m=await message.message.answer(text='Tanlang', reply_markup=reply_buttons)
        await state.update_data({'m_id': m.message_id})

    else:
        db.delete_admin(id=mal)
        ol = await state.get_data()
        await state.set_state(admin_sozlamalari.admin_royxati)
        m_id = ol.get('m_id')
        await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)

        ol = db.select_admins()

        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

        def create_admin_buttons(admins):
            buttons = []

            for idd, tg_user, username, ismi in admins:
                if username:  # Agar username mavjud bo‘lsa (None emas, bo‘sh emas)
                    buttons.append([
                        InlineKeyboardButton(
                            text=ismi,
                            url=f"https://t.me/{username.lstrip('@')}"  # faqat URL bilan
                        )
                    ])
                else:
                    buttons.append([
                        InlineKeyboardButton(
                            text=ismi,
                            callback_data=f"admin:{idd}"  # faqat callback_data
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
            m = await message.message.answer("Adminlar ro‘yxati:", reply_markup=keyboard)
            await state.update_data({'m_id': m.message_id})


@router.message(F.text=="🗓 Adminlar ro'yxati",StateFilter(admin_sozlamalari.admin_sozlamalari))
async def bot_start(message: types.Message,state: FSMContext):
    ol=await state.get_data()
    await state.set_state(admin_sozlamalari.admin_royxati)
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    await message.delete()
    ol = db.select_admins()

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    def create_admin_buttons(admins):
        buttons = []

        for idd, tg_user, username, ismi in admins:
            if username:  # Agar username mavjud bo‘lsa (None emas, bo‘sh emas)
                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                        url=f"https://t.me/{username.lstrip('@')}"  # faqat URL bilan
                    )
                ])
            else:
                buttons.append([
                    InlineKeyboardButton(
                        text=ismi,
                        callback_data=f"admin:{idd}"  # faqat callback_data
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
        m = await message.answer("Adminlar topilmadi.", reply_markup=keyboard2)
        await state.update_data({'m_id': m.message_id})
    else:

        keyboard = create_admin_buttons(ol)
        m=await message.answer("Adminlar ro‘yxati:", reply_markup=keyboard)
        await state.update_data({'m_id': m.message_id})
# Ortga
@router.callback_query(StateFilter(admin_sozlamalari.admin_royxati))
async def bot_start(message: CallbackQuery,state: FSMContext):
    await state.set_state(admin_sozlamalari.admin_sozlamalari)
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Adminlar ro'yxati")],
            [KeyboardButton(text="➕ Admin qo'shish"),KeyboardButton(text="Admin o'chirish ➖")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    m=await message.message.answer(text='Tanlang', reply_markup=reply_buttons)
    await state.update_data({'m_id': m.message_id})







@router.callback_query(F.data=="bot_azolariga_xabar_yuborish",StateFilter(Admin.admin_tanlov))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol = await state.get_data()

    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ortga 🔙", callback_data="back")],


    ])
    m=await message.message.answer(text="📨Foydalanuvchilarga xabarni yuboring:",reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await state.set_state(bot_azolariga_xabar_yuborish.bot_azolariga_xabar_yuborish_xabarni_olish)

@router.callback_query( F.data =="back",StateFilter(bot_azolariga_xabar_yuborish.bot_azolariga_xabar_yuborish_xabarni_olish))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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

    m = await message.message.answer(text='Tanlang', reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await message.message.answer(text='Quyidagilardan tugmalardan birini tanlang:', reply_markup=reply_buttons)
    await state.set_state(Admin.admin_tanlov)

@router.message(
    StateFilter(bot_azolariga_xabar_yuborish.bot_azolariga_xabar_yuborish_xabarni_olish),
    F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'}))
async def bot_start(message: types.Message, state: FSMContext):
    users = db.select_all_users()

    sender_id = message.from_user.id

    for user in users:
        user_id = user[1]

        if int(user_id) == sender_id:
            pass  # o'ziga yuborilmasin
        else:

            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
            except Exception as e:
                print(f"❌ {user_id} ga yuborilmadi.")

    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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








@router.callback_query(F.data =="guruxlarga_xabar_yuborish",StateFilter(Admin.admin_tanlov ))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol = await state.get_data()

    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ortga 🔙", callback_data="back")],


    ])
    m=await message.message.answer(text="📨Guruxlarga xabarni yuboring:",reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await state.set_state(guruxlarga_xabar_yuborish.guruxlarga_xabar_yuborish)

@router.callback_query(F.data == "back",StateFilter(guruxlarga_xabar_yuborish.guruxlarga_xabar_yuborish))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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

    m = await message.message.answer(text='Tanlang', reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await message.message.answer(text='Quyidagilardan tugmalardan birini tanlang:', reply_markup=reply_buttons)
    await state.set_state(Admin.admin_tanlov)

@router.message(StateFilter(guruxlarga_xabar_yuborish.guruxlarga_xabar_yuborish), F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'})
)
async def bot_start(message: types.Message, state: FSMContext):
    users = db.select_kanallars()
    print("🔍 Foydalanuvchilar:", users)
    print("📷 Xabar ID:", message.message_id)
    print("📷 Chat ID:", message.chat.id)

    for user in users:
        user_id = user[2]

        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except Exception as e:
            print(f"❌ {user_id} ga yuborilmadi. Sabab: {e}")

    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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







@router.callback_query(F.data=="bitta_azoga_xabar_yuborish",StateFilter(Admin.admin_tanlov))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol = await state.get_data()

    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ortga 🔙", callback_data="back")],


    ])
    m=await message.message.answer(text="Xabar oluvchini ID yoki usernamesini yuboring:",reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})


    await state.set_state(bitta_azoga_xabar_yuborish.bitta_azoga_xabar_yuborish)

@router.message(StateFilter(bitta_azoga_xabar_yuborish.bitta_azoga_xabar_yuborish))
async def bot_start(message: types.Message, state: FSMContext):

        tg=db.select_user(tg_user=message.text)
        idd=db.select_user(id=message.text)
        if tg or idd:


            await state.update_data({'xabar': message.text})
            await message.answer('📨Foydalanuvchiga xabarni yuboring:')
            await state.set_state(bitta_azoga_xabar_yuborish.bitta_azoga_xabar_yuborish_oluvchi)
        else:
            await message.answer('Bunday ID yoki username dagi foydalanuvchi topilmadi🚫')
@router.message(StateFilter(bitta_azoga_xabar_yuborish.bitta_azoga_xabar_yuborish_oluvchi), F.content_type.in_({'text', 'photo', 'video', 'audio', 'document', 'animation'})
)
async def bot_start(message: types.Message, state: FSMContext):
    mal=await state.get_data()
    xabar=mal.get('xabar')
    manzil=message.text
    try:


            await bot.copy_message(
                chat_id=manzil,
                from_chat_id=message.from_user.id,
                message_id=message.message_id
            )


    except:

        foy=db.select_user(id=xabar)
        try:
            await bot.copy_message(
                chat_id=foy[1],
                from_chat_id=message.from_user.id,
                message_id=message.message_id
            )
        except Exception as e:
            print(f"❌ {foy[1]} ga yuborilmadi. Sabab: {e}")

    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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

    m = await message.answer(text='Xabar yuborildi. ', reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await message.answer(text='Xabaryuborildi tugmalardan birini tanlang:', reply_markup=reply_buttons)
    await state.set_state(Admin.admin_tanlov)


@router.callback_query(F.data =="back",StateFilter(bitta_azoga_xabar_yuborish.bitta_azoga_xabar_yuborish))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol=await state.get_data()
    m_id=  ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id,message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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

    m = await message.message.answer(text='Tanlang', reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await message.message.answer(text='Quyidagilardan tugmalardan birini tanlang:', reply_markup=reply_buttons)
    await state.set_state(Admin.admin_tanlov)



@router.callback_query(F.data =="statistika",StateFilter(Admin.admin_tanlov))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol = await state.get_data()

    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back")],


    ])
    son=db.count_users()
    gurux=db.count_group()
    adminlar=db.count_admin()
    text=(f"📊 Botning a'zolari soni: {son[0]}\n\n"
          f"👥Guruhlar soni: {gurux[0]}\n\n"
          f"👱Jami adminlar soni: {adminlar[0]}\n\n"
)
    m = await message.message.answer(text=text, reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await state.set_state(statistika.statistika)


@router.callback_query(F.data =="back",StateFilter(statistika.statistika))
async def bot_start(message: CallbackQuery,state: FSMContext):
    ol = await state.get_data()
    m_id = ol.get('m_id')
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📮 Botning azolariga xabar yuborish", callback_data="bot_azolariga_xabar_yuborish")],
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

    m = await message.message.answer(text='Tanlang', reply_markup=inline_buttons)
    await state.update_data({'m_id': m.message_id})
    await message.message.answer(text='Quyidagilardan tugmalardan birini tanlang:', reply_markup=reply_buttons)
    await state.set_state(Admin.admin_tanlov)