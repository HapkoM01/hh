"""Модуль для создания базы данных и таблиц"""

import psycopg2
from typing import Dict, Any


class DBCreator:
    """Класс для создания базы данных и таблиц"""

    def __init__(self, db_config: Dict[str, Any]):
        """
        Инициализация создателя БД

        Args:
            db_config: Конфигурация для подключения к БД
        """
        self.db_config = db_config

    def create_database(self, db_name: str) -> None:
        """
        Создание базы данных

        Args:
            db_name: Имя создаваемой базы данных
        """
        # Подключаемся к postgres для создания новой БД
        conn = psycopg2.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            database='postgres',
            user=self.db_config['user'],
            password=self.db_config['password']
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем существование БД
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE {db_name}')

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """Создание таблиц в базе данных"""
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        # Создание таблицы компаний
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                description TEXT,
                url VARCHAR(255),
                vacancies_url VARCHAR(255)
            )
        """)

        # Создание таблицы вакансий
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id) ON DELETE CASCADE,
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(3),
                url VARCHAR(255)
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

    def init_database(self, db_name: str) -> None:
        """
        Полная инициализация БД (создание БД и таблиц)

        Args:
            db_name: Имя базы данных
        """
        self.create_database(db_name)
        self.create_tables()
