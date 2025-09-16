# from pathlib import Path
#
# from loader import dp, bot, db
# import logging
#
# logging.basicConfig(level=logging.INFO)  # Yoki DEBUG
# logger = logging.getLogger(__name__)
#
# import os
# import re
# import requests
# import logging
# import asyncio
# from datetime import datetime
# from aiogram import Bot, Dispatcher, F, Router
# from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# from aiogram.filters import CommandStart, StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.default import DefaultBotProperties
# from docx import Document
# from docx.shared import Pt, Inches
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.oxml import OxmlElement
# from docx.oxml.ns import qn
#
# # --- Configuration ---
#
# AI_API_KEY = "sk-cb355fe140f84aad88999f6a3db45634"
# AI_API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
#
#
# from aiogram import Router
# from aiogram.types import Message
# from aiogram.filters import Command
#
# router = Router()  # Har doim shart!
#
#
# # --- FSM States ---
# class ReferatState(StatesGroup):
#     doc_type = State()
#     title = State()
#     institute = State()
#     author = State()
#     pages = State()
#     language = State()
#     reja_mode = State()
#     reja_manual = State()
#
#
# # --- Keyboard functions ---
# def start_keyboard():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="📘 Referat / Mustaqil ish", callback_data="start_referat")]
#     ])
#
#
# def doc_type_keyboard():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="REFERAT", callback_data="set_type_referat")],
#         [InlineKeyboardButton(text="MUSTAQIL ISH", callback_data="set_type_mustaqil")]
#     ])
#
#
# def reja_choice_keyboard():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="📝 O'zim yozaman", callback_data="reja_manual")],
#         [InlineKeyboardButton(text="🤖 AI tuzsin", callback_data="reja_ai")]
#     ])
#
#
# def language_keyboard():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Uzbek", callback_data="lang_uzbek"),
#             InlineKeyboardButton(text="Russian", callback_data="lang_rus"),
#             InlineKeyboardButton(text="English", callback_data="lang_english")
#         ]
#     ])
#
#
# # --- AI communication function ---
# async def ai_post(payload):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, lambda: requests.post(AI_API_URL, headers={
#         "Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"
#     }, json=payload))
#
#
# # --- Outline generation function ---
# async def generate_reja(title: str, lang: str = 'uzbek') -> list:
#     lang_prompts = {
#         "uzbek": f"'{title}' mavzusida faqat asosiy bandlardan iborat reja yozing. Har bir bandni yangi qatorda va raqamlangan ro'yxat shaklida yozing. Matn O'zbek tilida bo'lsin.",
#         "rus": f"Напишите план по теме '{title}'. Только основные пункты, каждый с новой строки в виде нумерованного списка. Текст должен быть на русском языке.",
#         "english": f"Write an outline for the topic '{title}'. Only main points, each on a new line as a numbered list. Text should be in English."
#     }
#     prompt = lang_prompts.get(lang, lang_prompts["uzbek"])
#
#     payload = {
#         "model": "qwen-turbo",
#         "messages": [
#             {"role": "system",
#              "content": "Siz reja tuzuvchi mutaxassis. Reja bandlarini faqat raqamlangan ro'yxat sifatida, hech qanday qo'shimcha formatlash yoki maxsus simvollarsiz taqdim eting."},
#             {"role": "user", "content": prompt},
#         ],
#         "temperature": 0.2,
#         "max_tokens": 500,
#     }
#     try:
#         response = await ai_post(payload)
#         response.raise_for_status()
#         content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
#
#         cleaned_reja = []
#         for line in content.split("\n"):
#             cleaned_line = re.sub(r'^[*-]?\s*\d+\.\s*', '', line).strip()
#             cleaned_line = re.sub(r'[*#]', '', cleaned_line).strip()
#             if cleaned_line:
#                 cleaned_reja.append(f"{len(cleaned_reja) + 1}. {cleaned_line}")
#
#         if not cleaned_reja:
#             default_reja = {
#                 "uzbek": ["1. Kirish", "2. Asosiy qism", "3. Xulosa"],
#                 "rus": ["1. Введение", "2. Основная часть", "3. Заключение"],
#                 "english": ["1. Introduction", "2. Main part", "3. Conclusion"]
#             }
#             return default_reja.get(lang, default_reja["uzbek"])
#         return cleaned_reja
#     except Exception as e:
#         logger.error(f"Reja yaratishda xato: {e}")
#         default_reja = {
#             "uzbek": ["1. Kirish", "2. Asosiy qism", "3. Xulosa"],
#             "rus": ["1. Введение", "2. Основная часть", "3. Заключение"],
#             "english": ["1. Introduction", "2. Main part", "3. Conclusion"]
#         }
#         return default_reja.get(lang, default_reja["uzbek"])
#
#
# # --- Text generation with page control ---
# async def generate_coursework(title: str, reja: list, pages: int, lang: str = 'uzbek') -> str:
#     # Calculate words per section (350 words/page is standard)
#     words_per_page = 515
#     total_words = words_per_page * pages
#     num_sections = len(reja)
#     words_per_section = max(255, total_words // num_sections)  # At least 100 words per section
#     print(title)
#
#     lang_prompts = {
#         "uzbek": lambda item: (
#             f"{item} haqida matn yozing. Matn faqat O'zbek tilida bo'lsin, {words_per_section} so'zdan oshmasin. Matnda hech qanday belgilar (** ## - *) ishlatilmasin. Faqat oddiy, silliq matn yozing."
#         ),
#         "rus": lambda item: (
#             f"Напишите связанный текст на тему '{item}' на русском языке. Не более {words_per_section} слов. Не используйте специальные символы (** ## - *). Только обычный текст без заголовков."
#         ),
#         "english": lambda item: (
#             f"Write a coherent text about '{item}' in English. No more than {words_per_section} words. Do not use any special characters like **, ##, -, or *. Just plain paragraph text, no headings."
#         )
#     }
#
#     prompt_generator = lang_prompts.get(lang, lang_prompts["uzbek"])
#     cleaned_reja = [re.sub(r'^\d+\.\s*', '', item).strip() for item in reja]
#
#     text = ""
#     for item in cleaned_reja:
#         text += f"\n\n<b>{item.upper()}</b>\n\n"
#         prompt = prompt_generator(item)
#
#         try:
#             payload = {
#                 "model": "qwen-turbo",
#                 "messages": [
#                     {"role": "system",
#                      "content": f"Matnni {words_per_section} so'zdan oshirmang. To'liq va tushunarli yozing."},
#                     {"role": "user", "content": prompt},
#                 ],
#                 "temperature": 0.7,
#                 "max_tokens": words_per_section * 2  # Approximate tokens
#             }
#             response = await ai_post(payload)
#             content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
#             text += content
#         except Exception as e:
#             logger.error(f"Matn generatsiya qilishda xato: {e}")
#             text += f"[{item} bo'limi uchun matn generatsiya qilinmadi]"
#
#     return text
#
#
# # --- Estimate page count ---
# def estimate_page_count(text: str) -> int:
#     word_count = len(re.findall(r'\w+', text))
#     return max(1, round(word_count / 350))  # 350 words per page
#
#
# # --- Document formatting functions ---
# def add_double_border(section):
#     sectPr = section._sectPr
#     pgBorders = OxmlElement('w:pgBorders')
#     for side in ['top', 'left', 'bottom', 'right']:
#         border = OxmlElement(f'w:{side}')
#         border.set(qn('w:val'), 'double')
#         border.set(qn('w:sz'), '12')
#         border.set(qn('w:space'), '24')
#         border.set(qn('w:color'), '000000')
#         pgBorders.append(border)
#     sectPr.append(pgBorders)
#
#
# def remove_borders(section):
#     for b in section._sectPr.xpath('./w:pgBorders'):
#         section._sectPr.remove(b)
#
#
# def clean_text(text: str) -> str:
#     cleaned = re.sub(r'[*_~#+\-\=\[\]\{\}\(\)\|]', '', text)
#     cleaned = re.sub(r'\s+', ' ', cleaned).strip()
#     return cleaned
#
#
# # --- Save to Word with accurate page control ---
# def save_to_word(title, institute, author, pages, language, text, reja, doc_type):
#     doc = Document()
#     section1 = doc.sections[0]
#     section1.top_margin = Inches(1)
#     section1.bottom_margin = Inches(1)
#     section1.left_margin = Inches(1)
#     section1.right_margin = Inches(1)
#     add_double_border(section1)
#
#     translations = {
#         "uzbek": {
#             "ministry": "O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM FAN VA INNOVATSIYA VAZIRLIGI",
#             "topic": "Mavzu",
#             "student": "O'quvchi",
#             "academic_year": "o'quv yili",
#             "plan": "Reja",
#             "referat": "REFERAT",
#             "mustaqil": "MUSTAQIL ISH"
#         },
#         "rus": {
#             "ministry": "МИНИСТЕРСТВО ВЫСШЕГО ОБРАЗОВАНИЯ, НАУКИ И ИННОВАЦИЙ РЕСПУБЛИКИ УЗБЕКИСТАН",
#             "topic": "Тема",
#             "student": "Студент",
#             "academic_year": "учебный год",
#             "plan": "План",
#             "referat": "РЕФЕРАТ",
#             "mustaqil": "САМОСТОЯТЕЛЬНАЯ РАБОТА"
#         },
#         "english": {
#             "ministry": "MINISTRY OF HIGHER EDUCATION, SCIENCE AND INNOVATION OF THE REPUBLIC OF UZBEKISTAN",
#             "topic": "Topic",
#             "student": "Student",
#             "academic_year": "academic year",
#             "plan": "Plan",
#             "referat": "REFERAT",
#             "mustaqil": "INDEPENDENT WORK"
#         }
#     }
#
#     lang_texts = translations.get(language, translations["uzbek"])
#     translated_doc_type = lang_texts["referat"] if doc_type == "REFERAT" else lang_texts["mustaqil"]
#
#     def set_style(p, size, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=0):
#         p.alignment = align
#         run = p.runs[0]
#         run.font.size = Pt(size)
#         run.font.name='Times new roman'
#         run.bold = bold
#         p.paragraph_format.space_after = Pt(after)
#
#     # Add document header
#     p1 = doc.add_paragraph(lang_texts["ministry"])
#     set_style(p1, 16, True, WD_ALIGN_PARAGRAPH.CENTER, 12)
#     p2 = doc.add_paragraph(institute)
#     set_style(p2, 16, True, WD_ALIGN_PARAGRAPH.CENTER, 60)
#     p3 = doc.add_paragraph(translated_doc_type)
#     set_style(p3, 54, True, WD_ALIGN_PARAGRAPH.CENTER, 24)
#     p4 = doc.add_paragraph(f"{lang_texts['topic']}: {title}")
#     set_style(p4, 16, True, WD_ALIGN_PARAGRAPH.CENTER, 60)
#     p5 = doc.add_paragraph(f"{lang_texts['student']}: {author}")
#     set_style(p5, 14, True, WD_ALIGN_PARAGRAPH.CENTER, 230)
#     p6 = doc.add_paragraph(f"{datetime.now().year}-{lang_texts['academic_year']}")
#     set_style(p6, 9, True, WD_ALIGN_PARAGRAPH.CENTER)
#
#     # Add content sections
#     section2 = doc.add_section()
#     remove_borders(section2)
#
#     # Add outline
#     p7 = doc.add_paragraph(f"{lang_texts['plan']}:")
#     set_style(p7, 14, True, WD_ALIGN_PARAGRAPH.LEFT)
#     for item in reja:
#         pi = doc.add_paragraph(item)
#         set_style(pi, 14, False, WD_ALIGN_PARAGRAPH.LEFT)
#
#     doc.add_page_break()
#
#     # Add main text with proper formatting
#     for para in text.split("\n\n"):
#         # **...** formatdagi matnlarni o'tkazib yuboramiz
#         if para.startswith("**") and para.endswith("**"):
#             continue  # Bu matnni butunlay o'tkazib yuboramiz
#
#         # <b>...</b> teglaridagi matnlarni sarlavha sifatida qo'shamiz
#         elif para.startswith("<b>") and para.endswith("</b>"):
#             heading_text = para[3:-4].strip()
#
#             p = doc.add_paragraph(heading_text)
#             p.runs[0].font.size = Pt(24)
#             p.runs[0].font.name = "Amasis MT Pro Black"
#             p.runs[0].bold = True
#             p.alignment = WD_ALIGN_PARAGRAPH.LEFT
#
#         # Qolgan matnlarni oddiy formatda qo'shamiz
#         else:
#             text = para.strip()
#             if text:  # Matn bo'sh bo'lmaganligini tekshiramiz
#                 # Agar hujjatda shu matn yo'q bo'lsa qo'shamiz
#                 if not any(text == p.text for p in doc.paragraphs):
#                     p = doc.add_paragraph(text)
#                     p.runs[0].font.size = Pt(16)
#                     p.runs[0].font.name = "Times new roman"
#                     p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
#
#     filename = f"referat_{title.replace(' ', '_')[:50]}.docx"
#     doc.save(filename)
#     return filename
#
#
#
#
# @router.callback_query(F.data == "start_referat")
# async def start_referat(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(ReferatState.doc_type)
#     photo_manzili = Path(r".\handlers\users\img_1.png")
#     rasim=FSInputFile(photo_manzili)
#     await bot.send_photo(chat_id=callback.from_user.id,caption="Tanlang:", photo=rasim,reply_markup=doc_type_keyboard())
#
#
# @router.callback_query(F.data.startswith("set_type_"))
# async def set_doc_type(callback: CallbackQuery, state: FSMContext):
#     doc_type = "REFERAT" if callback.data == "set_type_referat" else "MUSTAQIL ISH"
#     await state.update_data(doc_type=doc_type)
#     await callback.message.answer("Mavzuni kiriting:")
#     await state.set_state(ReferatState.title)
#
#
# @router.message(StateFilter(ReferatState.title))
# async def get_title(message: Message, state: FSMContext):
#     await state.update_data(title=clean_text(message.text))
#     await message.answer("Institut va kafedrani kiriting:")
#     await state.set_state(ReferatState.institute)
#
#
# @router.message(StateFilter(ReferatState.institute))
# async def get_institute(message: Message, state: FSMContext):
#     await state.update_data(institute=clean_text(message.text))
#     await message.answer("Muallif (Ism Familiya) ni kiriting:")
#     await state.set_state(ReferatState.author)
#
#
# @router.message(StateFilter(ReferatState.author))
# async def get_author(message: Message, state: FSMContext):
#     await state.update_data(author=clean_text(message.text))
#     await message.answer("Asosiy matn uchun sahifalar sonini kiriting (5-10 bet):")
#     await state.set_state(ReferatState.pages)
#
#
# @router.message(StateFilter(ReferatState.pages))
# async def get_pages(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer("Iltimos, raqam kiriting (5-10):")
#         return
#     pages = int(message.text)
#     if not 5 <= pages <= 10:
#         await message.answer("Iltimos, 5 dan 10 gacha bo'lgan raqam kiriting:")
#         return
#     await state.update_data(pages=pages)
#     await message.answer("Qaysi tilda yozilsin?", reply_markup=language_keyboard())
#     await state.set_state(ReferatState.language)
#
#
# @router.callback_query(F.data.startswith("lang_"))
# async def get_language(callback: CallbackQuery, state: FSMContext):
#     lang_code = callback.data.split("_")[1]
#     lang = {"uzbek": "uzbek", "rus": "rus", "english": "english"}.get(lang_code, "uzbek")
#     await state.update_data(language=lang)
#     await callback.message.answer("Rejani kim tuzsin?", reply_markup=reja_choice_keyboard())
#     await state.set_state(ReferatState.reja_mode)
#
#
# @router.callback_query(F.data == "reja_ai")
# async def reja_ai(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#
#     reja = await generate_reja(data['title'], data['language'])
#     await state.update_data(reja_items=reja, reja_type="ai")
#     await generate_and_send_referat(callback.message, state)
#
#
# @router.callback_query(F.data == "reja_manual")
# async def reja_manual(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(reja_type="manual")
#     await callback.message.answer("Reja bandlarini kiriting (har birini yangi qatorda yozing):")
#     await state.set_state(ReferatState.reja_manual)
#
#
# @router.message(StateFilter(ReferatState.reja_manual))
# async def get_manual_reja(message: Message, state: FSMContext):
#     reja = [f"{i + 1}. {clean_text(line)}" for i, line in enumerate(message.text.split("\n")) if clean_text(line)]
#     if len(reja) < 3:
#         await message.answer("Iltimos, kamida 3 ta reja bandini kiriting:")
#         return
#     await state.update_data(reja_items=reja)
#     await generate_and_send_referat(message, state)
#
#
# async def generate_and_send_referat(message: Message, state: FSMContext):
#     data = await state.get_data()
#     requested_pages = data['pages']
#     lang = data['language']
#     doc_type = data['doc_type']
#     reja = data['reja_items']
#
#     progress_msg = await message.answer("Referat tayyorlanmoqda...")
#
#     try:
#         # Generate text with controlled length
#         text = await generate_coursework(data['title'], reja, requested_pages, lang)
#
#         # Check actual page count
#         actual_pages = estimate_page_count(text)
#         if actual_pages > requested_pages * 1.2:  # If 20% more than requested
#             await progress_msg.delete()
#             await message.answer(
#                 f"⚠️ Siz so'ragan {requested_pages} sahifa o'rniga {actual_pages} sahifa generatsiya qilindi. "
#                 "Qisqartirilgan versiyani yuborish uchun /qisqa buyrug'ini yuboring."
#             )
#             await state.update_data(long_text=text)
#             return
#
#         # Save and send document
#         file_path = save_to_word(
#             data['title'], data['institute'], data['author'],
#             requested_pages, lang, text, reja, doc_type
#         )
#
#         await progress_msg.delete()
#         caption = f"📌 {data['title']}\n💡 @Slaydai_bot\n\n Boshqa amal bajarish uchun /start tugmasini bosing."
#         await message.answer_document(FSInputFile(file_path), caption=caption)
#         os.remove(file_path)
#
#     except Exception as e:
#         logger.error(f"Xatolik: {e}")
#         await message.answer(f"Xatolik yuz berdi: {str(e)}")
#     finally:
#         await state.clear()
#
#
# @router.message(F.text == "/qisqa")
# async def send_short_version(message: Message, state: FSMContext):
#     data = await state.get_data()
#     long_text = data.get('long_text', '')
#
#     if not long_text:
#         await message.answer("Qisqartiriladigan matn topilmadi.")
#         return
#
#     progress_msg = await message.answer("Qisqartirilgan versiya tayyorlanmoqda...")
#
#     try:
#         # Generate shorter version
#         requested_pages = data['pages']
#         text = await generate_coursework(data['title'], data['reja_items'], requested_pages, data['language'])
#
#         # Save and send
#         file_path = save_to_word(
#             data['title'], data['institute'], data['author'],
#             requested_pages, data['language'], text, data['reja_items'], data['doc_type']
#         )
#
#         actual_pages = estimate_page_count(text)
#         await progress_msg.delete()
#         caption = f"📌 {data['title']} (qisqartirilgan)\n sahifa\n💡 @Slaydai_bot\n\n Boshqa amal bajarish uchun /start tugmasini bosing."
#         await message.answer_document(FSInputFile(file_path), caption=caption)
#         os.remove(file_path)
#
#     except Exception as e:
#         logger.error(f"Xatolik: {e}")
#         await message.answer(f"Qisqartirishda xatolik: {str(e)}")
#     finally:
#         await state.clear()
#
#
