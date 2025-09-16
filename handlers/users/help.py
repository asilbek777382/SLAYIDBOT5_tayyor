from aiogram import types
from aiogram.filters import Command, CommandStart

from aiogram import Router, F
from aiogram.types import Message


from loader import dp, db

router = Router()

@router.message(F.text == "/help")
async def help_handler(message: Message):
    ol=db.select_user(tg_user=message.from_user.id)
    til=ol[4]
    if til=='uz':
          text=(f"📖Botdan foydalanish qo'llanmasi:\n\n"
                f"Taqdimotga oid (video - /vid):\n"
                f"📌 Mavzu - Taqdimot mavzusi.\n"
                f"👤 Muallif - Taqdimotda muallifining ismi-familiyasi.\n"
                f"🧮 Sahifalar soni - Taqdimotda nechta sahifa bo'lishi kerakligi.\n"
                f"🇺🇿 Til - Taqdimot qaysi tilda bo'lishi.\n"
                f"📋 Rejalar - Rejalar mavzuga oid bo'ladi va avtomatik kiritiladi! Rejalar soni standard 3ta.\n\n"
                f"📕Taqdimot - tugmasi bosilgandan keyin, quyidagi bosqichlardan ketma-ket o'tilib taqdimot yaratiladi:\n"
                f"1. Mavzu kiritish - Kerakli taqdimot mavzusini kiritish.\n"
                f"2. Muallif ism-familiyasi(to'liq) - Taqdimot tayyorlovchi.\n"
                f"3. Ma'lumotlarni tasdiqlash - Taqdimot mavzusi, muallif ism-familiyasi, sahifalar soni va tasdiqlash.\n\n"
                f"📘Referat/Mustaqil ish\n"
                f"1. Ko'rsatilgan tartibda so'ralgan ma'lumotlarni kiriting.\n\n"
                f"🕹Buyruqlarga oid:\n"
                f"/my - ma'lumotlaringizni ko'rish uchun.\n"
                f"/new - yangi taqdimot tayorlashni boshlash uchun.\n"
                f"/info - ma'lumot qidirish uchun.\n"
                f"/buy - kartaga to'lov qilish orqali, balansingizni to'ldiring.\n"
                f"/chek - to'lov qilganingizdan so'ng chekni skrenshot ko'rinishida yuborasiz va admin ko'rib chiqib tasdiqlaydi, sizning balansingizga pul tushadi.\n"
                f"/vid - taqdimot qilish uchun video qo'llanma.\n"
                f"/help - qo'shimcha yordamlaar uchun.\n\n"
                f"⁉️Qo'shimcha:\n"
                f"1. Referal a'zolaringiz har bir tayorlagan hujjati uchun sizga 50 so'm bonus beriladi.\n"
                f"2. Referal a'zolaringiz har bir qilgan to'lovidan sizga 5% beriladi (Ex: 20 000 so'm uchun - 500 so'm).\n\n"
                f"✍️Chat - @slaydai_chat\n"
                f"🆕Bot yangilanishlari - @slaydai_news")
          await message.answer(text=text)
    if til=='ru':
          text=(f"📖Руководство пользователя бота:\n\n"
                  f"Презентация (видео - /vid):\n"
                  f"📌 Тема - Тема презентации.\n"
                  f"👤 Автор - Имя и фамилия автора презентации.\n"
                  f"🧮 Количество страниц - Сколько страниц должно быть в презентации.\n"
                  f"🇺🇿 Язык - На каком языке должна быть презентация.\n"
                  f"📋 Планы - Планы привязаны к темам и добавляются автоматически! Стандартное количество планов - 3.\n\n"
                  f"📕Презентация - После нажатия кнопки выполняются следующие шаги для создания презентации:\n"
                  f"1. Введите тему - Введите желаемую тему презентации.\n"
                  f"2. Имя автора (полностью) - Создатель презентации.\n"
                  f"3. Подтверждение данных - Тема презентации, имя автора, количество страниц и Подтверждение.\n\n"
                  f"📘Справочная/Самостоятельная работа\n"
                  f"1. Введите запрашиваемую информацию в указанном порядке.\n\n"
                  f"🕹По вопросам заказов:\n"
                  f"/my - для просмотра информации.\n"
                  f"/new - для начала подготовки новой презентации.\n"
                  f"/info - для поиска информации.\n"
                  f"/buy - для пополнения баланса на карту.\n"
                  f"/check - после оплаты вы отправляете чек в виде скриншота, администратор его проверяет и подтверждает, деньги зачисляются на ваш баланс.\n"
                  f"/vid - видеоинструкция по созданию презентации.\n"
                  f"/help - для получения дополнительной помощи.\n\n"
                  f"⁉️Дополнительно:\n"
                  f"1. Ваши рефералы получат каждый... Вы получите бонус в размере 50 сумов за каждый предоставленный вами документ. Подготовьтесь.\n"
                  f"2. Вы будете получать 5% с каждого платежа, совершённого вашими рефералами (например, за 20 000 сумов — 500 сумов).\n\n"
                  f"✍️Чат — @slaydai_chat\n"
                  f"🆕Обновления бота — @slaydai_news")
          await message.answer(text=text)
    if til=='en':
          text=(f"📖Bot User Guide:\n\n"
f"Presentation (video - /vid):\n"
f"📌 Topic - Topic of the presentation.\n"
f"👤 Author - First and last name of the presentation author.\n"
f"🧮 Number of Pages - How many pages should the presentation have.\n"
f"🇺🇿 Language - What language should the presentation be in.\n"
f"📋 Plans - Plans are linked to topics and are added automatically! The standard number of plans is 3.\n\n"
f"📕Presentation - After clicking the button, the following steps are performed to create a presentation:\n"
f"1. Enter Topic - Enter the desired topic of the presentation.\n"
f"2. Author Name (Full) - The creator of the presentation.\n"
f"3. Confirmation Data - Presentation Topic, Author Name, Number of Pages, and Confirmation.\n\n"
f"📘Help/Independent Work\n"
f"1. Enter the requested information in the order specified.\n\n"
f"🕹For questions about orders:\n"
f"/my - to view information.\n"
f"/new - to start preparing a new presentation.\n"
f"/info - to search for information.\n"
f"/buy - to top up your balance on the card.\n"
f"/check - after payment, you send a receipt in the form of a screenshot, the administrator checks and confirms it, the money is credited to your balance.\n"
f"/vid - video instructions for creating a presentation.\n"
f"/help - for additional assistance.\n\n"
f"⁉️Additionally:\n"
f"1. Your referrals will receive each... You will receive a bonus of 50 soums for each document you provide. Get ready.\n"
f"2. You will receive 5% of each payment made by your referrals (for example, for 20,000 sums - 500 sums).\n\n"
f"✍️Chat - @slaydai_chat\n"
f"🆕Bot updates - @slaydai_news")
          await message.answer(text=text)

