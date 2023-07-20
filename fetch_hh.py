import argparse
from itertools import count

import requests

from functions_predict_salary import convert_to_table, predict_salary
from languages import languages as default_languages
from search_settings import HHSearchSettings


def predict_rub_salary_for_hh(vacancy):
    if not vacancy or vacancy['currency'] != 'RUR':
        return None
    salary_from = vacancy["from"]
    salary_to = vacancy["to"]
    vacancy_salary_predict = predict_salary(salary_from, salary_to)
    return vacancy_salary_predict


def calculate_average_salary_hh(vacancies):
    if not vacancies:
        return 0, 0
    salary_predict_sum = 0
    processed_vacancies_count = 0
    for vacancy in vacancies:
        vacancy_salary = vacancy["salary"]
        vacancy_salary_predict = predict_rub_salary_for_hh(vacancy_salary)
        if not vacancy_salary_predict:
            if len(vacancies) == 1:
                return 0, 0
            continue
        salary_predict_sum += vacancy_salary_predict
        processed_vacancies_count += 1
    average_salary = int(salary_predict_sum / processed_vacancies_count)
    return processed_vacancies_count, average_salary


def fetch_vacancies_hh(programming_languages, search_settings):
    url = "https://api.hh.ru/vacancies"
    hh_vacansies = {}
    for programming_language in programming_languages:
        found_vacancies = []
        for page in count(0):
            params = {
                "area": search_settings.search_area,
                "text": f"{programming_language}",
                "search_field": search_settings.search_field,
                "period": search_settings.search_period,
                "page": page,
                "per_page": search_settings.per_page_result_count,
                }
            try:
                hh_response = requests.get(url, params=params)
                hh_response.raise_for_status
                received_vacancies = hh_response.json()
            except requests.exceptions.RequestException as error:
                print("Произошла ошибка при выполнении запроса:", error)
            if page == received_vacancies['pages']:
                break
            vacancies = received_vacancies["items"]
            found_vacancies.extend(vacancies)
            hh_vacansies[programming_language] = found_vacancies
    return hh_vacansies


def process_vacancy_statistics_hh(programming_languages, search_settings):
    programming_language_statistics = {}
    hh_vacancies = fetch_vacancies_hh(programming_languages, search_settings)
    for (
        programming_language_vacancy,
        found_vacancies
    ) in hh_vacancies.items():
        vacancies_found = len(found_vacancies)
        vacancies_processed, average_salary = calculate_average_salary_hh(
            found_vacancies
        )
        programming_language_statistics[programming_language_vacancy] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return programming_language_statistics


def main():
    parser = argparse.ArgumentParser(
        description='Программа собирает статистику по вакансиям '
                    'с headhunter.ru'
    )
    parser.add_argument(
        '-pl',
        '--programming_languages',
        nargs='+',
        default=default_languages,
        help='Язык программрования который быдет указан в названии вакансии'
    )
    args = parser.parse_args()
    programming_languages = args.programming_languages
    hh_table_title = "HeadHunter Moscow"
    search_settings = HHSearchSettings(
        search_area=1,
        search_field="name",
        search_period=30,
        per_page_result_count=100
    )
    programming_language_statistics = process_vacancy_statistics_hh(
        programming_languages,
        search_settings
    )
    hh_vacansies_table = convert_to_table(
        hh_table_title,
        programming_language_statistics
    )
    print(hh_vacansies_table.table)


if __name__ == '__main__':
    main()
