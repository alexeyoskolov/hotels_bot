from datetime import datetime, date

from aiogram.types import Message, ContentType
from hotels_API.API_req import _get_city_id

from database.database import user_dict



def check_city_name(message: Message) -> bool:

    if message.content_type != ContentType.TEXT:
        return False
    elif not message.text.isalpha():
        return False
    else:

        if _get_city_id(message.text):
           return True
        else:
           return False


def check_date(message: Message) -> bool:

    if message.content_type != ContentType.TEXT:
        return False
    else:
        count = 0
        user_date = message.text.split('.'  )



        for i in user_date:
            if i.isdigit():
                count += 1
        if count == len(user_date):

            try:

                cur_date = date.today()
                user_date = date(int(user_date[2]), int(user_date[1]), int(user_date[0]))

                if user_date >= cur_date and (user_date.year - cur_date.year <= 1):
                    return True

                else:
                    return False


            except Exception:
                return False


        else:
            return False

def check_check_out(message: Message):

    global user_dict

    user_date = message.text.split('.')
    int_user_date = [int(i) for i in user_date]

    if int_user_date <= user_dict[message.from_user.id]['check_in']:
        return False
    else:
        return True