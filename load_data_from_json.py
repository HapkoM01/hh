"""Модуль для загрузки данных из JSON-файла в базу данных"""

import json
from typing import Dict, Any, List
from db_manager import DBManager
from config import DB_CONFIG


def load_companies_from_json(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлечение данных о компаниях из JSON

    Args:
        json_data: Данные из JSON-файла

    Returns:
        Список уникальных компаний
    """
    companies_dict = {}

    for item in json_data.get('items', []):
        employer = item.get('employer', {})
        company_id = employer.get('id')

        if company_id and company_id not in companies_dict:
            companies_dict[company_id] = {
                'company_id': int(company_id),
                'company_name': employer.get('name', ''),
                'description': '',  # API не возвращает описание в этом файле
                'url': employer.get('alternate_url', ''),
                'vacancies_url': employer.get('alternate_url', '')
            }

    return list(companies_dict.values())


def load_vacancies_from_json(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлечение данных о вакансиях из JSON

    Args:
        json_data: Данные из JSON-файла

    Returns:
        Список вакансий
    """
    vacancies = []

    for item in json_data.get('items', []):
        salary_data = item.get('salary')
        employer = item.get('employer', {})

        # Получаем данные о зарплате
        salary_from = salary_data.get('from') if salary_data else None
        salary_to = salary_data.get('to') if salary_data else None
        currency = salary_data.get('currency') if salary_data else None

        vacancy = {
            'vacancy_id': int(item.get('id')),
            'company_id': int(employer.get('id')) if employer.get('id') else None,
            'vacancy_name': item.get('name', ''),
            'salary_from': salary_from,
            'salary_to': salary_to,
            'currency': currency,
            'url': item.get('alternate_url', '')
        }

        # Пропускаем вакансии без company_id
        if vacancy['company_id']:
            vacancies.append(vacancy)

    return vacancies


def load_data_from_json_file(filename: str) -> None:
    """
    Загрузка данных из JSON-файла в базу данных

    Args:
        filename: Имя JSON-файла
    """
    print(f"Загрузка данных из файла: {filename}")

    # Читаем JSON-файл
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    print(f"Найдено вакансий: {data.get('found', 0)}")

    # Извлекаем компании и вакансии
    companies = load_companies_from_json(data)
    vacancies = load_vacancies_from_json(data)

    print(f"Уникальных компаний: {len(companies)}")
    print(f"Вакансий для загрузки: {len(vacancies)}")

    # Создаем менеджер БД
    db_manager = DBManager(DB_CONFIG)

    # Сохраняем компании
    if companies:
        db_manager.save_companies(companies)
        print(f"Сохранено {len(companies)} компаний")

    # Сохраняем вакансии
    if vacancies:
        db_manager.save_vacancies(vacancies)
        print(f"Сохранено {len(vacancies)} вакансий")

    # Выводим статистику
    print("\n" + "=" * 80)
    print("СТАТИСТИКА ЗАГРУЖЕННЫХ ДАННЫХ:")
    print("=" * 80)

    companies_count = db_manager.get_companies_and_vacancies_count()
    for company_name, vacancies_count in companies_count:
        print(f"  • {company_name}: {vacancies_count} вакансий")

    avg_salary = db_manager.get_avg_salary()
    print(f"\n  • Средняя зарплата по всем вакансиям: {avg_salary:.2f} руб.")

    print("\n" + "=" * 80)
    print("ВАКАНСИИ С ЗАРПЛАТОЙ ВЫШЕ СРЕДНЕЙ:")
    print("=" * 80)
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for company_name, vacancy_name, salary, url in high_salary_vacancies[:5]:
        print(f"  • {company_name} — {vacancy_name}")
        print(f"    Зарплата: {salary}")
        print(f"    Ссылка: {url}\n")


if __name__ == "__main__":
    # Загружаем данные из файла
    load_data_from_json_file('hh_vacancies_sample.json')
