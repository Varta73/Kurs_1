from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
import requests_mock

from src.utils import cost_promotion, currency_rates, filter_cards, get_greeting, read_excel, top_transaction

# ROOT_PATH = Path(__file__).resolve().parent.parent
test_list = read_excel("../data/operations.xlsx")
nul_list = []


# def test_get_greeting():
#     # greeting = get_greeting()
#     assert get_greeting == "Доброе утро" or "Добрый день" or "Добрый вечер" or "Доброй ночи"


def test_get_greeting():
    """Тестирование функции-приветствия"""
    assert get_greeting() == "Доброй ночи"


def test_filter_cards(test_transactions):
    """Тестирование функции, создающей информацию по каждой карте"""
    assert filter_cards(test_transactions) == [{'Номер карты': '7197',
                                                'Всего потрачено': 3337.0,
                                                'Кэшбэк': 33.37},
                                               {'Номер карты': '5091',
                                                'Всего потрачено': 571.07,
                                                'Кэшбэк': 5.71}]


def test_filter_cards_nul():
    """Тестирование функции, создающей информацию по каждой карте с пустым списком"""
    assert filter_cards(nul_list) == []


@pytest.fixture
def test_transactions():
    return [
        {'Дата операции': '03.01.2018 14:55:21',
         'Дата платежа': '05.01.2018',
         'Статус': 'OK',
         'Сумма платежа': -21.0,
         'Валюта платежа': 'RUB',
         'Категория': 'Красота',
         'Описание': 'OOO Balid',
         'Номер карты': '*7197'},
        {'Дата операции': '01.01.2018 20:27:51',
         'Дата платежа': '04.01.2018',
         'Статус': 'OK',
         'Сумма платежа': -316.0,
         'Валюта платежа': 'RUB',
         'Категория': 'Красота',
         'Описание': 'OOO Balid',
         'Номер карты': '*7197'},
        {'Дата операции': '01.01.2018 12:49:53',
         'Дата платежа': '01.01.2018',
         'Статус': 'OK',
         'Сумма платежа': -3000.0,
         'Валюта платежа': 'RUB',
         'Категория': 'Переводы',
         'Описание': 'Линзомат ТЦ Юность',
         'Номер карты': '*7197'},
        {'Дата операции': '31.12.2021 01:23:42',
         'Дата платежа': '31.12.2021',
         'Статус': 'OK',
         'Сумма платежа': -564.0,
         'Валюта платежа': 'RUB',
         'Категория': 'Различные товары',
         'Описание': 'Ozon.ru',
         'Номер карты': '*5091'},
        {'Дата операции': '30.12.2021 19:18:22',
         'Дата платежа': '31.12.2021',
         'Статус': 'OK',
         'Сумма платежа': -7.07,
         'Валюта платежа': 'RUB',
         'Категория': 'Каршеринг',
         'Описание': 'Ситидрайв',
         'Номер карты': '*5091'}
    ]


# @pytest.mark.parametrize(
#     "input_date_str, expected_result",
#     [
#         (
#             "20.06.2023",
#             [
#                 {
#                     "Дата операции": "01.06.2023 12:00:00",
#                     "Сумма операции": "-100.50",
#                     "Категория": "Покупки",
#                     "Описание": "Магазин",
#                 },
#                 {
#                     "Дата операции": "15.06.2023 18:30:00",
#                     "Сумма операции": "-250.00",
#                     "Категория": "Ресторан",
#                     "Описание": "Ужин",
#                 },
#                 {
#                     "Дата операции": "20.06.2023 10:00:00",
#                     "Сумма операции": "-75.00",
#                     "Категория": "Транспорт",
#                     "Описание": "Такси",
#                 },
#             ],
#         ),
#         (
#             "15.05.2023",
#             [
#                 {
#                     "Дата операции": "05.05.2023 08:15:00",
#                     "Сумма операции": "-500.00",
#                     "Категория": "Медицина",
#                     "Описание": "Аптека",
#                 },
#             ],
#         ),
#     ],
# )


