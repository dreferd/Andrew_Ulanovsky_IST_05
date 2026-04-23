import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

title = input("Введите фильм для поиска: ")
api_key = os.getenv("OMDB_API_KEY")

if not api_key:
    raise ValueError("Ключ OMDB_API_KEY не найден в .env")

try:
    response = requests.get(
        "https://www.omdbapi.com/",
        params={
            "t": title,
            "apikey": api_key
        },
        timeout=10
    )
    response.raise_for_status()
    json_data = response.json()
    if json_data.get("Response") == "False":
        print(f"Ошибка: {json_data.get('Error')}")

        exit()

    print(json.dumps(json_data, ensure_ascii=False, indent=2))

    movie_title = json_data.get("Title")
    year = json_data.get("Year")
    genre = json_data.get("Genre")
    director = json_data.get("Director")
    actors = json_data.get("Actors")
    imdb_rating = json_data.get("imdbRating")

    print(f"Название: {movie_title}")
    print(f"Год: {year}")
    print(f"Жанр: {genre}")
    print(f"Режиссёр: {director}")
    print(f"Актёры: {actors}")
    print(f"Рейтинг IMDb: {imdb_rating}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка подключения к OMDb API: {e}")