import datetime

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from lexicon.LEXICON import LEXICON
from keyboards.keyboards import (start_kb,
                                 cancel_kb,
                                 yes_no_kb,
                                 photo_count_kb,
                                 adults_kb,
                                 hotels_count_kb,
                                 distance_kb,
                                 price_kb)
from states.states import FSMbestdeal, FSMchoice

from database.database import user_dict, history_dict

from filters.filters import (check_city_name,
                             check_date,
                             check_check_out)


from hotels_API.API_req import get_user_hotels_data

router: Router = Router()

num_list = some_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']



@router.callback_query(Text(text='bestdeal'))
async def process_bestdeal_answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['bestdeal_greetings'],
                                     reply_markup=cancel_kb)

    await callback.message.answer(text=LEXICON['enter_city'])
    await state.set_state(FSMbestdeal.fill_city)


@router.callback_query(Text(text='cancel'))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(LEXICON['/start'], reply_markup=start_kb)



@router.message(FSMbestdeal.fill_city, check_city_name)
async def process_enter_city(message: Message, state: FSMContext):

    await message.answer(text=f'{LEXICON["city_name_ok"]} <b>{message.text}</b>')
    await message.answer(text=LEXICON['enter_adults'],
                         reply_markup=adults_kb)

    user_id = message.from_user.id

    if user_id not in user_dict:
        user_dict[user_id] = {}

    user_dict[user_id]['city_name'] = message.text
    user_dict[user_id]['search_command'] = 'bestdeal'

    await state.set_state(FSMbestdeal.fill_adults)


@router.message(FSMbestdeal.fill_city)
async def wrong_city(message: Message):
    await message.answer(text=LEXICON['city_name_wrong'])
    await message.delete()


@router.callback_query(FSMbestdeal.fill_adults, Text(text=['one', 'two', 'three', 'four']))
async def process_enter_adults(callback: CallbackQuery, state: FSMContext):

    some_list = ['one', 'two', 'three', 'four']
    result = some_list.index(callback.data) + 1
    user_dict[callback.from_user.id]['adults'] = result
    await callback.message.edit_text(text=LEXICON['enter_hotel_count'],
                                     reply_markup=hotels_count_kb)
    await state.set_state(FSMbestdeal.fill_hotels_count)

@router.message(FSMbestdeal.fill_adults)
async def wrong_adults(message: Message):

   await message.answer(text=LEXICON['wrong_adults'])


@router.callback_query(FSMbestdeal.fill_hotels_count, Text(text=num_list))
async def process_enter_hotelsCount(callback: CallbackQuery, state: FSMContext):

    result = num_list.index(callback.data) + 1
    user_dict[callback.from_user.id]['hotel_count'] = result
    await callback.message.edit_text(text=LEXICON['photo'], reply_markup=yes_no_kb)
    await state.set_state(FSMbestdeal.fill_photo)


@router.message(FSMbestdeal.fill_hotels_count)
async def wrong_hotels_count(message: Message):
    await message.answer(text=LEXICON['hotels_count_wrong'])
    await message.delete()


@router.callback_query(FSMbestdeal.fill_photo, Text(text=['yes', 'no']))
async def process_enter_photo(callback: CallbackQuery, state: FSMContext):

    if callback.data == 'yes':

        user_dict[callback.from_user.id]['photo'] = True
        await callback.message.edit_text(text=LEXICON['photo_count'],
                                      reply_markup=photo_count_kb)
        await state.set_state(FSMbestdeal.fill_photo_count)

    else:
        user_dict[callback.from_user.id]['photo'] = False
        user_dict[callback.from_user.id]['photo_count'] = 0
        await callback.message.edit_text(text=LEXICON['checkIn'])
        await state.set_state(FSMbestdeal.fill_ckeckIn)




@router.message(FSMbestdeal.fill_photo)
async def wrong_get_photo(message: Message):
    await message.answer(text=LEXICON['get_photo_wrong'])
    await message.delete()

@router.callback_query(FSMbestdeal.fill_photo_count, Text(text=['three', 'five', 'seven']))
async def process_enter_photocount(callback: CallbackQuery, state: FSMContext):

    if callback.data == 'three':
        user_dict[callback.from_user.id]['photo_count'] = 3
    elif callback.data == 'five':
        user_dict[callback.from_user.id]['photo_count'] = 5
    elif callback.data == 'seven':
        user_dict[callback.from_user.id]['photo_count'] = 7

    await callback.message.edit_text(text=LEXICON['checkIn'])
    await state.set_state(FSMbestdeal.fill_ckeckIn)


