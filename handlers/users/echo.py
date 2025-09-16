# import time
#
# from aiogram import types
# from aiogram.types import ContentType
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters import BoundFilter
# from aiogram.types import MessageEntityType
# from aiogram.utils.markdown import link
#
# from filters.kanal import shaxsiy
#
#
#
# from loader import dp, bot
#
#
# # Echo bot
# @dp.message_handler(shaxsiy(),content_types=ContentType.NEW_CHAT_MEMBERS)
# async def bot_echo(message: types.Message):
#     ism=message.new_chat_members[0].first_name
#     await message.answer(f"Assalomu alaykum {ism} kanalga xush kelibsiz")
#
#
#
#
#
#
#
#
#
#
#
# @dp.message_handler(shaxsiy(),content_types=ContentType.TEXT)
# async def bot_echo(message: types.Message):
#     print(message.text[:1])
#
#     sok=['bla','BLA','Bla','bLa','blA',
#          'Suka','Suka','SUKA','SukA',
#          "Gandon",'gandon','GANDON',
#          'Jalab','jallab','Jallab','JALLAB','jalab','Jalab','JALAB',
#          'ske','SKE','Ske'
#          'Porno','porno','PORNO','seks','SEKS','Seks','skish','Skish','SKISH','SKTIRISH','sktirish',
#          'faktu','Fakyu','FAKYU','faku'
#          'QOTO','QOTOQ','Qotoq','qotoq','Qoto',"qotoq"]
#
#     if 'https'==str(message.text[:5]):
#         await message.delete()
#         a = await message.answer(f"Iltimos kanalga reklama tashlamang. (5)")
#         for s in range(4, -1, -1):
#             time.sleep(1)
#             print(s)
#             await bot.edit_message_text(chat_id=message.chat.id, message_id=a.message_id,
#                                         text=f"Iltimos kanalga reklama tashlamang. ({s})")
#
#
#     if '@'==str(message.text[0]):
#         await message.delete()
#         a = await message.answer(f"Iltimos kanalga reklama tashlamang. (5)")
#         for s in range(4, -1, -1):
#             time.sleep(1)
#             print(s)
#             await bot.edit_message_text(chat_id=message.chat.id, message_id=a.message_id,
#                                         text=f"Iltimos kanalda so'kinmang. ({s})")
#         await bot.delete_message(chat_id=message.chat.id, message_id=a.message_id)
#
#     if message.text in sok:
#         await message.delete()
#         a=await message.answer(f"Iltimos kanalda so'kinmang. (5)")
#         for s in range(4, -1, -1):
#             time.sleep(1)
#             print(s)
#             await bot.edit_message_text(chat_id=message.chat.id,message_id=a.message_id,text=f"Iltimos kanalda so'kinmang. ({s})")
#         await bot.delete_message(chat_id=message.chat.id,message_id=a.message_id)
#
#
# from aiogram.utils.markdown import link
#
#
