from aiogram import Bot
from aiogram.types import BotCommand

from lexicon import LEXICON

async def set_main_menu(bot: Bot):

    main_menu_commands =[
        BotCommand(command='/start', description='Начало работы с ботом'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/history', description='Показать мою  историю запросов')]


    await bot.set_my_commands(main_menu_commands)