@router.message(FSMbestdeal.fill_photo_count)
async def wrong_photo_count(message: Message):
    await message.answer(text=LEXICON['wrong_photo_count'])


@router.message(FSMbestdeal.fill_ckeckIn, check_date)
async def process_enter_checkIn(message: Message, state: FSMContext):
    check_in = message.text.split('.')
    new_check_in = [int(i) for i in check_in]
    user_dict[message.from_user.id]['check_in'] = new_check_in
    await message.answer(text=LEXICON['checkOut'])
    await state.set_state(FSMbestdeal.fill_ckeckOut)

@router.message(FSMbestdeal.fill_ckeckIn)
async def wrong_checkIn(message: Message):
    await message.answer(text=LEXICON['wrong_date'])


@router.message(FSMbestdeal.fill_ckeckOut, check_date,  check_check_out)
async def process_enter_checkOut(message: Message, state: FSMContext):

    check_out = message.text.split('.')
    new_check_out = [int(i) for i in check_out]
    user_dict[message.from_user.id]['check_out'] = new_check_out
    await message.answer(text=LEXICON['distance_choiсe'],
                         reply_markup=distance_kb)
    await state.set_state(FSMbestdeal.fill_distance)


@router.message(FSMbestdeal.fill_ckeckOut)
async def wrong_checkIn(message: Message):
    await message.answer(text=LEXICON['wrong_date'])


@router.callback_query(FSMbestdeal.fill_distance, Text(text=['first', 'second', 'third', 'fourth']))
async def process_distanse_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'first':
        user_dict[callback.from_user.id]['distance'] = [0, 1]
    elif callback.data == 'second':
        user_dict[callback.from_user.id]['distance'] = [1, 3]
    elif callback.data == 'third':
        user_dict[callback.from_user.id]['distance'] = [3, 5]
    else:
        user_dict[callback.from_user.id]['distance'] = [5, 20]

    await callback.message.answer(text=LEXICON['price_choiсe'],
                                  reply_markup=price_kb)
    await state.set_state(FSMbestdeal.fill_price)

@router.callback_query(FSMbestdeal.fill_distance)
async def wrong_distance(message: Message):
    await message.answer(text=LEXICON['wrong_distance'])


@router.callback_query(FSMbestdeal.fill_price,Text(text=['first_price', 'second_price', 'third_price', 'fourth_price']))
async def process_price_choice(callback: CallbackQuery, state: FSMContext):

    if callback.data == 'first_price':
        user_dict[callback.from_user.id]['price'] = [0, 100]
    elif callback.data == 'second_price':
        user_dict[callback.from_user.id]['price'] = [100, 200]
    elif callback.data == 'third_price':
        user_dict[callback.from_user.id]['price'] = [200, 300]
    else:
        user_dict[callback.from_user.id]['price'] = [300, 1000]

    await callback.message.answer(text=LEXICON['results_wait'])

    result = get_user_hotels_data(user_dict[callback.from_user.id])

    if message.from_user.id not in history_dict:
        history_dict[callback.message.from_user.id] = {}

    history_dict[callback.message.from_user.id][str(datetime.datetime.now())] = {}
    history_dict[callback.message.from_user.id][str(datetime.datetime.now())]['request'] = user_dict[callback.message.from_user.id]
    history_dict[callback.message.from_user.id][str(datetime.datetime.now())]['response'] = result



    if result:

        for index, i_hotel in enumerate(result):
            for i_hotel_id, i_hotel_info in i_hotel.items():

                response = f'<b>{index + 1}{LEXICON["index"]}</b>\n' \
                           f'{LEXICON["hotel"]}  {i_hotel_info["name"]}\n' \
                           f'{LEXICON["distance_to_dt"]} {i_hotel_info["distance"]["value"]} {i_hotel_info["distance"]["unit"]}\n'\
                           f'{LEXICON["price_per_night"]} {i_hotel_info["price"]["per_night"]} {i_hotel_info["price"]["currency"]}\n' \
                           f'{LEXICON["total_price"]} {i_hotel_info["price"]["total"]} {i_hotel_info["price"]["currency"]}\n' \
                           f'{LEXICON["photos"]} \n'

                await callback.message.answer(text=response)
                media = []

                if i_hotel_info.get('photo', False):
                    for i_photo in i_hotel_info["photo"]:

                        photo = types.InputMediaPhoto(media=i_photo)
                        media.append(photo)

                    await callback.message.answer_media_group(media=media)
    else:
        await callback.message.answer(text=LEXICON['nothing_bestdeal'])


    await state.clear()
    await callback.message.answer(text=LEXICON['again'], reply_markup=yes_no_kb)
    await state.set_state(FSMchoice.get_choice)





