import functools
import json
import logging
import os
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from src.utils import read_excel_df

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


def report_to_file(func: Callable, filename: str = "search.json") -> Callable:
    """Записывает в файл результат, который возвращает функция, формирующая отчет."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        with open("search.json", "w", encoding="utf-8") as file:
            file.write(str(result))
        logger.info(f"Записан результат работы функции {func}в файл {filename}")
        return result

    return wrapper


@report_to_file
def spending_by_category(df: pd.DataFrame, category: str, date: Optional[str] = None) -> Any:
    """Функция возвращает траты по заданной категории за последние три месяца
    (от переданной даты; если дата не передана берет текущую)"""
    logger.info(f"Начали сортировку транзакций по категории: {category} за последние 3 месяца, начиная с {date}")
    last_date = pd.to_datetime(date, dayfirst=True) if date else datetime.today()
    start_date = last_date - relativedelta(months=3)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    filtered_transactions_by_date = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= last_date)]
    filtered_transactions_by_category = pd.DataFrame(
        filtered_transactions_by_date[filtered_transactions_by_date["Категория"] == category]
    )
    logger.info("Окончили сортировку транзакциям по категориям за последние 3 месяца")
    return json.dumps(
        filtered_transactions_by_category.to_dict(orient="records"), ensure_ascii=False, default=str, indent=4
    )


print(spending_by_category(read_excel_df(xlsx_path1), "Фастфуд", "29.12.2021 16:43:00"))
