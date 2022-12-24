import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
import aiofiles
from keyboards import markup, speech_btn
from googletrans import Translator
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Translate
from gtts import gTTS
import os


logging.basicConfig(level=logging.INFO)
translator = Translator()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"], state="*")
async def do_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_name = message.from_user.username
    await message.answer(f"Assalomu aleykum {user_full_name}! Bot orqali hohlagan matnni tajrima qilishingiz mumkin. Quyidagi tugmalardan birini tanlang", reply_markup=markup)
    await Translate.lang.set()


@dp.message_handler(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng - 🇺🇿 Uzb", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("Ingliz tilidagi matnni O'zbek tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "en",
        "to": "uz"
    })
    await Translate.next()
    # await Translate.text.set()


@dp.message_handler(text="🇷🇺 Rus - 🇺🇿 Uzb", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("Rus tilidagi matnni O'zbek tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "ru",
        "to": "uz"
    })
    await Translate.next()

@dp.message_handler(text="🇺🇿 Uzb - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("O'zbek tilidagi matnni Ingliz tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "uz",
        "to": "en"
    })
    await Translate.next()

@dp.message_handler(text="🇺🇿 Uzb - 🇷🇺 Rus", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("O'zbek tilidagi matnni Rus tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "uz",
        "to": "ru"
    })
    await Translate.next()

@dp.message_handler(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng - 🇷🇺 Rus", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("Ingliz tilidagi matnni Rus tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "en",
        "to": "ru"
    })
    await Translate.next()

@dp.message_handler(text="🇷🇺 Rus - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng", state=Translate.lang)
async def en_uz(message: types.Message, state: FSMContext):
    await message.answer("Rus tilidagi matnni Ingliz tiliga tarjima qilish")
    await message.answer("Tarjima qilmoqchi bo'lgan matnni jo'nating")
    await state.update_data({
        "from": "ru",
        "to": "en"
    })
    await Translate.next()

@dp.message_handler(state=Translate.text)
async def translate_text(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    lang1 = data.get('from')
    lang2 = data.get('to')
    translated_text = translator.translate(text=text, src=lang1, dest=lang2)
    if lang2 != "uz":
        tarjima = translated_text.text
        await state.update_data({
            "text": tarjima
        })
        await message.answer(tarjima, reply_markup=speech_btn)
        await Translate.next()
    else:
        await message.answer(translated_text.text, reply_markup=markup)
        await Translate.lang.set()


@dp.callback_query_handler(text="audio", state=Translate.speech)
async def text_to_audio(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Audio tayyorlanmoqda ...")
    user_id = call.from_user.id
    data = await state.get_data()
    lang = data.get('to')
    text = data.get('text')
    tts = gTTS(text=text, lang=lang)
    tts.save(f"{user_id}.mp3")
    await call.message.edit_reply_markup(reply_markup=None)
    async with aiofiles.open(f"{user_id}.mp3", "rb") as file:
        await call.message.answer_audio(audio=file, reply_markup=markup)
    if os.path.exists(f"{user_id}.mp3"):
        os.remove(f"{user_id}.mp3")    
    await Translate.lang.set()


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
