from src.db_manager import DBManager
from src.utils import create_db, create_tables, insert_in_tables


def main():
    print("Добро пожаловать! ")
    db_name = "hh_ru"
    create_db(db_name)
    create_tables(db_name)
    insert_in_tables(db_name)
    while True:
        print("1. Получение списка работодателей на hh.ru (топ-10 по кол-ву открытых вакансий")
        print("2. Получение списка вакансий из топ-10 компаний")
        print("3. Получение средней зарплаты по вакансиям.")
        print("4. Получение список всех вакансий, у которых зарплата выше средней зарплаты по вакансиям.")
        print("5. Получение список всех вакансий, по ключевому поиску.")
        num_op = input("Введите номер опции: ").strip()
        print("-" * 50)
        if num_op == '1':
            try:
                employer = DBManager(db_name)
                for emp in employer.get_companies_and_vacancies_count():
                    print(f"Название компании: {emp[1]}")
                    print(f"id компании: {emp[0]}")
                    print(f"Кол-во открытых вакансий компании: {emp[2]}")
                    print("-" * 50)

            except Exception as e:
                print(f"Произошла ошибка: {e}")
        elif num_op == '2':
            try:
                employer = DBManager(db_name)
                for emp in employer.get_all_vacancies():
                    print(f"Название компании: {emp[2]}")
                    print(f"Вакансия: {emp[1]}")
                    print(f"Зарплата от: {emp[3]}")
                    print(f"Зарплата до: {emp[4]}")
                    print(f"Ссылка: {emp[5]}")
                    print("-" * 50)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
        elif num_op == '3':
            try:
                employer = DBManager(db_name)
                print(f"Средняя заработная плата: {employer.get_avg_salary()}")
                print("-" * 50)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
        elif num_op == '4':
            try:
                employer = DBManager(db_name)
                for emp in employer.get_vacancies_with_higher_salary():
                    print(f"Название компании: {emp[2]}")
                    print(f"Вакансия: {emp[1]}")
                    print(f"Зарплата от: {emp[3]}")
                    print(f"Зарплата до: {emp[4]}")
                    print(f"Ссылка: {emp[5]}")
                    print("-" * 50)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
        elif num_op == '5':
            keyword_in_desc = input("Введите ключевое слово для поиска в названии вакансий: ").strip().lower()
            print("-" * 50)  # для отделения ввода и вывода
            try:
                employer = DBManager(db_name)
                for emp in employer.get_vacancies_with_keyword(keyword_in_desc):
                    print(f"Название компании: {emp[2]}")
                    print(f"Вакансия: {emp[1]}")
                    print(f"Зарплата от: {emp[3]}")
                    print(f"Зарплата до: {emp[4]}")
                    print(f"Ссылка: {emp[5]}")
                    print("-" * 50)
                    if not emp:
                        print("Вакансии с указанным ключевым словом в описании не найдены.")
                        break
                    else:
                        for vac in emp:
                            print(vac)
                        break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
        else:
            print("Некорректный выбор. Попробуйте снова.")
            print("-" * 50)


if __name__ == "__main__":
    main()
    # emp = DBManager("hh_ru")
    # print(emp.get_all_vacancies())