def test_top_transaction():
    """Тестирование функции для получения топ-5 транзакций по сумме платежа, в обычном режиме"""
    print(top_transaction(test_list))


# def test_greeting(mock_datetime, current_hour, expected_greeting):
#     mock_now = datetime(2023, 6, 20, current_hour, 0, 0)
#     mock_datetime.now.return_value = mock_now
#     result = get_greeting()
#     assert result == expected_greeting
#
#
# def test_get_cards_data_empty():
#     transactions = []
#     expected_result = []
#     assert get_cards_data(transactions) == expected_result
#
#
# def test_get_cards_data_single_transaction():
#     transactions = [{"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"}]
#     expected_result = [{"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0}]
#     assert get_cards_data(transactions) == expected_result
#
#
# def test_get_cards_data_multiple_transactions():
#     transactions = [
#         {"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"},
#         {"Номер карты": "1234", "Сумма операции": "-200.0", "Кэшбэк": "2.0", "Категория": "Продукты"},
#         {"Номер карты": "5678", "Сумма операции": "-50.0", "Кэшбэк": "0.5", "Категория": "Продукты"},
#     ]
#     expected_result = [
#         {"last_digits": "1234", "total_spent": 300.0, "cashback": 3.0},
#         {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
#     ]
#     assert get_cards_data(transactions) == expected_result
#
#
# def test_get_cards_data_nan_card_number():
#     transactions = [
#         {"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"},
#         {"Номер карты": "nan", "Сумма операции": "-200.0", "Кэшбэк": "2.0", "Категория": "Продукты"},
#         {"Номер карты": "5678", "Сумма операции": "-50.0", "Кэшбэк": "0.5", "Категория": "Продукты"},
#     ]
#     expected_result = [
#         {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
#         {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
#     ]
#     assert get_cards_data(transactions) == expected_result
#
#
# def test_get_cards_data_cashback():
#     transactions = [
#         {"Номер карты": "1234", "Сумма операции": "-100.0", "Категория": "Продукты"},
#         {"Номер карты": "5678", "Сумма операции": "-50.0", "Категория": "Продукты"},
#     ]
#     expected_result = [
#         {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
#         {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
#     ]
#     assert get_cards_data(transactions) == expected_result
#
#
# def test_get_top_transaction_empty():
#     transactions = []
#     expected_result = []
#     assert get_top_transaction(transactions) == expected_result
#
#
# def test_get_top_5_transactions_single_transaction():
#     transactions = [
#         {
#             "Дата операции": "20.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Еда",
#             "Описание": "Покупка еды",
#         }
#     ]
#     expected_result = [{"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"}]
#     assert get_top_5_transactions(transactions) == expected_result
#
#
# def test_get_top_5_transactions_multiple_transactions():
#     transactions = [
#         {
#             "Дата операции": "20.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Еда",
#             "Описание": "Покупка еды",
#         },
#         {
#             "Дата операции": "21.06.2023 12:00:00",
#             "Сумма операции": "-200.0",
#             "Категория": "Транспорт",
#             "Описание": "Оплата проезда",
#         },
#         {
#             "Дата операции": "22.06.2023 12:00:00",
#             "Сумма операции": "-50.0",
#             "Категория": "Развлечения",
#             "Описание": "Кино",
#         },
#         {
#             "Дата операции": "23.06.2023 12:00:00",
#             "Сумма операции": "-300.0",
#             "Категория": "Магазины",
#             "Описание": "Покупка одежды",
#         },
#         {
#             "Дата операции": "24.06.2023 12:00:00",
#             "Сумма операции": "-20.0",
#             "Категория": "Кофе",
#             "Описание": "Кофе на вынос",
#         },
#         {
#             "Дата операции": "25.06.2023 12:00:00",
#             "Сумма операции": "-400.0",
#             "Категория": "Магазины",
#             "Описание": "Покупка техники",
#         },
#     ]
#     expected_result = [
#         {"date": "25.06.2023", "amount": "-400.0", "category": "Магазины", "description": "Покупка техники"},
#         {"date": "23.06.2023", "amount": "-300.0", "category": "Магазины", "description": "Покупка одежды"},
#         {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
#         {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
#         {"date": "22.06.2023", "amount": "-50.0", "category": "Развлечения", "description": "Кино"},
#     ]
#     assert get_top_5_transactions(transactions) == expected_result
#
#
# def test_get_top_5_transactions_less_than_5():
#     transactions = [
#         {
#             "Дата операции": "20.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Еда",
#             "Описание": "Покупка еды",
#         },
#         {
#             "Дата операции": "21.06.2023 12:00:00",
#             "Сумма операции": "-200.0",
#             "Категория": "Транспорт",
#             "Описание": "Оплата проезда",
#         },
#     ]
#     expected_result = [
#         {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
#         {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
#     ]
#     assert get_top_5_transactions(transactions) == expected_result
#
#
# def test_get_top_5_transactions_with_equal_amounts():
#     transactions = [
#         {
#             "Дата операции": "20.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Еда",
#             "Описание": "Покупка еды",
#         },
#         {
#             "Дата операции": "21.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Транспорт",
#             "Описание": "Оплата проезда",
#         },
#         {
#             "Дата операции": "22.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Развлечения",
#             "Описание": "Кино",
#         },
#         {
#             "Дата операции": "23.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Магазины",
#             "Описание": "Покупка одежды",
#         },
#         {
#             "Дата операции": "24.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Кофе",
#             "Описание": "Кофе на вынос",
#         },
#         {
#             "Дата операции": "25.06.2023 12:00:00",
#             "Сумма операции": "-100.0",
#             "Категория": "Магазины",
#             "Описание": "Покупка техники",
#         },
#     ]
#     expected_result = [
#         {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
#         {"date": "21.06.2023", "amount": "-100.0", "category": "Транспорт", "description": "Оплата проезда"},
#         {"date": "22.06.2023", "amount": "-100.0", "category": "Развлечения", "description": "Кино"},
#         {"date": "23.06.2023", "amount": "-100.0", "category": "Магазины", "description": "Покупка одежды"},
#         {"date": "24.06.2023", "amount": "-100.0", "category": "Кофе", "description": "Кофе на вынос"},
#     ]
#     assert get_top_5_transactions(transactions) == expected_result
#
#
# @pytest.fixture
# def api_key_currency():
#     return "test_api_key"


