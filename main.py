import logging
import aiogram
import os

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start(message: aiogram.types.Message):
    await message.answer("Welcome to Renaissance, here you can do whatever you want, "
                         "and your path is determined only by you. What are you waiting for, let's go!")


@dp.message_handler()
async def main(message: aiogram.types.Message):
    pass


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
