import os
from unittest.mock import Mock, patch

import pytest
from freezegun import freeze_time

from src.utils import cost_promotion, currency_rates, filter_cards, get_greeting, read_excel, top_transaction

current_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(current_dir, "../data/operations.xlsx")
xlsx_path1 = os.path.abspath(xlsx_path)

current_dir = os.path.dirname(os.path.abspath(__file__))
user_path = os.path.join(current_dir, "../data/user_setings.json")
user_path1 = os.path.abspath(user_path)

test_list = read_excel(xlsx_path)
nul_list = []


@freeze_time("2023-01-01 10:00:00")
def test_get_greeting_1():
    assert get_greeting() == "Доброе утро"


@freeze_time("2023-01-01 15:00:00")
def test_get_greeting_2():
    assert get_greeting() == "Добрый день"


@freeze_time("2023-01-01 19:00:00")
def test_get_greeting_3():
    assert get_greeting() == "Добрый вечер"


@freeze_time("2023-01-01 23:00:00")
def test_get_greeting_4():
    assert get_greeting() == "Доброй ночи"


def test_filter_cards():
    """Тестирование функции, создающей информацию по каждой карте"""
    assert filter_cards(test_list) == [
        {"Всего потрачено": 2504514.54, "Кэшбэк": 25045.15, "Номер карты": "7197"},
        {"Всего потрачено": 18216.84, "Кэшбэк": 182.17, "Номер карты": "5091"},
        {"Всего потрачено": 2103029.17, "Кэшбэк": 21030.29, "Номер карты": "4556"},
        {"Всего потрачено": 46207.08, "Кэшбэк": 462.07, "Номер карты": "1112"},
        {"Всего потрачено": 84000.0, "Кэшбэк": 840.0, "Номер карты": "5507"},
        {"Всего потрачено": 69200.0, "Кэшбэк": 692.0, "Номер карты": "6002"},
        {"Всего потрачено": 470854.8, "Кэшбэк": 4708.55, "Номер карты": "5441"},
    ]


@pytest.mark.parametrize(
    "test, result",
    [
        (
                [
                    [
                        {
                            "Дата операции": "31.12.2021 16:44:00",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "*7197",
                            "Статус": "OK",
                            "Сумма операции": -160.89,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -160.89,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Супермаркеты",
                            "MCC": 5411.0,
                            "Описание": "Колхоз",
                            "Бонусы (включая кэшбэк)": 3,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 160.89,
                        },
                        {
                            "Дата операции": "31.12.2021 16:42:04",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "*7197",
                            "Статус": "OK",
                            "Сумма операции": -64.0,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -64.0,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Супермаркеты",
                            "MCC": 5411.0,
                            "Описание": "Колхоз",
                            "Бонусы (включая кэшбэк)": 1,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 64.0,
                        },
                        {
                            "Дата операции": "31.12.2021 16:39:04",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "*7197",
                            "Статус": "OK",
                            "Сумма операции": -118.12,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -118.12,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Супермаркеты",
                            "MCC": 5411.0,
                            "Описание": "Магнит",
                            "Бонусы (включая кэшбэк)": 2,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 118.12,
                        },
                        {
                            "Дата операции": "31.12.2021 15:44:39",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "*7197",
                            "Статус": "OK",
                            "Сумма операции": -78.05,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -78.05,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Супермаркеты",
                            "MCC": 5411.0,
                            "Описание": "Колхоз",
                            "Бонусы (включая кэшбэк)": 1,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 78.05,
                        },
                        {
                            "Дата операции": "31.12.2021 01:23:42",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "*5091",
                            "Статус": "OK",
                            "Сумма операции": -564.0,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -564.0,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Различные товары",
                            "MCC": 5399.0,
                            "Описание": "Ozon.ru",
                            "Бонусы (включая кэшбэк)": 5,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 564.0,
                        },
                        {
                            "Дата операции": "31.12.2021 00:12:53",
                            "Дата платежа": "31.12.2021",
                            "Номер карты": "Отсутствует",
                            "Статус": "OK",
                            "Сумма операции": -800.0,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -800.0,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "Отсутствует",
                            "Категория": "Переводы",
                            "MCC": "Отсутствует",
                            "Описание": "Константин Л.",
                            "Бонусы (включая кэшбэк)": 0,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 800.0,
                        },
                    ],
                    [
                        {
                            "Дата операции": "31.12.2021",
                            "Сумма": 564.0,
                            "Категория": "Различные товары",
                            "Описание": "Ozon.ru",
                        },
                        {
                            "Дата операции": "31.12.2021",
                            "Сумма": 160.89,
                            "Категория": "Супермаркеты",
                            "Описание": "Колхоз",
                        },
                        {
                            "Дата операции": "31.12.2021",
                            "Сумма": 118.12,
                            "Категория": "Супермаркеты",
                            "Описание": "Магнит",
                        },
                        {"Дата операции": "31.12.2021", "Сумма": 78.05, "Категория": "Супермаркеты",
                         "Описание": "Колхоз"},
                        {"Дата операции": "31.12.2021", "Сумма": 64.0, "Категория": "Супермаркеты",
                         "Описание": "Колхоз"},
                    ],
                ]
        )
    ],
)
def test_top_transaction(test, result):
    assert top_transaction(test) == result


@patch("requests.get")
def test_currency_rates(mock_get):
    """Тестирование функции вывода курса валют"""
    mock_response_usd = Mock()
    mock_response_usd.json.return_value = {"conversion_rates": {"RUB": 88.34}}
    mock_response_eur = Mock()
    mock_response_eur.json.return_value = {"conversion_rates": {"RUB": 97.8}}
    mock_get.side_effect = [mock_response_usd, mock_response_eur]

    result = currency_rates()
    expected = [{"Валюта": "USD", "Курс": 88.34}, {"Валюта": "EUR", "Курс": 97.8}]
    assert result == expected


@patch("requests.get")
def test_cost_promotion(mock_get):
    mock_get.return_value.status.code.return_value = 200
    mock_get.return_value.json.return_value = [
        {
            "symbol": "GOOGL",
            "name": "AfterNext HealthTech Acquisition Corp.",
            "price": 177.66,
            "exchange": "New York Stock Exchange",
            "exchangeShortName": "NYSE",
            "type": "stock",
        },
        {
            "symbol": "MSFT",
            "name": "AfterNext HealthTech Acquisition Corp.",
            "price": 437.11,
            "exchange": "New York Stock Exchange",
            "exchangeShortName": "NYSE",
            "type": "stock",
        },
        {
            "symbol": "AAPL",
            "name": "AfterNext HealthTech Acquisition Corp.",
            "price": 224.31,
            "exchange": "New York Stock Exchange",
            "exchangeShortName": "NYSE",
            "type": "stock",
        },
        {
            "symbol": "TSLA",
            "name": "AfterNext HealthTech Acquisition Corp.",
            "price": 239.2,
            "exchange": "New York Stock Exchange",
            "exchangeShortName": "NYSE",
            "type": "stock",
        },
        {
            "symbol": "AMZN",
            "name": "AfterNext HealthTech Acquisition Corp.",
            "price": 183.13,
            "exchange": "New York Stock Exchange",
            "exchangeShortName": "NYSE",
            "type": "stock",
        },
    ]
    assert cost_promotion() == [
        {"Акция": "GOOGL", "Цена": 177.66},
        {"Акция": "MSFT", "Цена": 437.11},
        {"Акция": "AAPL", "Цена": 224.31},
        {"Акция": "TSLA", "Цена": 239.2},
        {"Акция": "AMZN", "Цена": 183.13},
    ]
