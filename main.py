"""Главный модуль программы для загрузки данных из JSON-файла"""

from db_creator import DBCreator
from db_manager import DBManager
from config import DB_CONFIG
from load_data_from_json import load_data_from_json_file
import json


def display_all_results(db_manager: DBManager) -> None:
    """Отображение всех результатов из БД"""
    print("\n" + "=" * 80)
    print("1. КОМПАНИИ И КОЛИЧЕСТВО ВАКАНСИЙ:")
    print("=" * 80)
    companies_count = db_manager.get_companies_and_vacancies_count()
    for company_name, vacancies_count in companies_count:
        print(f"  • {company_name}: {vacancies_count} вакансий")

    print("\n" + "=" * 80)
    print("2. ВСЕ ВАКАНСИИ (первые 10):")
    print("=" * 80)
    all_vacancies = db_manager.get_all_vacancies()
    for company_name, vacancy_name, salary, url in all_vacancies[:10]:
        print(f"  • {company_name} — {vacancy_name}")
        print(f"    Зарплата: {salary}")
        print(f"    Ссылка: {url}\n")

    print("\n" + "=" * 80)
    print("3. СРЕДНЯЯ ЗАРПЛАТА ПО ВСЕМ ВАКАНСИЯМ:")
    print("=" * 80)
    avg_salary = db_manager.get_avg_salary()
    print(f"  • Средняя зарплата: {avg_salary:.2f} руб.")

    print("\n" + "=" * 80)
    print("4. ВАКАНСИИ С ЗАРПЛАТОЙ ВЫШЕ СРЕДНЕЙ:")
    print("=" * 80)
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for company_name, vacancy_name, salary, url in high_salary_vacancies:
        print(f"  • {company_name} — {vacancy_name}")
        print(f"    Зарплата: {salary}")
        print(f"    Ссылка: {url}\n")

    print("\n" + "=" * 80)
    print("5. ПОИСК ВАКАНСИЙ ПО КЛЮЧЕВОМУ СЛОВУ 'Python':")
    print("=" * 80)
    keyword_vacancies = db_manager.get_vacancies_with_keyword('Python')
    for company_name, vacancy_name, salary, url in keyword_vacancies:
        print(f"  • {company_name} — {vacancy_name}")
        print(f"    Зарплата: {salary}")
        print(f"    Ссылка: {url}\n")


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""
    print("Добро пожаловать в парсер вакансий hh.ru!")
    print("\nИспользуются данные из JSON-файла (реальные вакансии).")

    # Инициализация базы данных
    print("\n1. Инициализация базы данных...")
    db_creator = DBCreator(DB_CONFIG)
    db_creator.init_database(DB_CONFIG['database'])
    print(f"   База данных '{DB_CONFIG['database']}' успешно создана")

    # Загрузка данных из JSON-файла
    print("\n2. Загрузка данных из JSON-файла...")
    load_data_from_json_file('hh_vacancies_sample.json')

    # Демонстрация результатов
    print("\n3. ПОЛНЫЙ ОТЧЕТ ПО ДАННЫМ:")
    db_manager = DBManager(DB_CONFIG)
    display_all_results(db_manager)

    print("\nПрограмма завершила работу!")


if __name__ == "__main__":
    user_interaction()
