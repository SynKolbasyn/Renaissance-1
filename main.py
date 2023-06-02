import logging
import aiogram
import os

import functions

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher(bot)


async def setup_bot_commands(dispatcher):
    bot_commands = [
        aiogram.types.BotCommand(command="/start", description="Show start menu"),
        aiogram.types.BotCommand(command="/help", description="Show start menu"),
        aiogram.types.BotCommand(command="/info", description="Show player info")
    ]
    await bot.set_my_commands(bot_commands)


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


@dp.message_handler(commands="info")
async def info(message: aiogram.types.Message):
    await message.answer(functions.get_player_info(message.from_user.id))


@dp.message_handler()
async def events(message: aiogram.types.Message):
    answer = functions.do_event(message.from_user.id, message.text)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_players_events(message.from_user.id))
    await message.answer(answer, reply_markup=keyboard)


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)
