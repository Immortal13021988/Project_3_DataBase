import psycopg2

from config import config


class DBManager:

    def __init__(self, db_name):
        """Инициализатор класса"""
        self.__db_name = db_name

    def __execute_query(self, query):
        """Метод открытия базы данных для использования другими методами"""
        params = config()
        with psycopg2.connect(dbname=self.__db_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании"""
        query = "SELECT * FROM employers"
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию
        """
        query = "SELECT * FROM vacancies"
        return self.__execute_query(query)

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary_from) + AVG(salary_to)  FROM vacancies"
        res = self.__execute_query(query)[0][0]
        return round(res, 2)

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = f"SELECT * FROM vacancies WHERE salary_from > {self.get_avg_salary()}"
        res = self.__execute_query(query)

        return res

    def get_vacancies_with_keyword(self, word_inp):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например python
        """
        query = f"SELECT * FROM vacancies WHERE name LIKE  '%{word_inp}%' "
        res = self.__execute_query(query)
        return res
