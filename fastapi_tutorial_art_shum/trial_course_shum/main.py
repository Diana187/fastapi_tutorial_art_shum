import requests
import json
import time
import functools
from retrying import retry


url = "https://api.hh.ru/vacancies"


@retry(Exception, stop_max_attempt_number=5, wait_fixed=2000)
def fetch_hh_vacancies(url: str, page: int = 0):
    query_params = {
        "text": "django OR fastapi OR flask OR litestar OR aiohttp",
        "per_page": 100,
        "page": page,
    }
    responce = requests.get(url, params=query_params)
    if responce.status_code != 200:
        raise requests.HTTPError(f"Ошибка {responce.status_code}: {responce.text}")
        print("Запрос упал с ошибкой", responce.text)
    print("Успешно полученны вакансии", {page})
    result = responce.json()
    return result


def time_sleep_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(0.2)
        return func(*args, **kwargs)

    return wrapper


@retry(Exception, stop_max_attempt_number=7, wait_fixed=2000)
@time_sleep_decorator
def fetch_all_hh_vacancies(url: str):
    page = 0
    vacvacancies_data = []
    while True:
        if page == 20:
            break
        vacvacancies = fetch_hh_vacancies(url, page)
        if len(vacvacancies["items"]) == 0:
            break
        vacvacancies_data.extend(vacvacancies["items"])
        page += 1

    with open("vacvacancies.json", "w") as file:
        file.write(json.dumps(vacvacancies_data, ensure_ascii=False))


def main():
    fetch_all_hh_vacancies(url)


if __name__ == "__main__":
    main()
