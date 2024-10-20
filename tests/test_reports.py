import pytest
import pandas as pd
from src.reports import spending_by_category


@pytest.fixture
def sample_data():
    # Пример тестовых данных
    data = {
        "Дата операции": [
            "01.01.2022 10:00:00",
            "01.01.2022 10:30:00",
            "15.01.2022 15:45:00",
            "01.02.2023 09:10:00",
            "05.02.2023 15:20:00",
        ],
        "Категория": ["Фастфуд", "Фастфуд", "Каршеринг", "Фастфуд", "Каршеринг"],
        "Сумма": [50, 100, 200, 150, 250],
    }
    df = pd.DataFrame(data)
    return df


def test_spending_by_category_with_date(sample_data):
    # Тестирование функции с указанной датой и категорией "Фастфуд"
    result = spending_by_category(sample_data, "Фастфуд", "01.01.2022 17:50:30")
    assert result.count("Фастфуд") == 2


def test_spending_by_category_no_date(sample_data):
    # Тестирование функции с указанной категорией
    result = spending_by_category(sample_data, "Фастфуд")
    assert result.count("Фастфуд") == 0


def test_spending_by_category_future_date(sample_data):
    # Тестирование функции с будущей датой
    result = spending_by_category(sample_data, "01.01.2023 00:00:00")
    assert result.count("01.01.2023 00:00:00") == 0


def test_spending_by_category_no_transactions(sample_data):
    # Тестирование функции с категорией, для которой нет транзакций
    result = spending_by_category(sample_data, "Продукты")
    assert result.count("Продукты") == 0


# if __name__ == "__main__":
#     pytest.main()