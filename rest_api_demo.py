import os
import sys
import json
import requests
from dotenv import load_dotenv


def load_api_key() -> str:
    """Загружает и проверяет наличие API ключа."""
    load_dotenv()
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        print("❌ Ошибка: Ключ OMDB_API_KEY не найден в файле .env")
        sys.exit(1)
    return api_key


def search_movie(title: str, api_key: str) -> dict:
    """Ищет информацию о фильме через OMDb API."""
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"t": title, "apikey": api_key},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("❌ Ошибка: Истёк timeout при подключении к OMDb API")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения к OMDb API: {e}")
        sys.exit(1)

    try:
        json_data = response.json()
    except json.JSONDecodeError:
        print("❌ Ошибка: Некорректный ответ от API (не JSON)")
        sys.exit(1)

    if json_data.get("Response") == "False":
        print(f"❌ Ошибка: {json_data.get('Error', 'Неизвестная ошибка')}")
        sys.exit(1)

    return json_data


def display_movie_info(movie_data: dict):
    """Выводит информацию о фильме в красивом формате."""
    fields_to_display = {
        "Title": "Название",
        "Year": "Год",
        "Genre": "Жанр",
        "Director": "Режиссёр",
        "Actors": "Актёры",
        "imdbRating": "Рейтинг IMDb"
    }

    print("\n📽️  Информация о фильме:")
    print("-" * 50)
    for field, label in fields_to_display.items():
        value = movie_data.get(field, "N/A")
        print(f"{label}: {value}")
    print("-" * 50)


def main():
    """Главная функция приложения."""
    title = input("🔍 Введите название фильма для поиска: ").strip()
    
    if not title:
        print("❌ Ошибка: Название фильма не может быть пустым")
        sys.exit(1)

    api_key = load_api_key()
    movie_data = search_movie(title, api_key)

    print("\n📄 Полный ответ API:")
    print(json.dumps(movie_data, ensure_ascii=False, indent=2))

    display_movie_info(movie_data)


if __name__ == "__main__":
    main()
