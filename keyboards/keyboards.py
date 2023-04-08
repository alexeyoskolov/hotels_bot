from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.LEXICON import LEXICON


def create_inline_kb(width: int, **kwargs):

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for cb_data, text in kwargs.items():
            button = InlineKeyboardButton(text=text,
                                          callback_data=cb_data)
            buttons.append(button)
    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()


start_kb = create_inline_kb(width=1,
                            lowprice=LEXICON['lowprice'],
                            highprice=LEXICON['highprice'],
                            bestdeal=LEXICON['bestdeal'])

cancel_kb = create_inline_kb(width=1,  cancel=LEXICON['cancel'])

yes_no_kb = create_inline_kb(width=2, yes=LEXICON['yes'], no=LEXICON['no'])

photo_count_kb = create_inline_kb(width=4,
                                  three=LEXICON['three'],
                                  five=LEXICON['five'],
                                  seven=LEXICON['seven'])
adults_kb = create_inline_kb(width=4,
                             one=LEXICON['one'],
                             two=LEXICON['two'],
                             three=LEXICON['three'],
                             four=LEXICON['four'])
hotels_count_kb = create_inline_kb(width=2,
                                    one=LEXICON['one'],
                                    two=LEXICON['two'],
                                    three=LEXICON['three'],
                                    four=LEXICON['four'],
                                    five=LEXICON['five'],
                                    six=LEXICON['six'],
                                    seven=LEXICON['seven'],
                                    eigth=LEXICON['eight'],
                                    nine=LEXICON['nine'],
                                    ten=LEXICON['ten'])

distance_kb = create_inline_kb(width=4,
                               first=LEXICON['first_dist'],
                               second=LEXICON['second_dist'],
                               third=LEXICON['third_dist'],
                               fourth=LEXICON['fourth_dist'])

price_kb = create_inline_kb(width=4,
                            first_price=LEXICON['first_price'],
                            second_price=LEXICON['second_price'],
                            third_price=LEXICON['third_price'],
                            fourth_price=LEXICON['fourth_price'])