@router.callback_query(F.data == "qollanma_en")
@router.callback_query(F.data == "qollanma_ru")
@router.callback_query(F.data == "qollanma")
async def help_handler(message: types.CallbackQuery):
    ol=db.select_user(tg_user=message.from_user.id)
    til=ol[4]
    if til=='uz':
          text=(f"📖Botdan foydalanish qo'llanmasi:\n\n"
                f"Taqdimotga oid (video - /vid):\n"
                f"📌 Mavzu - Taqdimot mavzusi.\n"
                f"👤 Muallif - Taqdimotda muallifining ismi-familiyasi.\n"
                f"🧮 Sahifalar soni - Taqdimotda nechta sahifa bo'lishi kerakligi.\n"
                f"🇺🇿 Til - Taqdimot qaysi tilda bo'lishi.\n"
                f"📋 Rejalar - Rejalar mavzuga oid bo'ladi va avtomatik kiritiladi! Rejalar soni standard 3ta.\n\n"
                f"📕Taqdimot - tugmasi bosilgandan keyin, quyidagi bosqichlardan ketma-ket o'tilib taqdimot yaratiladi:\n"
                f"1. Mavzu kiritish - Kerakli taqdimot mavzusini kiritish.\n"
                f"2. Muallif ism-familiyasi(to'liq) - Taqdimot tayyorlovchi.\n"
                f"3. Ma'lumotlarni tasdiqlash - Taqdimot mavzusi, muallif ism-familiyasi, sahifalar soni va tasdiqlash.\n\n"
                f"📘Referat/Mustaqil ish\n"
                f"1. Ko'rsatilgan tartibda so'ralgan ma'lumotlarni kiriting.\n\n"
                f"🕹Buyruqlarga oid:\n"
                f"/my - ma'lumotlaringizni ko'rish uchun.\n"
                f"/new - yangi taqdimot tayorlashni boshlash uchun.\n"
                f"/info - ma'lumot qidirish uchun.\n"
                f"/buy - kartaga to'lov qilish orqali, balansingizni to'ldiring.\n"
                f"/chek - to'lov qilganingizdan so'ng chekni skrenshot ko'rinishida yuborasiz va admin ko'rib chiqib tasdiqlaydi, sizning balansingizga pul tushadi.\n"
                f"/vid - taqdimot qilish uchun video qo'llanma.\n"
                f"/help - qo'shimcha yordamlaar uchun.\n\n"
                f"⁉️Qo'shimcha:\n"
                f"1. Referal a'zolaringiz har bir tayorlagan hujjati uchun sizga 50 so'm bonus beriladi.\n"
                f"2. Referal a'zolaringiz har bir qilgan to'lovidan sizga 5% beriladi (Ex: 20 000 so'm uchun - 500 so'm).\n\n"
                f"✍️Chat - @slaydai_chat\n"
                f"🆕Bot yangilanishlari - @slaydai_news")
          await message.message.answer(text=text)
    if til=='ru':
          text=(f"📖Руководство пользователя бота:\n\n"
                  f"Презентация (видео - /vid):\n"
                  f"📌 Тема - Тема презентации.\n"
                  f"👤 Автор - Имя и фамилия автора презентации.\n"
                  f"🧮 Количество страниц - Сколько страниц должно быть в презентации.\n"
                  f"🇺🇿 Язык - На каком языке должна быть презентация.\n"
                  f"📋 Планы - Планы привязаны к темам и добавляются автоматически! Стандартное количество планов - 3.\n\n"
                  f"📕Презентация - После нажатия кнопки выполняются следующие шаги для создания презентации:\n"
                  f"1. Введите тему - Введите желаемую тему презентации.\n"
                  f"2. Имя автора (полностью) - Создатель презентации.\n"
                  f"3. Подтверждение данных - Тема презентации, имя автора, количество страниц и Подтверждение.\n\n"
                  f"📘Справочная/Самостоятельная работа\n"
                  f"1. Введите запрашиваемую информацию в указанном порядке.\n\n"
                  f"🕹По вопросам заказов:\n"
                  f"/my - для просмотра информации.\n"
                  f"/new - для начала подготовки новой презентации.\n"
                  f"/info - для поиска информации.\n"
                  f"/buy - для пополнения баланса на карту.\n"
                  f"/check - после оплаты вы отправляете чек в виде скриншота, администратор его проверяет и подтверждает, деньги зачисляются на ваш баланс.\n"
                  f"/vid - видеоинструкция по созданию презентации.\n"
                  f"/help - для получения дополнительной помощи.\n\n"
                  f"⁉️Дополнительно:\n"
                  f"1. Ваши рефералы получат каждый... Вы получите бонус в размере 50 сумов за каждый предоставленный вами документ. Подготовьтесь.\n"
                  f"2. Вы будете получать 5% с каждого платежа, совершённого вашими рефералами (например, за 20 000 сумов — 500 сумов).\n\n"
                  f"✍️Чат — @slaydai_chat\n"
                  f"🆕Обновления бота — @slaydai_news")
          await message.message.answer(text=text)
    if til=='en':
          text=(f"📖Bot User Guide:\n\n"
f"Presentation (video - /vid):\n"
f"📌 Topic - Topic of the presentation.\n"
f"👤 Author - First and last name of the presentation author.\n"
f"🧮 Number of Pages - How many pages should the presentation have.\n"
f"🇺🇿 Language - What language should the presentation be in.\n"
f"📋 Plans - Plans are linked to topics and are added automatically! The standard number of plans is 3.\n\n"
f"📕Presentation - After clicking the button, the following steps are performed to create a presentation:\n"
f"1. Enter Topic - Enter the desired topic of the presentation.\n"
f"2. Author Name (Full) - The creator of the presentation.\n"
f"3. Confirmation Data - Presentation Topic, Author Name, Number of Pages, and Confirmation.\n\n"
f"📘Help/Independent Work\n"
f"1. Enter the requested information in the order specified.\n\n"
f"🕹For questions about orders:\n"
f"/my - to view information.\n"
f"/new - to start preparing a new presentation.\n"
f"/info - to search for information.\n"
f"/buy - to top up your balance on the card.\n"
f"/check - after payment, you send a receipt in the form of a screenshot, the administrator checks and confirms it, the money is credited to your balance.\n"
f"/vid - video instructions for creating a presentation.\n"
f"/help - for additional assistance.\n\n"
f"⁉️Additionally:\n"
f"1. Your referrals will receive each... You will receive a bonus of 50 soums for each document you provide. Get ready.\n"
f"2. You will receive 5% of each payment made by your referrals (for example, for 20,000 sums - 500 sums).\n\n"
f"✍️Chat - @slaydai_chat\n"
f"🆕Bot updates - @slaydai_news")
          await message.message.answer(text=text)
