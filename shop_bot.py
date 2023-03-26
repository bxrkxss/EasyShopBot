import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "yourtelegrambot token"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

products = {
    "item1": {"name": "Текст1", "price": 100, "quantity": 10},
    "item2": {"name": "Текст2", "price": 200, "quantity": 5},
    "item3": {"name": "Текст3", "price": 150, "quantity": 15},
}

def create_assortment_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for item, data in products.items():
        button_text = f"{data['name']} - Цена: {data['price']} - Количество: {data['quantity']}"
        keyboard.add(InlineKeyboardButton(button_text, callback_data=item))
        keyboard.add(InlineKeyboardButton("Купить", url="https://t.me/yourname"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    await message.reply("Добро пожаловать! Выберите товар:", reply_markup=create_assortment_keyboard())

@dp.callback_query_handler(lambda c: c.data in ["item1", "item2", "item3"])
async def process_callback(callback_query: types.CallbackQuery):
    item = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if item in products:
        product_info = products[item]
        response_text = f"Вы выбрали товар:\n\n{product_info['name']}\nЦена: {product_info['price']} рублей\nКоличество: {product_info['quantity']} шт."
        await bot.send_message(callback_query.from_user.id, response_text)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
