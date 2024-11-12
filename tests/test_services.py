import json
import os
import pytest
import unittest

from src.utils import read_excel
from src.services import simple_search, search_by_phone_numbers

current_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(current_dir, "../data/operations.xlsx")
xlsx_path1 = os.path.abspath(xlsx_path)

test_list = read_excel(xlsx_path)
null_list = []


def test_simple_search():
    """Тестирование функции простой поиск в обычных условиях"""
    assert simple_search(test_list, "Ozon.ru") == json.dumps([
        {
            "Дата операции": "31.12.2021 01:23:42",
            "Дата платежа": "31.12.2021",
            "Статус": "OK",
            "Сумма платежа": -564.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*5091"
        },
        {
            "Дата операции": "20.12.2021 19:42:13",
            "Дата платежа": "20.12.2021",
            "Статус": "OK",
            "Сумма платежа": 421.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата операции": "14.12.2021 00:17:19",
            "Дата платежа": "14.12.2021",
            "Статус": "OK",
            "Сумма платежа": -421.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата операции": "21.10.2021 12:30:42",
            "Дата платежа": "21.10.2021",
            "Статус": "OK",
            "Сумма платежа": -119.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата операции": "02.10.2020 22:08:55",
            "Дата платежа": "04.10.2020",
            "Статус": "OK",
            "Сумма платежа": -750.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        }
    ], indent=4,
        ensure_ascii=False, )


def test_simple_search_1():
    """Тестирование функции простой поиск, с пустыми атрибутами """
    assert simple_search(null_list, "") == "[]"


class TestSqrt(unittest.TestCase):
    def test_simple_search_2(self):
        with self.assertRaises(Exception):
            assert simple_search(test_list, 1) == AssertionError

    def test_search_by_phone_numbers_1(self):
        transactions = [
            {"Сумма операции": -1000},
            {"Сумма операции": -1500},
            {"Сумма операции": -500},
            {"Сумма операции": -2000},
            {"Сумма операции": -300}
        ]
        with self.assertRaises(Exception):
            assert search_by_phone_numbers(transactions) == Exception


def test_search_by_phone_numbers():
    transactions = [
        {"Описание": "Я МТС +7 921 11-22-33", "Сумма операции": -1000},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Сумма операции": -1500},
        {"Описание": "Магазин", "Сумма операции": -500},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Сумма операции": -2000},
        {"Описание": "Оплата по карте", "Сумма операции": -300}
    ]

    expected_output = json.dumps([
        {"Описание": "Я МТС +7 921 11-22-33", "Сумма операции": -1000},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Сумма операции": -1500},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Сумма операции": -2000}
    ], ensure_ascii=False, indent=4)

    result = search_by_phone_numbers(transactions)
    assert result == expected_output
