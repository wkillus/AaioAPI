import hashlib, requests
from urllib.parse import urlencode
from requests.exceptions import ConnectTimeout, ReadTimeout


class AaioAPI:
    def __init__(self, API_KEY, SECRET_KEY, MERCHANT_ID):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.MERCHANT_ID = MERCHANT_ID


    def get_balance(self):
        """Get Balance"""

        URL = 'https://aaio.io/api/balance'

        headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.API_KEY
        }

        try:
            response = requests.post(URL, headers=headers, timeout=(15, 60))
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


    def create_payment(self, order_id, amount, lang='ru', currency='RUB', description=None):
        """Creating of payment"""

        merchant_id = self.MERCHANT_ID # merchant id
        secret = self.SECRET_KEY # secret key №1 from shop settings


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
            'desc': description,
            'lang': lang
        }

        url_aaio = "https://aaio.io/merchant/pay?" + urlencode(params)


        return url_aaio

        
    def get_payment_info(self, order_id):
        """Get payment info"""

        URL = 'https://aaio.io/api/info-pay'

        params = {
            'merchant_id': self.MERCHANT_ID,
            'order_id': order_id
        }

        headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.API_KEY

        }

        response = requests.post(URL, data=params, headers=headers)
        response_json = response.json()

        return response_json    


    def is_expired(self, order_id):
        """Check status payment (expired)"""

        URL = 'https://aaio.io/api/info-pay'

        params = {
            'merchant_id': self.MERCHANT_ID,
            'order_id': order_id
        }

        headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.API_KEY

        }

        response = requests.post(URL, data=params, headers=headers)
        response_json = response.json()

        return response_json['type'] == 'success' and response_json['status'] == 'expired'


    def is_success(self, order_id):
        """Check status payment (success)"""

        URL = 'https://aaio.io/api/info-pay'

        params = {
            'merchant_id': self.MERCHANT_ID,
            'order_id': order_id
        }

        headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.API_KEY

        }

        response = requests.post(URL, data=params, headers=headers)
        response_json = response.json()

        return response_json['type'] == 'success' and response_json['status'] == 'success'