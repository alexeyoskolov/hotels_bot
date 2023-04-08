import requests
import json
from config import HEADERS, URL


def _body_city_search(city_name: str) -> dict:

    """
    Возвращает тело запроса по введенному городу
    :param city_name: str
    :return: тело запроса
    """

    return {'q': city_name, 'locale': 'ru_RU'}


def _get_city_id(user_city_name: str) -> str|bool:
    """
    Возвращает cловарь ID города и координаты центра, если такой существует.
    Если по имени города нет 100% совпадений, то возвращает
    предупреждение.
    Достаем отсюда ID и координаты
    :param user_city_name: str
    :return:  int | str
    """


    url = f"{URL}locations/v3/search"

    params = _body_city_search(city_name=user_city_name)
    response = requests.request('GET',
                                url=url,
                                params=params,
                                headers=HEADERS)

    result = json.loads(response.text)

    user_city_name: str = result.get('q')

    if user_city_name.lower() == result.get('sr')[0].get('regionNames').get('shortName').lower():

        city_id: str = result.get('sr')[0].get('gaiaId')

        return city_id

    else:
        return None


def _body_hotels_search (user_response: dict) -> dict:
    """
    Функция. Возвращает тело запроса, составленное с использованием
    следующих параметров.
    :param user_response: dict - Содержит информацию, собранную от пользователяЖ
        'city_name': "Лондон" - Название города
        'check_in': [23, 4, 2023] - Дата заселения [Д, М, Г]
        'check_out': [26, 4, 2023] - Дата выселения [Д, М, Г]
        'adults': 2 - кол-во человек
        'search_command': 'bestdeal' - Формат поиска (lowprice, highprice, bestdeal)
        'hotel_count': 5 - Кол-во отелей, которые необходимо вывести в результате (default <= 10)
        'photo': True - Нужны ли фото
        'photo_count': 5 - Если нужны, то сколько
        'price': [0, 250] - Диапазон цен (только для bestdeal)
        'distance': [0, 20] - Диапазон расстояний от центра (только для bestdeal)
    :return: dict Тело запроса
    """



    sort_dict: dict = {"low": "PRICE_LOW_TO_HIGH",
                       "high": "PRICE_HIGH_TO_LOW",
                       "dist": "DISTANCE"}

    city_id = _get_city_id(user_city_name=user_response['city_name'])

    if not city_id.isdigit():

        raise TypeError

    else:

        if user_response['search_command'] in ('lowprice', 'highprice'):
            sort_type = sort_dict["low"]
            filters_dict: dict[str] = {'availableFilter': ' SHOW_AVAILABLE_ONLY'}


        elif user_response['search_command'] == 'bestdeal':
            sort_type = sort_dict["dist"]
            filters_dict: dict[str] = {"price": {"max": user_response['price'][1], "min": user_response['price'][0]},
                                       'availableFilter': ' SHOW_AVAILABLE_ONLY'}

        else:
            sort_type = sort_dict["low"]
            filters_dict: dict[str] = {'availableFilter': ' SHOW_AVAILABLE_ONLY'}


        req_body =  {
            "currency": "EUR",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": str(city_id)},
            "checkInDate": {
                "day": user_response['check_in'][0],
                "month": user_response['check_in'][1],
                "year": user_response['check_in'][2]
            },
            "checkOutDate": {
                "day": user_response['check_out'][0],
                "month": user_response['check_out'][1],
                "year": user_response['check_out'][2]
            },
            "rooms": [
                {
                    "adults": user_response['adults']
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 200,
            "sort": sort_type,
            "filter": filters_dict
        }

        return req_body


def _get_all_hotels_response(user_request: dict) -> list:
    """
    Функция. Возвращает запрос составленный на основе тела запроса.
    Содержит перечень всех доступных отелей в городе.
    :param req_body: dict - Тело запроса
    :return: Ответ о всех доступных отелях
    """

    req_body = _body_hotels_search(user_request)

    url = f"{URL}properties/v2/list"

    response = requests.request("POST", url, json=req_body, headers=HEADERS)
    result = json.loads(response.text)

    all_hotels_prop = result['data']["propertySearch"]["properties"]



    return all_hotels_prop


def _add_photo(hotel_id: int, photo_count:int) -> list:
    """
    Функция. Принимает ID отеля и кол-во необходимых фото(N).
    Возвращает словарь, содержащий N url из галереи фотографий отеля

    :param hotel_id: int - кол-во отелей
    :param photo_count: - кол-во фото
    :return: user_photo: list
    """

    url = f"{URL}properties/v2/detail"

    payload = {
        "currency": "EUR",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": str(hotel_id)
    }

    response = requests.request("POST", url, json=payload, headers=HEADERS)
    result = json.loads(response.text)
    photo_gallery: dict = result['data']['propertyInfo']['propertyGallery']['images']
    user_photo: list = []
    count = 0

    for i_photo_data in photo_gallery:
        if count == photo_count:
            break
        user_photo.append(i_photo_data['image']['url'])
        count += 1


    return user_photo


def _create_hotel_info(hotel_data: dict, user_request: dict) -> dict:
    """
    Функция. Принимает на вход данные об отеле и формирует словарь с необходимой
    пользователю информацией. Переформатирует информацию об отеле.
    :param hotel_data: dict - информация об N-ом отеле из запроса _get_all_hotels_response
    :param user_response: dict - словарь, содержащий данные, полученные от пользователя
    :return: hotel_dict: dict - словарь, который содержит необходимую информацию об отеле
    """

    new_hotel_data: dict = {}

    new_hotel_data['name'] = hotel_data.get('name')
    new_hotel_data['distance'] = {
        'value': hotel_data.get("destinationInfo").get("distanceFromDestination")['value'],
        'unit': hotel_data["destinationInfo"]["distanceFromDestination"]['unit']}

    total_price_message = hotel_data["price"]["displayMessages"][1]["lineItems"][0]["value"]
    total_price = total_price_message.split()[0][1:]
    currency = total_price_message.split()[0][0]
    price_per_night = hotel_data["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"][1:]
    new_hotel_data['price'] = {'total': total_price,
                               'currency': currency,
                               'per_night': price_per_night}

    new_hotel_data['coordinates'] = {'lat': hotel_data.get("mapMarker").get("latLong").get("latitude"),
                                     'long': hotel_data.get("mapMarker").get("latLong").get("longitude")}
    if user_request['photo_count']:
        new_hotel_data['photo'] = _add_photo(hotel_id=hotel_data['id'],
                                             photo_count=user_request['photo_count'])

    hotel_dict = {int(hotel_data.get('id')): new_hotel_data}

    return hotel_dict


def _get_bestdeal(all_hotels_list: list, user_response: dict) -> list:
    """
    Функция. Производит отбор только тех отелей, которые соответствуют условиям
    :param all_hotels_list: list -  список всех доступных отелей
    :param user_response: dict - - словарь, содержащий данные, полученные от пользователя
    :return: user_hotels_list - словарь, содержащий информацию об N отелях в нужном формате
    """

    user_price_interval = user_response['price']
    user_dist_interval = user_response['distance']

    user_hotels_list: list = []
    count = 0

    for i_hotel in all_hotels_list:

        if count == user_response['hotel_count'] or count == 10:
            break

        HP_per_night: str = i_hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"][1:]

        if ',' in HP_per_night:
            HP_per_night = f'{HP_per_night[0]}{HP_per_night[2::]}'

        hotel_distance = i_hotel["destinationInfo"]["distanceFromDestination"]['value']

        if user_price_interval[0] <= int(HP_per_night) <= user_price_interval[1] and \
                user_dist_interval[0] <= hotel_distance <= user_dist_interval[1]:

            hotel_dict = _create_hotel_info(hotel_data=i_hotel, user_request=user_response)
            user_hotels_list.append(hotel_dict)
            count += 1


    return user_hotels_list


def get_user_hotels_data(user_request: dict) -> list:
    """
    Функция. Принимает словарь необходимых параметров от пользователя и
    возвращает отформатированный список отелей
    :param user_request: dict - запрос от пользователя
    :return: user_hotels_list - финальный список отелей
    """

    count = 0
    user_hotels_list: list = []
    all_hotels_list = _get_all_hotels_response(user_request=user_request)

    if user_request['search_command'] == 'lowprice':

        for i_hotel in all_hotels_list:

            if (count == user_request['hotel_count']) or (count == 10):
                break

            hotel_dict = _create_hotel_info(hotel_data=i_hotel,
                                         user_request=user_request)

            user_hotels_list.append(hotel_dict)

            count += 1

    elif user_request['search_command'] == 'highprice':

        all_hotels_count = len(all_hotels_list)

        for i in range(all_hotels_count, -1, -1):

            if (count == user_request['hotel_count']) or (count == 10):
                break

            hotel_dict = _create_hotel_info(hotel_data=all_hotels_list[i-1],
                                            user_request=user_request)

            user_hotels_list.append(hotel_dict)

            count += 1

    else:

        user_hotels_list = _get_bestdeal(all_hotels_list, user_response=user_request)


    return user_hotels_list


