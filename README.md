<h1><img src="https://aaio.io/assets/landing/img/logo-m.svg" width=30 height=30> AAIO</h1>

A Library for easy work with [Aaio API](https://wiki.aaio.io/), in the Python programming language.  
Библиотека для легкой работы с [Aaio API](https://wiki.aaio.io/), на языке программирования Python.


 ## What is available in this library? - Что имеется в данной библиотеке?

- Creating a bill for payment - Создание счета для оплаты
- Quick check of payment status - Быстрая проверка статуса оплаты
- Asynchronous / synchronous version - Асинхронная / синхронная версия
- Get balance - Получение баланса
- Get payment info - Получение информации о платежах


## Installation - Установка

Required version [Python](https://www.python.org/): not lower than 3.7          
Требуемая версия [Python](https://www.python.org/): не ниже 3.7

```cmd
pip install AaioAPI
```


## Using - Использование
To get started, you need to register and get all the necessary store data [via this link on the official AAIO website](https://aaio.io/cabinet/merchants/)     
Чтобы начать работу, вам необходимо зарегистрироваться и получить все необходимые данные магазина [по этой ссылке на оф.сайте AAIO](https://aaio.io/cabinet/merchants/)

### Get balance - Получение баланса
Чтобы получить доступ к балансу, скопируйте ваш [API Ключ](https://aaio.io/cabinet/api/)

Использование в синхронной версии:
```python
from AaioAPI import AaioAPI

client = AaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')
balance = client.get_balance()
balance = balance['balance']
# balance = {
#     "type": "success",
#     "balance": 50.43, // Текущий доступный баланс
#     "referral": 0, // Текущий реферальный баланс
#     "hold": 1.57 // Текущий замороженный баланс
#  }

print(balance)
```

Использование в асинхронной версии:
```python
from AaioAPI import AsyncAaioAPI
import asyncio

async def main():
    client = AsyncAaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')
    balance = await client.get_balance()
    balance = balance['balance']
    # balance = {
    #     "type": "success",
    #     "balance": 50.43, // Текущий доступный баланс
    #     "referral": 0, // Текущий реферальный баланс
    #     "hold": 1.57 // Текущий замороженный баланс
    #  }

    print(balance)


asyncio.run(main())
```

### Get payment info - Получение информации о платеже
Здесь пример получения информации о платеже

Использование в синхронной версии:
```python
from AaioAPI import AaioAPI

client = AaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')
order_id = 'my_id123' # Номер заказа
payment_info = client.get_payment_info(order_id)

print(payment_info)
```

Использование в синхронной версии:
```python
from AaioAPI import AsyncAaioAPI
import asyncio

async def main():
    client = AsyncAaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')
    order_id = 'my_id123' # Номер заказа
    payment_info = await client.get_payment_info(order_id)

    print(payment_info)


asyncio.run(main())
```

### Example of creating an invoice and receiving a payment link - Пример создания счета и получения ссылки на оплату
Здесь вам понадобятся [данные вашего магазина](https://aaio.io/cabinet/merchants/)

Использование в синхронной версии:
```python
from AaioAPI import AaioAPI
import time

client = AaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')

order_id = 'my_id123' # Номер заказа
amount = 25 # Сумма к оплате
lang = 'ru' # Язык страницы
currency = 'RUB' # Валюта заказа
desc = 'Test payment.' # Описание заказа

URL = client.create_payment(order_id, amount, lang, currency, desc)

print(URL) # Ссылка на оплату
```

Использование в aсинхронной версии:
```python
from AaioAPI import AsyncAaioAPI
import asyncio

async def main():
    client = AsyncAaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')

    order_id = 'my_id123' # Номер заказа
    amount = 25 # Сумма к оплате
    lang = 'ru' # Язык страницы
    currency = 'RUB' # Валюта заказа
    desc = 'Test payment.' # Описание заказа

    URL = await client.create_payment(order_id, amount, lang, currency, desc)

    print(URL) # Ссылка на оплату


asyncio.run(main())
```

### Example of a status check - Пример проверки статуса
Проверяем статус платежа каждые 5 секунд с помощью цикла

Использование в синхронной версии:
```python
while True:

    if client.is_expired(order_id):                # Если счет просрочен
        print("Invoice was expired")
        break
    elif client.is_success(order_id):              # Если оплата прошла успешно
        print("Payment was succesful")
        break
    else:                                   # Или если счет ожидает оплаты
        print("Invoice wasn't paid. Please pay the bill")
    time.sleep(5)
```

Использование в асинхронной версии:
```python
while True:

    if await client.is_expired(order_id):                # Если счет просрочен
        print("Invoice was expired")
        break
    elif await client.is_success(order_id):              # Если оплата прошла успешно
        print("Payment was succesful")
        break
    else:                                                # Или если счет ожидает оплаты
        print("Invoice wasn't paid. Please pay the bill")
    await asyncio.sleep(5)
```


### Full Code - Полный код
Синхронная версия:
```python
from AaioAPI import AaioAPI
import time

client = AaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')

order_id = 'my_id123' # Номер заказа
amount = 25 # Сумма к оплате
lang = 'ru' # Язык страницы
currency = 'RUB' # Валюта заказа
desc = 'Test payment.' # Описание заказа

URL = client.create_payment(order_id, amount, lang, currency, desc)

print(URL) # Ссылка на оплату


while True:

    if client.is_expired(order_id):                # Если счет просрочен
        print("Invoice was expired")
        break
    elif client.is_success(order_id):              # Если оплата прошла успешно
        print("Payment was succesful")
        break
    else:                                          # Или если счет ожидает оплаты
        print("Invoice wasn't paid. Please pay the bill")
    time.sleep(5)
```

Асинхронная версия:
```python
from AaioAPI import AsyncAaioAPI
import asyncio


async def main():
    client = AsyncAaioAPI('API KEY', 'SECRET №1', 'MERCHANT ID')

    order_id = 'my_id123' # Номер заказа
    amount = 25 # Сумма к оплате
    lang = 'ru' # Язык страницы
    currency = 'RUB' # Валюта заказа
    desc = 'Test payment.' # Описание заказа

    URL = await client.create_payment(order_id, amount, lang, currency, desc)

    print(URL) # Ссылка на оплату


    while True:

        if await client.is_expired(order_id):                # Если счет просрочен
            print("Invoice was expired")
            break
        elif await client.is_success(order_id):              # Если оплата прошла успешно
            print("Payment was succesful")
            break
        else:                                                # Или если счет ожидает оплаты
            print("Invoice wasn't paid. Please pay the bill")
        await asyncio.sleep(5)


asyncio.run(main())
```

## License
MIT