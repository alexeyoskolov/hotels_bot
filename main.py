import asyncio
import logging

from aiogram import Bot, Dispatcher


from handlers import highprice_hnd, lowprice_hnd, bestdeal_hdl, user_handlers
from config import BOT_TOKEN
from keyboards.main_menu import set_main_menu


logger = logging.getLogger(__name__)

# Фунуция конфигурирования и запуска бота

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )
    # Выводим в консоль информацию о запуске бота
    logger.info('Starting bot')

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot=bot)

    await set_main_menu(bot)


    # # Регистрируем роутеры в диспетчере

    dp.include_router(user_handlers.router)
    dp.include_router(lowprice_hnd.router)
    dp.include_router(highprice_hnd.router)
    dp.include_router(bestdeal_hdl.router)

    # Пропускаем накопившиеся апдейты и запускам пуллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
