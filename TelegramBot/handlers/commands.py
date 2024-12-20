from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message

import keyboards.inline_kb as in_kb
import handlers.function as hf
import url_storage as storage
import datetime

router = Router()


@router.message(F.text.contains("tiktok.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def video_request(message:Message):
    url = message.text.strip()
    url_id = hf.generate_url_id(url)
    storage.url_storage[url_id] = url
    storage.save_url_storage(storage.url_storage)
    storage.url_storage = storage.load_url_storage()
    await message.answer("ᅠᅠ", reply_markup= await in_kb.format_btn(url_id))



@router.message()
async def debug_handler(message: Message):
    print(f"[{datetime.datetime.now()}] Received message: {message.text}")


