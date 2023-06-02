import logging
import aiogram
import os

import functions

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start(message: aiogram.types.Message):
    if not functions.is_account_exist(message.from_user.id):
        functions.create_new_account(message.from_user.first_name, message.from_user.username, message.from_user.id)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_players_events(message.from_user.id))
    await message.answer(f"Hello {message.from_user.first_name}. "
                         f"Welcome to Renaissance, here you can do whatever you want, "
                         f"and your path is determined only by you. What are you waiting for, let's go!",
                         reply_markup=keyboard)


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
