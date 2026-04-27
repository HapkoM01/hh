"""Модуль для работы с данными в БД"""

import psycopg2
from typing import List, Dict, Any, Optional


class DBManager:
    """Класс для управления данными в базе данных"""

    def __init__(self, db_config: Dict[str, Any]):
        """
        Инициализация менеджера БД

        Args:
            db_config: Конфигурация для подключения к БД
        """
        self.db_config = db_config

    def _execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """
        Выполнение SQL-запроса и возврат результата

        Args:
            query: SQL-запрос
            params: Параметры запроса

        Returns:
            List результатов запроса
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def save_companies(self, companies: List[Dict[str, Any]]) -> None:
        """
        Сохранение компаний в БД

        Args:
            companies: Список словарей с данными о компаниях
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        for company in companies:
            cur.execute("""
                INSERT INTO companies (company_id, company_name, description, url, vacancies_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (company_id) DO UPDATE SET
                    company_name = EXCLUDED.company_name,
                    description = EXCLUDED.description
            """, (
                company['company_id'],
                company['company_name'],
                company.get('description'),
                company.get('url'),
                company.get('vacancies_url')
            ))

        conn.commit()
        cur.close()
        conn.close()

    def save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Сохранение вакансий в БД

        Args:
            vacancies: Список словарей с данными о вакансиях
        """
        if not vacancies:
            print("   Нет данных о вакансиях для сохранения")
            return

        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        for vacancy in vacancies:
            try:
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO UPDATE SET
                        vacancy_name = EXCLUDED.vacancy_name,
                        salary_from = EXCLUDED.salary_from,
                        salary_to = EXCLUDED.salary_to,
                        currency = EXCLUDED.currency
                """, (
                    vacancy.get('vacancy_id'),
                    vacancy.get('company_id'),
                    vacancy.get('vacancy_name'),
                    vacancy.get('salary_from'),
                    vacancy.get('salary_to'),
                    vacancy.get('currency'),
                    vacancy.get('url')
                ))
            except Exception as e:
                print(f"   Ошибка при сохранении вакансии {vacancy.get('vacancy_id')}: {e}")
                continue

        conn.commit()
        cur.close()
        conn.close()

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """
        Получение списка всех компаний и количества вакансий у каждой компании

        Returns:
            List кортежей (company_name, vacancies_count)
        """
        query = """
            SELECT c.company_name, COUNT(v.vacancy_id) as vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.company_id = v.company_id
            GROUP BY c.company_id, c.company_name
            ORDER BY vacancies_count DESC
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> List[tuple]:
        """
        Получение списка всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию

        Returns:
            List кортежей (company_name, vacancy_name, salary, url)
        """
        query = """
            SELECT c.company_name, 
                   v.vacancy_name,
                   CASE 
                       WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL 
                           THEN CONCAT(v.salary_from, ' - ', v.salary_to, ' ', COALESCE(v.currency, ''))
                       WHEN v.salary_from IS NOT NULL 
                           THEN CONCAT('от ', v.salary_from, ' ', COALESCE(v.currency, ''))
                       WHEN v.salary_to IS NOT NULL 
                           THEN CONCAT('до ', v.salary_to, ' ', COALESCE(v.currency, ''))
                       ELSE 'Не указана'
                   END as salary,
                   v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            ORDER BY c.company_name, v.vacancy_name
        """
        return self._execute_query(query)

    def get_avg_salary(self) -> float:
        """
        Получение средней зарплаты по вакансиям

        Returns:
            Средняя зарплата (float)
        """
        query = """
            SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2) as avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        result = self._execute_query(query)
        return result[0][0] if result[0][0] else 0.0

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """
        Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям

        Returns:
            List кортежей с данными о вакансиях с зарплатой выше средней
        """
        avg_salary = self.get_avg_salary()

        query = """
            SELECT c.company_name, 
                   v.vacancy_name,
                   CONCAT(COALESCE(v.salary_from::text, ''), ' - ', 
                          COALESCE(v.salary_to::text, ''), ' ', 
                          COALESCE(v.currency, '')) as salary,
                   v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 > %s
            ORDER BY (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
        """
        return self._execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """
        Получение списка всех вакансий, в названии которых содержатся переданные слова

        Args:
            keyword: Ключевое слово для поиска

        Returns:
            List вакансий, содержащих ключевое слово в названии
        """
        query = """
            SELECT c.company_name, 
                   v.vacancy_name,
                   CONCAT(COALESCE(v.salary_from::text, ''), ' - ', 
                          COALESCE(v.salary_to::text, ''), ' ', 
                          COALESCE(v.currency, '')) as salary,
                   v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            WHERE v.vacancy_name ILIKE %s
            ORDER BY c.company_name, v.vacancy_name
        """
        return self._execute_query(query, (f'%{keyword}%',))
