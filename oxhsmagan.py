# import asyncio
# import os
# import re
# import logging
# import types
# from pathlib import Path
#
# import aiohttp
# from io import BytesIO
# import textwrap
# from aiogram.types import Message, FSInputFile, BufferedInputFile
# from aiogram.fsm.state import StatesGroup, State
# from pptx import Presentation
# from pptx.enum.text import PP_ALIGN
# from pptx.util import Inches, Pt
# from pptx.dml.color import RGBColor
# from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram import Router, F
# from loader import bot, db
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# logging.basicConfig(level=logging.INFO)
# # API keys
#
#
# API_KEY = "sk-cb355fe140f84aad88999f6a3db45634"
# API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
# router = Router()
# # Bot setup
#
#
#
# # User states
# class PresState(StatesGroup):
#     language = State()
#     topic = State()
#     author = State()
#     bg = State()
#     reja_mode = State()
#     reja = State()
#     slide_count = State()
#     bg_upload = State()
#
# user_data = {}
#
#
# async def ask_ai_content(topic: str, band: str, lan: str,max_retries: int = 4) -> str:
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#     if lan == "uz":
#         prompt = (
#             f"Mavzu: {topic}. Band: {band}. Ushbu band bo'yicha 700-800 belgidan iborat to'liq va izohli matn yozing. "
#             "Matn bir nechta to'liq gap va paragraflardan iborat bo'lsin. "
#             "Matnda -=* kabi belgilar bo'lmasin. "
#             "Matn mantiqiy ravishda tugallangan bo'lsin."
#         )
#     elif lan == "ru":
#         prompt = (
#             f"Тема: {topic}. Пункт: {band}. Напишите связанный и пояснительный текст на 750–850 символов по данному пункту. "
#             "Текст должен состоять из нескольких полных предложений и абзацев. "
#             "Не используйте символы вроде -=*. "
#             "Текст должен быть логически завершённым."
#         )
#     elif lan == "en":
#         prompt = (
#             f"Topic: {topic}. Section: {band}. Write a complete and explanatory text of 700–800 characters for this section. "
#             "The text should consist of several full sentences and paragraphs. "
#             "Do not use symbols like -=*. "
#             "The text should be logically complete."
#         )
#
#     for attempt in range(max_retries):
#         try:
#             data = {
#                 "model": "qwen-turbo",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.7,
#                 "max_tokens": 1100
#             }
#
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(API_URL, headers=headers, json=data) as resp:
#                     result = await resp.json()
#                     content = result['choices'][0]['message']['content'].strip()
#
#                     # Remove any special characters and extra newlines
#                     content = re.sub(r'[-=*]+', '', content)
#                     content = re.sub(r'\n+', '\n', content)
#
#                     # Check if content is complete
#                     if len(content) < 700:
#                         raise ValueError(f"Matn juda qisqa ({len(content)} belgi)")
#                     if len(content) > 800:
#                         content = content[:800]
#
#                     # Ensure the text ends with a proper sentence
#                     if not content.endswith(('.', '!', '?')):
#                         last_sentence_end = max(content.rfind('.'), content.rfind('!'), content.rfind('?'))
#                         if last_sentence_end > 0:
#                             content = content[:last_sentence_end + 1]
#
#                     return content
#
#         except Exception as e:
#             logging.warning(f"AI so'rovida xatolik (urunish {attempt + 1}/{max_retries}): {e}")
#             if attempt == max_retries - 1:
#                 raise
#             await asyncio.sleep(1)
#
#     raise Exception(f"{max_retries} marta urunishdan keyin ham matn olinmadi")
#
#
# async def generate_presentation(uid: int, message: Message,lan):
#
#         data = user_data[uid]
#         topic = data["topic"]
#         print('g2')
#         author = data["author"]
#
#         bg_num=data["bg_num"]
#         bg=data["bg"]
#         reja = data["reja"]
#
#         prs = Presentation()
#         prs.slide_width = Inches(13.33)
#         prs.slide_height = Inches(7.5)
#
#         # Title slide
#
#
#         # Table of contents slide
#
#
#         total = len(reja)
#         progress_bar = lambda done: ''.join(['🟩' if i < done else '⬜️' for i in range(10)])
#
#         progress_msg = await message.answer("⏳ Tayyorlanmoqda...")
#
#         for idx, band in enumerate(reja):
#             try:
#                 # Update progress
#                 progress = (idx + 1) * 10 // total
#                 await progress_msg.edit_text(f"⏳ Tayyorlanmoqda...\n\n{progress_bar(progress)} ({progress * 10}%)")
#
#                 # Get content with retries
#                 matn = await ask_ai_content(topic, band,lan=lan)
#
#                 # Format the content
#                 formatted_content = format_text(matn,lan)
#
#                 # Add slide
#                 slide_title = f"{idx + 1}. {band}"
#                 add_slide(bg_num,prs, bg, slide_title,lan, formatted_content)
#
#             except Exception as e:
#                 logging.error(f"Xatolik yuz berdi (band: {band}): {e}")
#
#                 # Try with a simpler prompt if the first attempt fails
#                 try:
#                     simple_matn = await ask_ai_content_simple(topic, band,lan)
#                     formatted_content = format_text(simple_matn,lan)
#                     slide_title = f"{idx + 1}. {band}"
#                     add_slide(bg_num,prs, bg, slide_title,lan, formatted_content)
#                     await message.answer(f"⚠️ '{band}' bandi uchun soddaroq matn qo'shildi")
#                 except Exception as e2:
#                     logging.error(f"Ikkinchi urunishda ham xatolik: {e2}")
#                     await message.answer(f"⚠️ '{band}' bandida xatolik yuz berdi. Bo'sh slayd qo'shildi.")
#                     slide_title = f"{idx + 1}. {band}"
#                     add_slide(bg_num,prs, bg, slide_title,lan, "Ushbu band uchun matn yaratilmadi")
#                 continue
#
#         buffer = BytesIO()
#         prs.save(buffer)
#         buffer.seek(0)
#         caption = f"📌 {data['title']}\n💡 @Slaydai_bot\n\n Boshqa amal bajarish uchun /start tugmasini bosing."
#         await message.answer_document(BufferedInputFile(buffer.read(), filename=f"{topic}.pptx"),caption=caption)
#
#
# async def ask_ai_content_simple(topic: str, band: str,lan:str) -> str:
#     """Simpler version of content generation for fallback"""
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#     if lan == "uz":
#         prompt = f"Mavzu: {topic}. Band: {band}. Ushbu band bo‘yicha 700-800 belgidan iborat qisqa, tushunarli matn yozing. Matnda hech qanday belgilar (** ## - *) ishlatilmasin. Faqat oddiy, silliq matn yozing."
#
#     elif lan == "ru":
#         prompt = f"Тема: {topic}. Пункт: {band}. Напишите краткий и понятный текст по данному пункту (700-800 символов). Не используйте специальные символы (** ## - *). Только обычный текст без заголовков."
#
#     elif lan == "en":
#         prompt = f"Topic: {topic}. Section: {band}. Write a short and clear text about this section (700-800 characters). Do not use any special characters like **, ##, -, or *. Just plain paragraph text, no headings."
#
#     data = {
#         "model": "qwen-turbo",
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.7,
#     }
#
#     async with aiohttp.ClientSession() as session:
#         async with session.post(API_URL, headers=headers, json=data) as resp:
#             result = await resp.json()
#             return result['choices'][0]['message']['content'].strip()
#
#
#
#
#
# def format_text(text: str,lan:str, line_length: int = 90) -> str:
#     """Format text to have approximately line_length characters per line"""
#     lines = []
#     for paragraph in text.split('\n'):
#         if paragraph.strip():
#             wrapped = textwrap.fill(paragraph, width=line_length)
#             lines.append(wrapped)
#     return '\n'.join(lines)
#
#
# def add_slide(bg_num,prs, bg_bytes, title,lan, content=""):
#     slide = prs.slides.add_slide(prs.slide_layouts[6])
#     slide.shapes.add_picture(BytesIO(bg_bytes), 0, 0, width=prs.slide_width, height=prs.slide_height)
#     if bg_num==6 or bg_num==7 or bg_num==8:
#         if title:
#             title_box = slide.shapes.add_textbox(Inches(1), Inches(1), prs.slide_width - Inches(2), Inches(1))
#             tf = title_box.text_frame
#             tf.clear()
#             p = tf.paragraphs[0]
#             p.text = title
#             p.font.size = Pt(25)
#             p.font.bold = True
#             p.font.name = 'Times new roman'
#             p.font.color.rgb = RGBColor(255, 255, 255)
#
#
#         if content:
#             clean = re.sub(r'[-=*]+', '', content)
#             formatted_content = format_text(clean,lan)
#             content_box = slide.shapes.add_textbox(
#                 Inches(2.4),  # 1 (start) + 1 (title height) + 0.4 (1 qator bo‘sh joy)
#                 prs.slide_width - Inches(2),
#                 prs.slide_height - Inches(3)
#             )
#
#             tf = content_box.text_frame
#             tf.clear()
#             for line in formatted_content.split("\n"):
#                 if line.strip():
#                     p = tf.add_paragraph()
#                     p.text = line.strip()
#                     p.font.size = Pt(16)
#                     p.font.name = 'Times new roman'
#                     p.font.color.rgb = RGBColor(255, 255, 255)
#
#     else:
#         if title:
#             title_box = slide.shapes.add_textbox(Inches(1), Inches(1), prs.slide_width - Inches(2), Inches(1))
#             tf = title_box.text_frame
#             tf.clear()
#             p = tf.paragraphs[0]
#             p.text = title
#             p.font.size = Pt(25)
#             p.font.bold = True
#             p.font.name = 'Times new roman'
#             p.font.color.rgb = RGBColor(0, 0, 0)
#
#         if content:
#             clean = re.sub(r'[-=*]+', '', content)
#             formatted_content = format_text(clean, lan)
#             content_box = slide.shapes.add_textbox(Inches(1), Inches(2), prs.slide_width - Inches(2),
#                                                    prs.slide_height - Inches(3))
#             tf = content_box.text_frame
#             tf.clear()
#             for line in formatted_content.split("\n"):
#                 if line.strip():
#                     p = tf.add_paragraph()
#                     p.text = line.strip()
#                     p.font.size = Pt(16)
#                     p.font.name = 'Times new roman'
#                     p.font.color.rgb = RGBColor(0, 0, 0)
# def add_title_slide(bg_num,prs, bg_bytes, title, author,lan):
#     slide = prs.slides.add_slide(prs.slide_layouts[6])
#     slide.shapes.add_picture(BytesIO(bg_bytes), 0, 0, width=prs.slide_width, height=prs.slide_height)
#     if bg_num==6 or bg_num==7 or bg_num==8:
#         # Title box (o'rtaga joylashtirilgan)
#         title_box = slide.shapes.add_textbox(Inches(2), Inches(2), prs.slide_width - Inches(4), Inches(2))
#         tf = title_box.text_frame
#         tf.clear()
#         p = tf.paragraphs[0]
#         p.text = title
#         p.alignment = PP_ALIGN.CENTER  # Markazga tekislash
#         p.font.size = Pt(44)
#         p.font.bold = True
#         p.font.name = 'Amasis MT Pro Black'
#         p.font.color.rgb = RGBColor(255, 255, 255)  # Qora rang
#
#         if lan=='uz':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Muallif: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(255, 255, 255)
#         if lan=='ru':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Автор: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(255, 255, 255)
#         if lan=='en':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Author: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(255, 255, 255)
#     else:
#         # Title box (o'rtaga joylashtirilgan)
#         title_box = slide.shapes.add_textbox(Inches(2), Inches(2), prs.slide_width - Inches(4), Inches(2))
#         tf = title_box.text_frame
#         tf.clear()
#         p = tf.paragraphs[0]
#         p.text = title
#         p.alignment = PP_ALIGN.CENTER  # Markazga tekislash
#         p.font.size = Pt(44)
#         p.font.bold = True
#         p.font.name = 'Amasis MT Pro Black'
#         p.font.color.rgb = RGBColor(0, 0, 0)  # Qora rang
#
#         if lan == 'uz':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Muallif: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(0, 0, 0)
#         if lan == 'ru':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Автор: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(0, 0, 0)
#         if lan == 'en':
#             # Author box (title ostida, markazda)
#             author_box = slide.shapes.add_textbox(Inches(2), Inches(4.5), prs.slide_width - Inches(4), Inches(1))
#             af = author_box.text_frame
#             af.clear()
#             ap = af.paragraphs[0]
#             ap.text = f"Author: {author}"
#             ap.alignment = PP_ALIGN.CENTER
#             ap.font.size = Pt(32)
#             ap.font.name = 'Amasis MT Pro Black'
#             ap.font.color.rgb = RGBColor(0, 0, 0)
#
# async def generate_presentation(uid: int, message: Message,lan):
#         data = user_data[uid]
#         topic = data["topic"]
#         author = data["author"]
#         print('g1')
#
#         bg_num=data['bg_num']
#         print(bg_num)
#
#         bg = data["bg"]
#
#         reja = data["reja"]
#
#         prs = Presentation()
#         prs.slide_width = Inches(13.33)
#         prs.slide_height = Inches(7.5)
#
#         # Yangi title slide funksiyasini chaqiramiz
#         add_title_slide(bg_num,prs, bg, topic, author,lan)
#
#
#         reja_text = "\n" + "\n".join([f" {r}" for i, r in enumerate(reja)])
#         add_slide(bg_num,prs, bg, "Reja",lan, reja_text)
#
#         total = len(reja)
#         progress_bar = lambda done: ''.join(['🟩' if i < done else '⬜️' for i in range(10)])
#
#         progress_msg = await message.answer("⏳ Tayyorlanmoqda...")
#
#         for idx, band in enumerate(reja):
#             try:
#                 # Progressni yangilash
#                 progress = (idx + 1) * 10 // total
#                 await progress_msg.edit_text(f"⏳ Tayyorlanmoqda...\n\n{progress_bar(progress)} ({progress * 10}%)")
#
#                 # Matnni olish va formatlash
#                 matn = await ask_ai_content(topic, band,lan=lan)
#
#
#                 # Slaydga qo'shish
#                 slide_title = f"{idx + 1}. {band}"
#                 add_slide(bg_num,prs, bg, slide_title, lan,matn)
#
#             except Exception as e:
#                 logging.error(f"Xatolik yuz berdi (band: {band}): {e}")
#                 # Xatolik haqida foydalanuvchiga xabar berish
#                 print(f"⚠️ '{band}' bandida xatolik yuz berdi. Boshqa matn bilan davom etilmoqda...")
#
#                 # Bo'sh slayd qo'shish
#                 slide_title = f"{idx + 1}. {band}"
#                 matn = await ask_ai_content(topic, band,lan=lan)
#                 add_slide(bg_num, prs, bg, slide_title, lan, matn)
#                 continue
#
#         buffer = BytesIO()
#         prs.save(buffer)
#         buffer.seek(0)
#         await message.answer_document(BufferedInputFile(buffer.read(), filename=f"{topic}.pptx"))
#
#
#
# @router.message(F.text=='/new')
# @router.callback_query(F.data=='taqdimot')
# async def start(callback:CallbackQuery, state: FSMContext):
#     check=db.select_user(tg_user=callback.from_user.id)
#     if int(check[3]) < 2500:
#         await callback.message.answer(
#             f"Xisobingizda yetarli mablag' yetarli emas 🙅!\nXisobingiz:💰 {check[3]}\n\nXisobni toldirish uchun /bye tugmasini bosing.")
#     else:
#         keyboard = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
#             [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
#             [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
#         ])
#         await callback.message.answer("Prezentatsiya tilini tanlang:", reply_markup=keyboard)
#         await state.set_state(PresState.language)
#
#
# @router.callback_query(StateFilter(PresState.language), F.data.startswith("lang_"))
# async def set_language(callback: CallbackQuery, state: FSMContext):
#         lang = callback.data.split("_")[1]
#         await state.update_data({'lang': lang})
#         await callback.message.delete()
#
#         await callback.message.answer("📌 Prezentatsiya mavzusini kiriting:")
#         await state.set_state(PresState.topic)
#
#
# @router.message(StateFilter(PresState.topic))
# async def get_topic(msg: Message, state: FSMContext):
#     user_data[msg.from_user.id] = {"topic": msg.text}
#     await msg.answer("✍️ Muallif ismini kiriting:")
#     await state.set_state(PresState.author)
#
#
# @router.message(StateFilter(PresState.author))
# async def get_author(msg: Message, state: FSMContext):
#     user_data[msg.from_user.id]["author"] = msg.text
#
#     # Create background selection buttons
#     inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
#         [
#             InlineKeyboardButton(text="1", callback_data="bg_1"),
#             InlineKeyboardButton(text="2", callback_data="bg_2"),
#             InlineKeyboardButton(text="3", callback_data="bg_3"),
#             InlineKeyboardButton(text="4", callback_data="bg_4"),
#             InlineKeyboardButton(text="5", callback_data="bg_5")
#         ],
#         [
#             InlineKeyboardButton(text="6", callback_data="bg_6"),
#             InlineKeyboardButton(text="7", callback_data="bg_7"),
#             InlineKeyboardButton(text="8", callback_data="bg_8"),
#             InlineKeyboardButton(text="9", callback_data="bg_9"),
#             InlineKeyboardButton(text="10", callback_data="bg_10")
#         ],
#
#     ])
#
#     # Send sample image with background options
#     rasim_manzili=Path(r".\handlers\users\tanlov.jpg")
#     photo = FSInputFile(rasim_manzili)  # Make sure this file exists
#     await bot.send_photo(
#         chat_id=msg.from_user.id,
#         photo=photo,
#         caption="📸 Prezentatsiya fonini tanlang (1-10 raqamlardan birini tanlang yoki o'zingiz rasm yuboring):",
#         reply_markup=inline_buttons
#     )
#     await state.set_state(PresState.bg)
#
#
# @router.callback_query(StateFilter(PresState.bg), F.data.startswith("bg_"))
# async def handle_bg_selection(callback: CallbackQuery, state: FSMContext):
#     bg_number = callback.data.split("_")[1]  # Extract number from callback_data
#     await state.update_data({"bg_num":bg_number})
#     user_data[callback.from_user.id]["bg_num"] = int(bg_number)
#     try:
#         # Load selected background image
#         rasim_manzili = Path(rf".\handlers\users\rasimlar\{bg_number}.jpg")
#         bg_path = rasim_manzili  # Your background images path
#         with open(bg_path, "rb") as f:
#             user_data[callback.from_user.id]["bg"] = f.read()
#
#         await callback.message.delete()  # Remove the photo message with buttons
#
#
#
#         await state.set_state(PresState.reja_mode)
#         await callback.message.answer("📄 Nechta slayd (faqat raqam):")
#         await state.set_state(PresState.slide_count)
#
#         # Holatda reja mode ni saqlaymiz
#         await state.update_data(reja_mode="ai")
#     except Exception as e:
#         logging.error(f"Background load error: {e}")
#         await callback.answer("❌ Fon yuklanmadi, qayta urining", show_alert=True)
#
#
#
#
#
# @router.message(StateFilter(PresState.bg_upload), F.photo)
# async def handle_uploaded_bg(msg: Message, state: FSMContext):
#     photo = msg.photo[-1]
#     file = await bot.get_file(photo.file_id)
#     bg = await bot.download_file(file.file_path)
#     user_data[msg.from_user.id]["bg"] = bg.read()
#
#
#
#     await state.set_state(PresState.reja_mode)
#
#     await msg.message.answer("📄 Nechta slayd (faqat raqam):")
#     await state.set_state(PresState.slide_count)
#
#     # Holatda reja mode ni saqlaymiz
#     await state.update_data(reja_mode="ai")
#
#
# @router.message(StateFilter(PresState.slide_count))
# async def get_slide_count(msg: Message, state: FSMContext):
#     if not msg.text.isdigit():
#         await msg.answer("❌ Iltimos, faqat raqam kiriting!")
#         return
#
#     requested_slide_count = int(msg.text)
#     if requested_slide_count < 1:
#         await msg.answer("❌ Slaydlar soni 1 dan kam bo'lishi mumkin emas!")
#         return
#
#     data = await state.get_data()
#     uid = msg.from_user.id
#     lan = data.get('lang')
#
#     if data.get("reja_mode") == "ai":
#         # Determine how many outline points to generate
#         outline_points_to_generate = min(requested_slide_count, 10)
#
#         topic = user_data[uid]["topic"]
#
#         if lan == "uz":
#             prompt = (
#                 f"'{topic}' mavzusi uchun {outline_points_to_generate} ta reja bandini generatsiya qiling. "
#                 "Har bir band yangi qatorda bo'lsin va 5-7 so'zdan iborat bo'lsin. "
#                 "Har bir band alohida va tushunarli bo'lsin."
#             )
#         elif lan == "ru":
#             prompt = (
#                 f"Сгенерируйте {outline_points_to_generate} пунктов плана для темы '{topic}'. "
#                 "Каждый пункт должен быть с новой строки и содержать 5-7 слов. "
#                 "Каждый пункт должен быть самостоятельным и понятным."
#             )
#         elif lan == "en":
#             prompt = (
#                 f"Generate {outline_points_to_generate} outline points for the topic '{topic}'. "
#                 "Each point should be on a new line and contain 5-7 words. "
#                 "Each point should be self-contained and clear."
#             )
#
#         headers = {
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         }
#         data = {
#             "model": "qwen-turbo",
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": 0.7,
#         }
#
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(API_URL, headers=headers, json=data) as resp:
#                     result = await resp.json()
#                     reja = result['choices'][0]['message']['content'].split('\n')
#                     user_data[uid]["reja"] = [r.strip() for r in reja if r.strip()][:outline_points_to_generate]
#
#                     # If user requested more slides than outline points, distribute content
#                     if requested_slide_count > len(user_data[uid]["reja"]):
#                         additional_slides = requested_slide_count - len(user_data[uid]["reja"])
#                         # Calculate how to distribute additional slides
#                         slides_per_point = additional_slides // len(user_data[uid]["reja"]) + 1
#                         extra_slides = additional_slides % len(user_data[uid]["reja"])
#
#                         # Create an expanded reja list
#                         expanded_reja = []
#                         for i, point in enumerate(user_data[uid]["reja"]):
#                             expanded_reja.append(point)
#                             # Add extra slides for some points
#                             if i < extra_slides:
#                                 for _ in range(slides_per_point):
#                                     expanded_reja.append(f"{point} (davomi {i + 1})")
#                             elif slides_per_point > 1:
#                                 for _ in range(slides_per_point - 1):
#                                     expanded_reja.append(f"{point} (davomi {i + 1})")
#
#                         user_data[uid]["reja"] = expanded_reja[:requested_slide_count]
#
#             await msg.answer("⏳ Prezentatsiya tayyorlanmoqda, iltimos kuting...")
#             await generate_presentation(uid, msg, lan)
#             await state.clear()
#
#         except Exception as e:
#             logging.error(f"Reja generatsiyasida xatolik: {e}")
#             await msg.answer("❌ Reja generatsiyasida xatolik yuz berdi. Qo'lda kiritishga harakat qiling.")
#             user_data[uid]["reja"] = []
#             await msg.answer("📝 Har bir reja bandini yangi qatorda kiriting. Tugatish uchun 'tayyor' deb yozing.")
#             await state.set_state(PresState.reja)
#
#     else:
#         # For manual input
#         current_reja_count = len(user_data[uid]["reja"])
#
#         # If user entered more than 10 points but requests fewer slides
#         if current_reja_count > requested_slide_count:
#             user_data[uid]["reja"] = user_data[uid]["reja"][:requested_slide_count]
#         # If user entered fewer points than requested slides
#         elif requested_slide_count > current_reja_count:
#             additional_slides = requested_slide_count - current_reja_count
#             slides_per_point = additional_slides // current_reja_count + 1
#             extra_slides = additional_slides % current_reja_count
#
#             expanded_reja = []
#             for i, point in enumerate(user_data[uid]["reja"]):
#                 expanded_reja.append(point)
#                 # Add continuation slides
#                 if i < extra_slides:
#                     for _ in range(slides_per_point):
#                         expanded_reja.append(f"{point} (davomi {i + 1})")
#                 elif slides_per_point > 1:
#                     for _ in range(slides_per_point - 1):
#                         expanded_reja.append(f"{point} (davomi {i + 1})")
#
#             user_data[uid]["reja"] = expanded_reja[:requested_slide_count]
#
#         await msg.answer("⏳ Prezentatsiya tayyorlanmoqda, iltimos kuting...")
#         await generate_presentation(uid, msg, lan)
#         await state.clear()
#
#
# @router.message(StateFilter(PresState.reja))
# async def reja_input(msg: Message, state: FSMContext):
#     if msg.text.lower() == "tayyor":
#         if len(user_data[msg.from_user.id]["reja"]) == 0:
#             await msg.answer("❌ Kamida bitta reja bandini kiriting!")
#             return
#         await msg.answer("📄 Nechta slayd (faqat raqam):")
#         await state.set_state(PresState.slide_count)
#     else:
#         user_data[msg.from_user.id]["reja"].append(msg.text)
#
#
# @router.message(StateFilter(PresState.slide_count))
# async def get_slide_count(msg: Message, state: FSMContext):
#     if not msg.text.isdigit():
#         await msg.answer("❌ Iltimos, faqat raqam kiriting!")
#         return
#     ol=await state.get_data()
#     bg_num=ol.get("bg_num")
#     slide_count = int(msg.text)
#     if slide_count < 1:
#         await msg.answer("❌ Slaydlar soni 1 dan kam bo'lishi mumkin emas!")
#         return
#
#     # Adjust reja if needed
#     if len(user_data[msg.from_user.id]["reja"]) > slide_count:
#         user_data[msg.from_user.id]["reja"] = user_data[msg.from_user.id]["reja"][:slide_count]
#         await msg.answer(f"⚠️ Reja {slide_count} ta bandga qisqartirildi")
#
#
#     await generate_presentation(msg.from_user.id, msg)
#     await state.clear()
