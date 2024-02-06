import hashlib, requests
from urllib.parse import urlencode
from requests.exceptions import ConnectTimeout, ReadTimeout


class AaioAPI:
    def __init__(self, API_KEY, SECRET_KEY, MERCHANT_ID):
        """
        Creates instance of one AAIO merchant API client

        Args:
            merchant_id: Merchant ID from https://aaio.so/cabinet
            secret: 1st secret key from https://aaio.so/cabinet
            api_key: API key from https://aaio.so/cabinet/api
        """

        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.MERCHANT_ID = MERCHANT_ID


    def get_balance(self):
        """
        Creates a request for get balances of user
        See https://wiki.aaio.so/api/poluchenie-balansa

        Returns: Model from response JSON
        """

        URL = 'https://aaio.so/api/balance'

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


    def create_payment(self, order_id, 
                       amount, lang='ru', 
                       currency='RUB', description=None):
        """
        Creates payment URL
        See https://wiki.aaio.so/priem-platezhei/sozdanie-zakaza for more detailed information

        Args:
            amount: Payment amount
            order_id: Your order id
            description: Payment description (Optional)
            currency: Payment currency
            language: Page language (Optional)

        Returns: Payment URL

        """

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

        url_aaio = "https://aaio.so/merchant/pay?" + urlencode(params)


        return url_aaio

        
    def get_payment_info(self, order_id):
        """
        Creates a request for get payment information
        See https://wiki.aaio.so/api/informaciya-o-zakaze

        Args:
            order_id: Your order ID

        Returns: Model from response JSON

        """

        URL = 'https://aaio.so/api/info-pay'

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

        response_json = self.get_payment_info(order_id)

        return response_json['type'] == 'success' and response_json['status'] == 'expired'


    def is_success(self, order_id):
        """Check status payment (success)"""

        response_json = self.get_payment_info(order_id)

        return (response_json['type'] == 'success' and response_json['status'] == 'success') or \
               (response_json['type'] == 'success' and response_json['status'] == 'hold')