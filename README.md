<h1><img src="https://aaio.io/assets/landing/img/logo-m.svg" width=30 height=30> AAIO</h1>

A Library for easy work with [Aaio API](https://wiki.aaio.io/), in the Python programming language.  
Библиотека для легкой работы с [Aaio API](https://wiki.aaio.io/), на языке программирования Python.


 ## What is available in this library? - Что имеется в данной библиотеке?

- Creating a bill for payment - Создания счета для оплаты
- Quick check of payment status - Быстрая проверка статуса оплаты
- The largest number of payment methods - Наибольшее количество способов оплаты


## Installation - Установка

Required version [Python](https://www.python.org/): not lower than 3.7          
Требуемая версия [Python](https://www.python.org/): не ниже 3.7

```cmd
pip install AaioAPI
```


## Using - Использование
To get started, you need to register and get all the necessary store data [via this link on the official AAIO website](https://aaio.io/cabinet/merchants/)     
Чтобы начать работу, вам необходимо зарегистрироваться и получить все необходимые данные магазина [по этой ссылке на оф.сайте AAIO](https://aaio.io/cabinet/merchants/)

### Example of creating an invoice and receiving a payment link - Пример создания счета и получения ссылки на оплату
Здесь вам понадобятся данные вашего магазина
``` python
from AaioAPI import Aaio
import AaioAPI, time

payment = Aaio()

merchant_id = 'your_shop_id' # ID магазина
amount = 25 # Сумма к оплате
currency = 'RUB' # Валюта заказа
secret = 'your_secret_key' # Секретный ключ №1 из настроек магазина
desc = 'Test payment.' # Описание заказа

url_aaio = AaioAPI.pay(merchant_id, amount, currency, secret, desc)

print(url_aaio) # Ссылка на оплату
```

### Example of a status check - Пример проверки статуса
Проверяем статус платежа каждые 5 секунд с помощью цикла
```python
while True:
    AaioAPI.check_payment(url_aaio, payment)

    if payment.is_expired():                # Если счет просрочен
        print("Invoice was expired")
        break
    elif payment.is_success():              # Если оплата прошла успешно
        print("Payment was succesful")
        break
    else:                                   # Или если счет ожидает оплаты
        print("Invoice wasn't paid. Please pay the bill")
    time.sleep(5)
```



                                                                 
### Full Code - Полный код
```python
from AaioAPI import Aaio
import AaioAPI, time

payment = Aaio()

merchant_id = 'your_shop_id' # ID магазина
amount = 25 # Сумма к оплате
currency = 'RUB' # Валюта заказа
secret = 'your_secret_key' # Секретный ключ №1 из настроек магазина
desc = 'Test payment.' # Описание заказа

url_aaio = AaioAPI.pay(merchant_id, amount, currency, secret, desc)

print(url_aaio) # Ссылка на оплату


while True:
    AaioAPI.check_payment(url_aaio, payment)

    if payment.is_expired():                # Если счет просрочен
        print("Invoice was expired")
        break
    elif payment.is_success():              # Если оплата прошла успешно
        print("Payment was succesful")
        break
    else:                                   # Или если счет ожидает оплаты
        print("Invoice wasn't paid. Please pay the bill")
    time.sleep(5)
```

## License
MIT