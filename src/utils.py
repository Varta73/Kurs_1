import datetime as dt
import json
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
path_1 = os.path.join(current_dir, "../logs/format.log")
path_2 = os.path.abspath(path_1)

# Логгер, который записывает логи в файл.
logger = logging.getLogger("format")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(path_2, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(current_dir, "../data/operations.xlsx")
xlsx_path1 = os.path.abspath(xlsx_path)

load_dotenv()
api_key = os.getenv("API_KEY")
apikey = os.getenv("apikey")


def get_greeting() -> str:
    """Функция - приветствие"""
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# print(get_greeting())


def read_excel(xlsx_path1: str) -> list[dict]:
    """Функция читает xlsx-файл и возвращает список словарей"""
    df = pd.read_excel(xlsx_path1)
    result = df.apply(
        lambda row: {
            "Дата операции": row["Дата операции"],
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result


# print(read_excel(xlsx_path1))


def read_excel_df(xlsx_path1: str) -> Any:
    """Функция читает xlsx-файл и возвращает DataFrame"""
    df = pd.read_excel(xlsx_path1)
    return df


# print(read_excel_df(xlsx_path1))


def filter_cards(result: list) -> str | list[dict[str | Any, str | Any]]:
    """Функция выводит информацию по каждой карте"""
    logger.info("Начата сортировка информации по картам")
    cards: dict[Any, float] = {}
    inf_cards = []
    for i in result:
        if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
            continue
        elif i["Сумма платежа"] == "nan":
            continue
        else:
            if i["Номер карты"][1:] in cards:
                cards[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
            else:
                cards[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
    for k, v in cards.items():
        inf_cards.append({"Номер карты": k, "Всего потрачено": round(v, 2), "Кэшбэк": round(v / 100, 2)})
        logger.info("Сортировка информации по картам закончена")
    return inf_cards


# print(filter_cards(read_excel(xlsx_path1)))


def top_transaction(transaction: list) -> list:
    """Функция выводит топ-5 транзакций"""
    logger.info("Начата обработка ТОП-5 транзакций")
    top_transaction = []
    for key in transaction:
        filters = {
            "Дата операции": key["Дата операции"][:10],
            "Сумма": abs(key["Сумма платежа"]),
            "Категория": key["Категория"],
            "Описание": key["Описание"],
        }
        for i, value in key.items():
            if value is None:
                filters[i] = "Нет информации"
        top_transaction.append(filters)
    logger.info("Обработка информации ТОП-5 транзакций закончена")
    return sorted(top_transaction, key=lambda x: x["Сумма"], reverse=True)[1:6]


# print(top_transaction(read_excel(xlsx_path1)))


def currency_rates() -> list:
    """Функция выводит курс валют для необходимой валюты из пользовательских настроек"""
    logger.info("Получаем информацию из файла о необходимой валюте")
    with open("../data/user_setings.json", "r") as file:
        reading = json.load(file)["user_currencies"]

    currency_rate = []
    logger.info("Производим запрос по API по необходимым валютам")
    for i in reading:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={i}&amount=1"

        headers = {"apikey": api_key}

        response = requests.request("GET", url, headers=headers)
        result = round(response.json()["result"], 2)
        currency_rate.append(dict(Валюта=i, Курс=result))
    logger.info("Сбор информации по курсам валют закончен")
    return currency_rate


print(currency_rates())


def cost_promotion() -> list:
    """Функция получает по API цену акций и выводит их стоимость"""
    logger.info("Получаем информацию из пользовательских настроек о необходимых акциях")
    with open("../data/user_setings.json", "r") as file:
        reading = json.load(file)["user_stocks"]

        logger.info("Производим запрос по API")
        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={apikey}"
        response = requests.get(url)

        data = response.json()
        stock_prices = []
        logger.info("Фильтруем список согласно необходимых данных")
        for i in data:
            for element in reading:
                if i["symbol"] == element:
                    stock_prices.append(dict(Акция=element, Цена=i["price"]))
        logger.info("Подсчет стоимости акций закончен")
        return stock_prices


# print(cost_promotion())
