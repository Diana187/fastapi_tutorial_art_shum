import requests
import json
import time
import functools
from dataclasses import dataclass, asdict
from typing import Optional, List
from retrying import retry


url = "https://api.hh.ru/vacancies"


@dataclass
class SalaryData:
    frm: Optional[int]
    to: Optional[int]
    currency: Optional[str]
    gross: Optional[bool]

    @classmethod
    def from_api(cls, salary: Optional[dict]) -> Optional["SalaryData"]:
        if salary is None:
            return None
        return cls(
            frm=salary.get("from"),
            to=salary.get("to"),
            currency=salary.get("currency"),
            gross=salary.get("gross"),
        )


@dataclass(frozen=True)
class VacancyData:
    salary: Optional[SalaryData]
    name: str
    alternate_url: str

    @classmethod
    def from_api(cls, item: dict) -> "VacancyData":
        return cls(
            salary=SalaryData.from_api(item.get("salary")),
            name=item.get("name", ""),
            alternate_url=item.get("alternate_url", ""),
        )


def time_sleep_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(0.2)
        return func(*args, **kwargs)

    return wrapper


@time_sleep_decorator
@retry(stop_max_attempt_number=5, wait_fixed=2000)
def fetch_hh_vacancies(url: str, page: int = 0) -> dict:
    query_params = {
        "text": "django OR fastapi OR flask OR litestar OR aiohttp",
        "per_page": 100,
        "page": page,
    }
    response = requests.get(url, params=query_params, timeout=10)
    if response.status_code != 200:
        raise requests.HTTPError(f"Ошибка {response.status_code}: {response.text}")
    print(f"Успешно получены вакансии со страницы {page}")
    result = response.json()
    return result


@time_sleep_decorator
def fetch_all_hh_vacancies(url: str) -> List[VacancyData]:
    page = 0
    vacancies_data: List[VacancyData] = []
    while True:
        if page == 20:
            break

        data = fetch_hh_vacancies(url, page)
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            vacancies_data.append(VacancyData.from_api(item))

        page += 1

    with open("vacvacancies.json", "w", encoding="utf-8") as file:
        json.dump(
            [asdict(v) for v in vacancies_data], file, ensure_ascii=False, indent=2
        )
    return vacancies_data


def main():
    fetch_all_hh_vacancies(url)


if __name__ == "__main__":
    main()
