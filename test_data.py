"""Тестовые данные для проверки работы БД"""

test_companies = [
    {'company_id': 1740, 'company_name': 'Яндекс', 'description': 'Российская IT-компания, разработка поисковой системы, сервисов такси, доставки и других продуктов', 'url': 'https://yandex.ru', 'vacancies_url': 'https://hh.ru/employer/1740'},
    {'company_id': 3529, 'company_name': 'Сбербанк', 'description': 'Крупнейший банк России и IT-компания', 'url': 'https://sberbank.ru', 'vacancies_url': 'https://hh.ru/employer/3529'},
    {'company_id': 80, 'company_name': 'VK', 'description': 'Российская IT-компания, развивает социальную сеть ВКонтакте, почту Mail.ru и другие сервисы', 'url': 'https://vk.company', 'vacancies_url': 'https://hh.ru/employer/80'},
    {'company_id': 39305, 'company_name': 'Газпромбанк', 'description': 'Один из крупнейших банков России', 'url': 'https://gazprombank.ru', 'vacancies_url': 'https://hh.ru/employer/39305'},
    {'company_id': 2180, 'company_name': 'Ozon', 'description': 'Крупнейший маркетплейс России', 'url': 'https://ozon.ru', 'vacancies_url': 'https://hh.ru/employer/2180'},
    {'company_id': 15478, 'company_name': 'Wildberries', 'description': 'Крупнейший онлайн-ретейлер России', 'url': 'https://wildberries.ru', 'vacancies_url': 'https://hh.ru/employer/15478'},
    {'company_id': 87021, 'company_name': 'Тинькофф', 'description': 'Банк и экосистема финансовых и IT-сервисов', 'url': 'https://tbank.ru', 'vacancies_url': 'https://hh.ru/employer/87021'},
    {'company_id': 3776, 'company_name': 'МТС', 'description': 'Телекоммуникационная компания и IT-разработчик', 'url': 'https://mts.ru', 'vacancies_url': 'https://hh.ru/employer/3776'},
    {'company_id': 1057, 'company_name': 'Билайн', 'description': 'Телекоммуникационная компания', 'url': 'https://beeline.ru', 'vacancies_url': 'https://hh.ru/employer/1057'},
    {'company_id': 2381, 'company_name': 'Ростелеком', 'description': 'Крупнейший провайдер цифровых услуг в России', 'url': 'https://rostelecom.ru', 'vacancies_url': 'https://hh.ru/employer/2381'},
]

test_vacancies = [
    {'vacancy_id': 1, 'company_id': 1740, 'vacancy_name': 'Python разработчик', 'salary_from': 200000, 'salary_to': 300000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/1'},
    {'vacancy_id': 2, 'company_id': 1740, 'vacancy_name': 'Java разработчик', 'salary_from': 180000, 'salary_to': 250000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/2'},
    {'vacancy_id': 3, 'company_id': 1740, 'vacancy_name': 'Data Scientist', 'salary_from': 220000, 'salary_to': 350000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/3'},  # ИСПРАВЛЕНО: было 'vaccancy_name'
    {'vacancy_id': 4, 'company_id': 3529, 'vacancy_name': 'Python разработчик', 'salary_from': 170000, 'salary_to': 220000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/4'},
    {'vacancy_id': 5, 'company_id': 3529, 'vacancy_name': 'Frontend разработчик', 'salary_from': 150000, 'salary_to': 200000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/5'},
    {'vacancy_id': 6, 'company_id': 3529, 'vacancy_name': 'DevOps инженер', 'salary_from': 190000, 'salary_to': 280000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/6'},
    {'vacancy_id': 7, 'company_id': 80, 'vacancy_name': 'Python разработчик', 'salary_from': 180000, 'salary_to': 250000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/7'},
    {'vacancy_id': 8, 'company_id': 80, 'vacancy_name': 'Go разработчик', 'salary_from': 200000, 'salary_to': 300000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/8'},
    {'vacancy_id': 9, 'company_id': 39305, 'vacancy_name': 'Java разработчик', 'salary_from': 160000, 'salary_to': 220000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/9'},
    {'vacancy_id': 10, 'company_id': 2180, 'vacancy_name': 'Python разработчик', 'salary_from': 190000, 'salary_to': 260000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/10'},
    {'vacancy_id': 11, 'company_id': 2180, 'vacancy_name': 'Аналитик данных', 'salary_from': 140000, 'salary_to': 190000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/11'},
    {'vacancy_id': 12, 'company_id': 15478, 'vacancy_name': 'Python разработчик', 'salary_from': 200000, 'salary_to': 300000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/12'},
    {'vacancy_id': 13, 'company_id': 87021, 'vacancy_name': 'Data Scientist', 'salary_from': 230000, 'salary_to': 350000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/13'},
    {'vacancy_id': 14, 'company_id': 87021, 'vacancy_name': 'Python разработчик', 'salary_from': 210000, 'salary_to': 320000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/14'},
    {'vacancy_id': 15, 'company_id': 3776, 'vacancy_name': 'Java разработчик', 'salary_from': 170000, 'salary_to': 240000, 'currency': 'RUR', 'url': 'https://hh.ru/vacancy/15'},
]
