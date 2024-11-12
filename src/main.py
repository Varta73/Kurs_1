import os

from src.services import search_by_phone_numbers, simple_search
from src.utils import read_excel
from src.views import main

current_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(current_dir, "../data/operations.xlsx")
xlsx_path1 = os.path.abspath(xlsx_path)


def main_function() -> None:
    """Результат всех реализованных в проекте функциональностей"""

    result = main(date=input("Введите дату: "))
    print(result)
    while True:
        print("Нужен поиск по категории или описанию?")
        user_input = input("Введите да/нет: ").lower()
        if user_input in ("да", "нет"):
            break
        else:
            print("Введён некорректный ответ. Повторите ввод ответа.")
    if user_input == "да":
        search = simple_search(read_excel(xlsx_path1), search=input(str("Что ищем? ")))
        print(search)

    while True:
        print("Нужен поиск по телефонным номерам?")
        currency_selection = input("Введите да/нет: ").lower()
        if currency_selection in ("да", "нет"):
            break
        else:
            print("Введён некорректный ответ. Повторите ввод ответа.")
    if currency_selection == "да":
        phone_numbers = search_by_phone_numbers(read_excel(xlsx_path1))
        print(phone_numbers)
    elif currency_selection == "нет":
        print("")


if __name__ == "__main__":
    main_function()