# def test_currency_rates_success(api_key_currency):
#     currencies = ["USD", "EUR"]
#     expected_result = [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 90.0}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/USD",
#             json={"conversion_rates": {"RUB": 75.0}},
#         )
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/EUR",
#             json={"conversion_rates": {"RUB": 90.0}},
#         )
#
#         assert currency_rates(currencies, api_key_currency) == expected_result

@patch("requests.get")
def test_currency_rates(mock_get):
    mock_get.return_value.status.code.return_value = 200
    mock_get.return_value.json.return_value = {"base": "EUR", "date": "2024-07-18", "rates": {"RUB": 96.62},
                                               "success": True, "timestamp": 1721291536}
    assert currency_rates() == [{'Валюта': 'USD', 'Курс': 95.8}, {'Валюта': 'EUR', 'Курс': 104.18}]


# def test_get_currency_rates_partial_failure(api_key_currency):
#     currencies = ["USD", "EUR"]
#     expected_result = [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": None}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/USD",
#             json={"conversion_rates": {"RUB": 75.0}},
#         )
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/EUR", status_code=404, text="Not Found"
#         )
#
#         assert currency_rates(currencies, api_key_currency) == expected_result
#
#
# def test_get_exchange_rates_all_failure(api_key_currency):
#     currencies = ["USD", "EUR"]
#     expected_result = [{"currency": "USD", "rate": None}, {"currency": "EUR", "rate": None}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/USD", status_code=500, text="Server Error"
#         )
#         mocker.get(
#             f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/EUR", status_code=500, text="Server Error"
#         )
#
#         assert currency_rates(currencies, api_key_currency) == expected_result
#
#
# @pytest.fixture
# def api_key_stocks():
#     return "test_api_key"
#
#
# def test_get_cost_promotion_success(api_key_stocks):
#     companies = ["AAPL", "AMZN"]
#     expected_result = [{"stock": "AAPL", "price": 150.0}, {"stock": "AMZN", "price": 3000.0}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=" f"{api_key_stocks}",
#             json={"Time Series (Daily)": {"2023-06-19": {"4. close": "150.0"}}},
#         )
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=" f"{api_key_stocks}",
#             json={"Time Series (Daily)": {"2023-06-19": {"4. close": "3000.0"}}},
#         )
#
#         assert cost_promotion(companies, api_key_stocks) == expected_result
#
#
# def test_get_cost_promotion_partial_failure(api_key_stocks):
#     companies = ["AAPL", "AMZN"]
#     expected_result = [{"stock": "AAPL", "price": 150.0}, {"stock": "AMZN", "price": None}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=" f"{api_key_stocks}",
#             json={"Time Series (Daily)": {"2023-06-19": {"4. close": "150.0"}}},
#         )
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=" f"{api_key_stocks}",
#             status_code=404,
#             text="Not Found",
#         )
#
#         assert cost_promotion(companies, api_key_stocks) == expected_result
#
#
# def test_get_cost_promotion_all_failure(api_key_stocks):
#     companies = ["AAPL", "AMZN"]
#     expected_result = [{"stock": "AAPL", "price": None}, {"stock": "AMZN", "price": None}]
#
#     with requests_mock.Mocker() as mocker:
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=" f"{api_key_stocks}",
#             status_code=500,
#             text="Server Error",
#         )
#         mocker.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=" f"{api_key_stocks}",
#             status_code=500,
#             text="Server Error",
#         )
#
#         assert cost_promotion(companies, api_key_stocks) == expected_result


