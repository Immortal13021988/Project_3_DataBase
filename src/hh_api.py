import requests


class HHApi:
    """Класс взаимодействия с hh.ru"""

    @staticmethod
    def get_employers() -> list[dict]:
        """Получение компаний с hh.ru"""
        try:
            params = {"sort_by": "by_vacancies_open", "per_page": 10}
            response = requests.get("https://api.hh.ru/employers", params=params)
            response.raise_for_status()
            data = response.json()["items"]
            employers = []
            for employer in data:
                employers.append(
                    {
                        "id": employer["id"],
                        "name": employer["name"],
                        "open_vacancies": employer["open_vacancies"],
                    }
                )
            return employers
        except requests.RequestException as e:  # pragma no cover
            print(f"Ошибка при подключении к API: {e}")
            return []

    @staticmethod
    def get_vacancies(employer_id) -> list[dict]:
        """Получение вакансий компаний с hh.ru"""
        try:
            params = {"employer_id": employer_id, "per_page": 50}
            response = requests.get("https://api.hh.ru/vacancies", params=params)
            response.raise_for_status()
            data = response.json()["items"]
            # print(data)
            vacancies = []
            for vacancy in data:
                if vacancy["salary"]:
                    salary_from = (
                        vacancy["salary"]["from"]
                        if vacancy["salary"]["from"]
                        else vacancy["salary"]["to"]
                    )
                    salary_to = (
                        vacancy["salary"]["to"]
                        if vacancy["salary"]["to"]
                        else vacancy["salary"]["from"]
                    )
                else:
                    salary_from = 0
                    salary_to = 0
                vacancies.append(
                    {
                        "id": vacancy["id"],
                        "name": vacancy["name"],
                        "employer": vacancy["employer"]["name"],
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "url": vacancy["alternate_url"],
                    }
                )
            return vacancies
        except requests.RequestException as e:  # pragma no cover
            print(f"Ошибка при подключении к API: {e}")
            return []


if __name__ == "__main__":
    hh = HHApi()
    print(hh.get_vacancies(2748))
