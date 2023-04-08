from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon.LEXICON import LEXICON
from keyboards.keyboards import start_kb, cancel_kb

from states.states import (FSMlowprice,
                           FSMbestdeal,
                           FSMhighprice,
                           FSMchoice)

from database.database import history_dict


router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
   await message.answer(LEXICON['/start'], reply_markup=start_kb)


@router.message(Command(commands='history'))
async def process_history_command(message: Message):

    print(history_dict[message.from_user.id])

    await message.answer(text='Результат выведен в консоль')

@router.message(Command(commands='help'))
async def process_help_command(message: Message):

    await message.answer(text=LEXICON['help_command'])


@router.callback_query(FSMchoice.get_choice, Text(text=['yes', 'no']))
async def process_restart_answer(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await callback.message.answer(text=LEXICON['/start'], reply_markup=start_kb)


    else:
        await callback.message.answer(text=LEXICON['not_again'])
    await callback.message.delete()
    await state.clear()
