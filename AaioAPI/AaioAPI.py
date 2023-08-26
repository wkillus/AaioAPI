import hashlib, random, requests, sys
from urllib.parse import urlencode
from requests.exceptions import ConnectTimeout, ReadTimeout


class Aaio:
    """Класс возвращении статусов платежей"""
    def __init__(self):
        self.status = None

    def set(self, status):
        self.status = status

    def is_expired(self):
        return self.status == "expired"

    def is_success(self):
        return self.status == "success"


def get_balance(api_key):
    url = 'https://aaio.io/api/balance'

    headers = {
        'Accept': 'application/json',
        'X-Api-Key': api_key
    }

    try:
        response = requests.post(url, headers=headers, timeout=(15, 60))
    except ConnectTimeout:
        print('ConnectTimeout') # Не хватило времени на подключение к сайту
        sys.exit()
    except ReadTimeout:
        print('ReadTimeout') # Не хватило времени на выполнение запроса
        sys.exit()

    if(response.status_code in [200, 400, 401]):
        try:
            response_json = response.json() # Парсинг результата
        except:
            print('Не удалось пропарсить ответ')
            sys.exit()

        if(response_json['type'] == 'success'):
            return response_json
        else:
            print('Ошибка: ' + response_json['message']) # Вывод ошибки
    else:
        print('Response code: ' + str(response.status_code)) # Вывод неизвестного кода ответа


def pay(merchant_id_aaio, amount_aaio, currency_aaio, secret_aaio, desc_aaio):
    """Генерация рандомных чисел для  № заказа"""
    rand = "1234567890"
    number = ''
    for i in range(10):
        number = number + random.choice(list(rand))


    """ID магазина"""
    merchant_id = merchant_id_aaio

    """Сумма к оплате"""
    amount = amount_aaio

    """Валюта заказа"""
    currency = currency_aaio

    """Секретный ключ №1 из настроек магазина"""
    secret = secret_aaio

    """Идентификатор заказа в системе"""
    order_id = number

    """Описание заказа"""
    desc = desc_aaio

    """Язык формы"""
    lang = 'ru'


    sign = f':'.join([
        str(merchant_id),
        str(amount),
        str(currency),
        str(secret),
        str(order_id)
    ])

    params = {
        'merchant_id': merchant_id,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': desc,
        'lang': lang
    }

    url_aaio = "https://aaio.io/merchant/pay?" + urlencode(params)

    return url_aaio


def check_payment(url_aaio, payment):
    """Функция проверки статуса оплаты"""
    response = requests.get(url_aaio)

    if '<span class="mb-2">Заказ просрочен. Оплатить заказ необходимо было' in response.content.decode():
        payment.set("expired")
    elif '<span class="mb-2">Заказ успешно был оплачен</span>' in response.content.decode():
        payment.set("success")
    else:
        pass

    return response