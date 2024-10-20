import json
import logging
import os
import re
from typing import Dict, List

from src.utils import read_excel

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


def simple_search(result: List[Dict], search: str) -> str:
    """Функция принимает транзакции в формате списка словарей и строку — запрос для поиска"""
    try:
        result_search = []
        for transaction in result:
            category = str(transaction.get("Категория", ""))
            description = str(transaction.get("Описание", ""))
            if search.lower() in description.lower() or search.lower() in category.lower():
                result_search.append(transaction)
        logger.info(f"Выполнен поиск по запросу {search}")
        return json.dumps(result_search, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Возникла ошибка {e}")
        logger.error(f"Возникла ошибка {e}")
        return ""


# print(simple_search(read_excel(xlsx_path1), "Rumyanyj Khleb"))


def search_by_phone_numbers(result: List[Dict]) -> str:
    """Функция возвращает транзакции в описании которых есть мобильный номер"""
    try:
        phone_numbers = re.compile(r"\+\d{1,4}")
        result_search = []
        for transaction in result:
            description = transaction.get("Описание", "")
            if phone_numbers.search(description):
                result_search.append(transaction)
        logger.info("Выполнен поиск по транзакциям с номером телефона")
        return json.dumps(result_search, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Возникла ошибка {e}")
        logger.error(f"Возникла ошибка {e}")
        return ""


# print(search_by_phone_numbers(read_excel(xlsx_path1)))
