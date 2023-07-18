import argparse
from itertools import count

import requests

from functions_predict_salary import convert_to_table, predict_salary
from languages import languages as default_languages


def predict_rub_salary_for_hh(vacancy):
    if vacancy is None or vacancy['currency'] != 'RUR':
        return None
    salary_from = vacancy["from"]
    salary_to = vacancy["to"]
    salary_predict_vacancy = predict_salary(salary_from, salary_to)
    return salary_predict_vacancy


def calculate_average_salary_hh(vacancies):
    if not vacancies:
        return 0, 0
    sum_predict_salary = 0
    processed_vacancies_count = 0
    for _, vacancy in enumerate(vacancies):
        vacancy_salary = vacancy["salary"]
        salary_predict_vacancy = predict_rub_salary_for_hh(vacancy_salary)
        if salary_predict_vacancy is None:
            if len(vacancies) == 1:
                return 0, 0
            continue
        sum_predict_salary += salary_predict_vacancy
        processed_vacancies_count += 1
    average_salary = int(sum_predict_salary / processed_vacancies_count)
    return processed_vacancies_count, average_salary


def fetch_all_vacancies_hh(programm_languages):
    url = "https://api.hh.ru/vacancies"
    hh_vacansies = {}
    for _, programm_language in enumerate(programm_languages):
        pages_data_language = []
        for page in count(0):
            params = {
                "area": 1,
                "text": f"{programm_language }",
                "search_field": "name",
                "period": 30,
                "page": page,
                "per_page": 100,
                }
            try:
                hh_response = requests.get(url, params=params)
                hh_response.raise_for_status
                vacancies_info = hh_response.json()
            except requests.exceptions.RequestException as error:
                print("Произошла ошибка при выполнении запроса:", error)
            if page == vacancies_info['pages']:
                break
            vacancies_page = vacancies_info["items"]
            pages_data_language.extend(vacancies_page)
            hh_vacansies[programm_language] = pages_data_language
    return hh_vacansies


def process_vacancy_statistics_hh(programm_languages):
    programming_language_statistics = {}
    hh_vacancies = fetch_all_vacancies_hh(programm_languages)
    for (
        programm_language_vacancies,
        all_vacancies_program_language
    ) in hh_vacancies.items():
        vacancies_found = len(all_vacancies_program_language)
        vacancies_processed, average_salary = calculate_average_salary_hh(
            all_vacancies_program_language
            )
        programming_language_statistics[programm_language_vacancies] = {
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
        '--program_language',
        nargs='+',
        default=default_languages,
        help='Язык программрования который быдет указан в названии вакансии'
    )
    args = parser.parse_args()
    programming_languages = args.program_language
    title = "HeadHunter Moscow"
    programming_language_statistics = process_vacancy_statistics_hh(
        programming_languages
        )
    convert_to_table(title,  programming_language_statistics)


if __name__ == '__main__':
    main()
