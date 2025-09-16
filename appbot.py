# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
# BOT_TOKEN = "7621722847:AAHMMr5hZZwqxp_WVI731JzgeBS2OEpIpd8"
# # Dastlabki taqiqlangan so‘zlar
# restricted_words = set([
#     "xoʻp boʻladi", "Xoʻp boʻladi", "XOʻP BOʻLADI",
#     "xop bo'ladi", "xop bo’ladi", "xop bo`ladi", "xop boladi",
#     "xup bo'ladi", "xup bo’ladi", "xup bo`ladi", "xup boladi",
#     "xob bo'ladi", "xob boladi",
#     "xop boladi", "xop buladi", "xup boladi", "xup buladi",
#     "xopbo'ladi", "xupbo'ladi", "xopbuladi", "xupbuladi",
#     "xopboladi", "xupboladi", "xobboladi",
#     "хоп булади", "хуп булади", "хоб булади", "хоп болади", "хуп болади", "хоб болади",
#     "хупбулади", "хопболади",
#     "xop", "xup", "xob", "xoʻp", "xo‘p", "xo’p", "xōp", "xö‘p",
#     "хоп", "хуп", "хоб", "hop", "hup", "hob",
#     "xop boladi.", "xop boladi!", "xop boladi?", "(xop boladi)", "xop boladi,", "xop boladi🤝",
# ])
# # ❌ Foydalanuvchi xabari tekshirish
# async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message:
#         return
#     user_message = update.message.text.lower()
#     for word in restricted_words:
#         if word in user_message:
#             try:
#                 await update.message.delete()
#                 await context.bot.send_message(
#                     chat_id=update.message.chat_id,
#                     text=f"⚠️ Огоҳлантириш, {update.message.from_user.first_name}: "
#                          f"таъқиқланган сўздан фойдаландингиз."
#                 )
#             except Exception as e:
#                 print(f"Хабарни ўчиришда хатолик: {e}")
#             break
# # ✅ /addban buyrug‘i orqali yangi so‘z qo‘shish
# async def add_banned_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not context.args:
#         await update.message.reply_text("❌ Иложсиз: Қандай сўзни қўшишни ёзинг. Масалан: /addban test")
#         return
#     new_word = " ".join(context.args).lower()
#     if new_word in restricted_words:
#         await update.message.reply_text(f"❗️ '{new_word}' аллақачон таъқиқланган.")
#     else:
#         restricted_words.add(new_word)
#         await update.message.reply_text(f"✅ '{new_word}' сўзи муваффақиятли таъқиқланди!")
# # 🔄 Bosh bot funksiyasi
# def main():
#     application = ApplicationBuilder().token(BOT_TOKEN).build()
#     # Tekshiruvchi handler
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
#     # Buyruq orqali yangi taqiqlangan so‘z qo‘shish
#     application.add_handler(CommandHandler("addban", add_banned_word))
#     application.run_polling()
#     print("Wokring telegram bot ...")
# if __name__ == "__main__":
#     main()
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import logging

# 🔑 Bot token
BOT_TOKEN = "7621722847:AAHMMr5hZZwqxp_WVI731JzgeBS2OEpIpd8"

# 📋 Dastlabki taqiqlangan so‘zlar
restricted_words = set([
    "xoʻp boʻladi", "Xoʻp бўladi", "XOʻP BOʻLADI",
    "xop bo'ladi", "xop bo’ladi", "xop bo`ladi", "xop boladi",
    "xup bo'ladi", "xup bo’ladi", "xup bo`ladi", "xup boladi",
    "xob bo'ladi", "xob boladi",
    "xop boladi", "xop buladi", "xup boladi", "xup buladi",
    "xopbo'ladi", "xupbo'ladi", "xopbuladi", "xupbuladi",
    "xopboladi", "xupboladi", "xobboladi",
    "хоп булади", "хуп булади", "хоб булади", "хоп болади", "хуп болади", "хоб болади",
    "хупбулади", "хопболади",
    "xop", "xup", "xob", "xoʻp", "xo‘p", "xo’p", "xōp", "xö‘p",
    "хоп", "хуп", "хоб", "hop", "hup", "hob",
    "xop boladi.", "xop boladi!", "xop boladi?", "(xop boladi)", "xop boladi,", "xop boladi🤝",
])

# 🚫 Oddiy xabarlarni tekshirish
async def check_message(message: Message):
    user_message = message.text.lower()
    for word in restricted_words:
        if word in user_message:
            try:
                await message.delete()
                await message.answer(
                    f"⚠️ Огоҳлантириш, {message.from_user.first_name}: "
                    f"таъқиқланган сўздан фойдаландингиз."
                )
            except Exception as e:
                logging.error(f"Хабарни ўчиришда хатолик: {e}")
            break

# ✅ /addban buyrug‘i orqali yangi so‘z qo‘shish
async def add_banned_word(message: Message):
    parts = message.text.split(maxsplit=1)  # /addban dan keyingi matnni olish
    if len(parts) < 2:
        await message.answer("❌ Иложсиз: Қандай сўзни қўшишни ёзинг. Масалан: /addban test")
        return

    new_word = parts[1].lower()
    if new_word in restricted_words:
        await message.answer(f"❗️ '{new_word}' аллақачон таъқиқланган.")
    else:
        restricted_words.add(new_word)
        await message.answer(f"✅ '{new_word}' сўзи муваффақиятли таъқиқланди!")

# 🔄 Botni ishga tushirish
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Xabarlarni tekshiruvchi handler
    dp.message.register(check_message, F.text & ~F.text.startswith("/"))

    # /addban buyrug‘i
    dp.message.register(add_banned_word, Command(commands=["addban"]))

    print("🚀 Bot ishga tushdi ...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
