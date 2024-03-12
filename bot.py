import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import weather

load_dotenv()
# Запуск бота
async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    # Диспетчер
    dp = Dispatcher()
    #Регистрируем роутер
    dp.include_router(weather.router)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
