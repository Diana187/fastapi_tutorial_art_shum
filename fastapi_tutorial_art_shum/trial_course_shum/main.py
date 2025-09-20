import requests
import json


url = "https://api.hh.ru/vacancies"


def fetch_hh_vacancies(url: str, page: int = 0):
    query_params = {
        "text": "django OR fastapi OR flask OR litestar OR aiohttp",
        "per_page": 100,
        "page": page,
    }
    responce = requests.get(url, params=query_params)
    if responce.status_code != 200:
        print("Запрос упал с ошибкой", responce.text)
    print("Успешно полученны вакансии", {page})
    result = responce.json()
    return result


def fetch_all_hh_vacancies(url: str):
    page = 0
    vacvacancies_data = []
    while True:
        if page == 20:
            break
        vacvacancies = fetch_hh_vacancies(url, page)
        vacvacancies_data
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
