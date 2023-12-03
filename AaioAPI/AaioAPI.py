import hashlib, random, requests
from urllib.parse import urlencode
from requests.exceptions import ConnectTimeout, ReadTimeout


class AaioAPI:
    def __init__(self, API_KEY, SECRET_KEY=None, MERCHANT_ID=None):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.MERCHANT_ID = MERCHANT_ID


    def get_balance(self):
        """Get Balance"""

        url = 'https://aaio.io/api/balance'

        headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.API_KEY
        }

        try:
            response = requests.post(url, headers=headers, timeout=(15, 60))
        except ConnectTimeout:
            return 'ConnectTimeout' # Не хватило времени на подключение к сайту
        
        except ReadTimeout:
            return 'ReadTimeout' # Не хватило времени на выполнение запроса

        if(response.status_code in [200, 400, 401]):
            try:
                response_json = response.json() # Парсинг результата
            except:
                return 'Не удалось пропарсить ответ'

            if(response_json['type'] == 'success'):
                return response_json
            else:
                return 'Ошибка: ' + response_json['message'] # Вывод ошибки
        else:
            return 'Response code: ' + str(response.status_code) # Вывод неизвестного кода ответа


    def create_payment(self, amount=20, currency='RUB', description=None):
        """Creating of payment"""

        rand = "1234567890"
        number = ''
        for i in range(10):
            number = number + random.choice(list(rand))

        merchant_id = self.MERCHANT_ID # merchant id

        amount_aaio = amount # amount

        currency_aaio = currency # currency

        secret = self.SECRET_KEY # secret key №1 from shop settings

        order_id = number # order id

        desc = description # order description

        lang = 'ru' # lang of form


        sign = f':'.join([
            str(merchant_id),
            str(amount_aaio),
            str(currency_aaio),
            str(secret),
            str(order_id)
        ])

        params = {
            'merchant_id': merchant_id,
            'amount': amount_aaio,
            'currency': currency_aaio,
            'order_id': order_id,
            'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
            'desc': desc,
            'lang': lang
        }

        url_aaio = "https://aaio.io/merchant/pay?" + urlencode(params)


        return url_aaio

        
    def is_expired(self, url: str):
        """Check status payment (expired)"""

        response = requests.get(url)

        if '<span class="mb-2">Заказ просрочен. Оплатить заказ необходимо было' in response.content.decode():
            return True
        else:
            return False
    

    def is_success(self, url: str):
        """Check status payment (success)"""

        response = requests.get(url)

        if '<span class="mb-2">Заказ успешно был оплачен</span>' in response.content.decode():
            return True
        else:
            return False