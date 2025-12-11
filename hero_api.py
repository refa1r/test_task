import pytest
import requests


API_URL = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"


@pytest.fixture(scope="session")
def heroes_data():
    """Получает данные с API один раз за выполнение всех тестов."""
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def filter_heroes(data, gender=None, has_job=None):
    """Фильтрует список героев."""
    if gender is None or has_job is None:
        return []

    return [
        hero for hero in data
        if hero["appearance"]["gender"].lower() == gender.lower()
        and ((hero["work"]["occupation"] != "-") if has_job else (hero["work"]["occupation"] == "-"))
    ]


def get_tallest_hero(data):
    """Возвращает самого высокого героя."""
    return max(
        data,
        key=lambda h: float(h["appearance"]["height"][1].split()[0])
    )


def test_api_available():
    """Проверяем, что API доступен."""
    response = requests.get(API_URL)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "gender, has_job, expect_result",
    [
        ("male", True, True),
        ("female", False, True),
        ("unknown", True, False),
        (None, True, False),
        ("", False, False),
    ]
)
def test_hero_selection(heroes_data, gender, has_job, expect_result):
    filtered = filter_heroes(heroes_data, gender, has_job)

    if not expect_result:
        assert filtered == []
    else:
        tallest = get_tallest_hero(filtered)
        assert "name" in tallest
        assert "appearance" in tallest
