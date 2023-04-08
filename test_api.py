import json
from hotels_API.API_req import get_user_hotels_data


# response_data: dict = {
#     'city_name': "Лондон",
#     'check_in': [23, 4, 2023],
#     'check_out': [26, 4, 2023],
#     'adults': 2,
#     'search_command': 'bestdeal',
#     'hotel_count': 5,
#     'photo': True,
#     'photo_count': 5,
#     'price': [0, 250],
#     'distance': [0, 20]
# }

# response_data: dict = {
#     'city_name': "Лондон",
#     'check_in': [23, 4, 2023],
#     'check_out': [26, 4, 2023],
#     'adults': 2,
#     'search_command': 'lowprice',
#     'hotel_count': 5,
#     'photo': True,
#     'photo_count': 5,
#
# }

response_data: dict = {'city_name': 'Париж',
                       'search_command': 'highprice',
                       'adults': 2, 'hotel_count': 6,
                       'photo': True, 'photo_count': 3,
                       'check_in': [23, 5, 2023],
                       'check_out': [24, 5, 2023]}


res = get_user_hotels_data(user_request=response_data)

with open('data.json', 'w', encoding='utf-8') as data_file:
    json.dump(res, data_file, indent=4)