@patch("requests.get")
def test_cost_promotion(mock_get):
    mock_get.return_value.status.code.return_value = 200
    mock_get.return_value.json.return_value = [{'symbol': 'GOOGL', 'name': 'AfterNext HealthTech Acquisition Corp.',
                                                'price': 177.66, 'exchange': 'New York Stock Exchange',
                                                'exchangeShortName': 'NYSE', 'type': 'stock'},
                                               {'symbol': 'MSFT', 'name': 'AfterNext HealthTech Acquisition Corp.',
                                                'price': 437.11, 'exchange': 'New York Stock Exchange',
                                                'exchangeShortName': 'NYSE', 'type': 'stock'},
                                               {'symbol': 'AAPL', 'name': 'AfterNext HealthTech Acquisition Corp.',
                                                'price': 224.31, 'exchange': 'New York Stock Exchange',
                                                'exchangeShortName': 'NYSE', 'type': 'stock'},
                                               {'symbol': 'TSLA', 'name': 'AfterNext HealthTech Acquisition Corp.',
                                                'price': 239.2, 'exchange': 'New York Stock Exchange',
                                                'exchangeShortName': 'NYSE', 'type': 'stock'},
                                               {'symbol': 'AMZN', 'name': 'AfterNext HealthTech Acquisition Corp.',
                                                'price': 183.13, 'exchange': 'New York Stock Exchange',
                                                'exchangeShortName': 'NYSE', 'type': 'stock'}]
    assert cost_promotion() == [{'Акция': 'GOOGL', 'Цена': 177.66}, {'Акция': 'MSFT', 'Цена': 437.11},
                                {'Акция': 'AAPL', 'Цена': 224.31},
                                {'Акция': 'TSLA', 'Цена': 239.2}, {'Акция': 'AMZN', 'Цена': 183.13}]
