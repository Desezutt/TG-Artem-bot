from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup

async def format_btn(url_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='download' ,callback_data=f"video|{url_id}")]
    ])
    return keyboard