import pytest

import requests

def api_data():
    """"Получает данные с API"""
    response = requests.get(
        "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    )
    response.raise_for_status()
    return response.json()


def heroes(gender, has_job):
    """Возвращает героя с максимальным ростом"""
    heroes_info = api_data()
    if not gender or has_job is None:
        return None
    filtered_heroes = [
        hero
        for hero in heroes_info
        if hero["appearance"]["gender"].lower() == gender.lower()
        and (
            hero["work"]["occupation"] != "-"
            if has_job
            else hero["work"]["occupation"] == "-"
        )
    ]

    if not filtered_heroes:
        return None

    tallest_hero = max(
        filtered_heroes,
        key=lambda hero: int(float(hero["appearance"]["height"][1].split()[0])),
    )

    return {
        "name": tallest_hero["name"],
        "height": tallest_hero["appearance"]["height"][1],
    }


def test_api_status():
    """"Проверяет, что статус-код 200 и API доступен"""
    response = requests.get(
        "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    )
    assert response.status_code == 200, "API не вернул 200 статус-код"


@pytest.mark.parametrize(
    "gender, has_job, expected",
    [
        ("random", True, None),
        ("male", True, dict),
        ("female", False, dict),
        ("male", True, dict),
        ("male", False, dict),
        ("male", None, None),
        (None, False, None),
        ("", True, None),
        ("MALE", True, dict),
    ],
)
def test_heroes(gender, has_job, expected):
    """"Тестирует функцию heroes"""
    data = heroes(gender, has_job)
    if expected is None:
        assert data is None, f"Ожидалось None, но получен {data}"
    else:
        assert isinstance(data, dict), f"Ожидался словарь, но получен {type(data)}"
        assert "name" in data, "Отсутствует ключ 'name'"
        assert "height" in data, "Отсутствует ключ 'height'"