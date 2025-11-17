import psycopg2

from config import config
from src.hh_api import HHApi


def create_db(db_name):
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name):
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE employers ("
                "id int PRIMARY KEY, "
                "name varchar(250) NOT NULL, "
                "open_vacancies int NOT NULL )"
            )
            cur.execute(
                "CREATE TABLE vacancies ("
                "id int PRIMARY KEY,"
                "name varchar(250) NOT NULL, "
                "employer varchar(250) NOT NULL, "
                "salary_from int,  "
                "salary_to int,  "
                "url varchar(250) )"
            )
    conn.close()


def insert_in_tables(db_name):
    hh = HHApi()
    employers = hh.get_employers()

    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for emp in employers:
                cur.execute(
                    "INSERT INTO employers VALUES (%s, %s, %s)",
                    (emp["id"], emp["name"], emp["open_vacancies"]),
                )
                vacancies = hh.get_vacancies(emp["id"])
                for vac in vacancies:
                    cur.execute(
                        "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            vac["id"],
                            vac["name"],
                            vac["employer"],
                            vac["salary_from"],
                            vac["salary_to"],
                            vac["url"],
                        ),
                    )

    conn.close()
