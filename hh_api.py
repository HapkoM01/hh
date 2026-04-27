"""Модуль для взаимодействия с API hh.ru"""

import requests
import time
from typing import List, Dict, Any


class HHApi:
    """Класс для работы с API HeadHunter"""

    def __init__(self, base_url: str = 'https://api.hh.ru'):
        """
        Инициализация API клиента

        Args:
            base_url: Базовый URL API hh.ru
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })

    def _make_request(self, url: str, params: dict = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        Выполнение запроса с повторными попытками

        Args:
            url: URL запроса
            params: Параметры запроса
            max_retries: Максимальное количество попыток

        Returns:
            JSON ответа
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    if attempt < max_retries - 1:
                        print(f"   Попытка {attempt + 1} не удалась (403), ждём 2 секунды...")
                        time.sleep(2)
                        # Меняем User-Agent при каждой попытке
                        self.session.headers.update({
                            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12{attempt}0.0.0 Safari/537.36'
                        })
                        continue
                else:
                    response.raise_for_status()

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"   Ошибка: {e}, повторная попытка {attempt + 2}...")
                    time.sleep(2)
                else:
                    raise

        raise Exception(f"Не удалось выполнить запрос после {max_retries} попыток")

    def get_company(self, company_id: str) -> Dict[str, Any]:
        """
        Получение информации о компании по ID

        Args:
            company_id: ID компании на hh.ru

        Returns:
            Dict с данными о компании
        """
        url = f'{self.base_url}/employers/{company_id}'
        return self._make_request(url)

    def get_vacancies(self, company_id: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Получение списка вакансий компании

        Args:
            company_id: ID компании на hh.ru
            per_page: Количество вакансий на странице

        Returns:
            List вакансий компании
        """
        vacancies = []
        page = 0

        while True:
            url = f'{self.base_url}/vacancies'
            params = {
                'employer_id': company_id,
                'per_page': per_page,
                'page': page
            }

            try:
                data = self._make_request(url, params)
                vacancies.extend(data.get('items', []))

                if page >= data.get('pages', 1) - 1:
                    break
                page += 1
                time.sleep(0.5)  # Задержка между страницами

            except Exception as e:
                print(f"   Ошибка при получении вакансий для компании {company_id}: {e}")
                break

        return vacancies

    def get_vacancy_details(self, vacancy_id: str) -> Dict[str, Any]:
        """
        Получение детальной информации о вакансии

        Args:
            vacancy_id: ID вакансии

        Returns:
            Dict с детальной информацией о вакансии
        """
        url = f'{self.base_url}/vacancies/{vacancy_id}'
        return self._make_request(url)
