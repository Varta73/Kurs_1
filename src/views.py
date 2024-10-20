import datetime
import json
import logging
import os

from src.utils import cost_promotion, currency_rates, filter_cards, get_greeting, read_excel, top_transaction


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


def main(date: str) -> dict:
    """Функция сортирует транзакции за период и выводит словарь:
    Приветствие, транзакции, топ-5 операций, курс валют, стоимость акций"""
    logger.info("Начали обработку информации для страницы Главная")
    date_obj = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    start_date = date_obj.replace(day=1, hour=0, minute=0, second=1)

    read_file = read_excel("../data/operations.xlsx")

    new_list = []
    for i in read_file:
        for a, d in i.items():
            if a == "Дата операции":
                d = datetime.datetime.strptime(d, "%d.%m.%Y %H:%M:%S")
                if start_date <= d <= date_obj:
                    new_list.append(i)
    logger.info(f"Транзакции в списке отфильтрованы по датам от {start_date} до {date_obj}")

    call_currency_rates = currency_rates()
    price_rub = currency_rates()[0]["Курс"]

    call_cost_promotion = cost_promotion()
    for key in call_cost_promotion:
        key["Стоимость"] = key.get("Цена") * price_rub

    answer_dict = {
        "Приветствие": get_greeting(),
        "Транзакции": filter_cards(new_list),
        "Топ-5 операций:": top_transaction(new_list),
        "Курс валют:": call_currency_rates,
        "Стоимость акций:": call_cost_promotion,
    }
    logger.info("Окончили обработку информации для страницы Главная")
    return json.dumps(answer_dict, ensure_ascii=False, indent=4)


print(main("20-05-2020 22:20:32"))
