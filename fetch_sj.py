import argparse
import os
from itertools import count

import requests
from dotenv import load_dotenv

from functions_predict_salary import convert_to_table, predict_salary
from languages import languages as default_languages


def fetch_vacancies_sj(sj_app_id, programming_languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    sj_vacancies = {}
    headers = {
        "X-Api-App-Id": sj_app_id
    }
    for programming_language in programming_languages:
        found_vacancies = []
        for page in count(0):
            params = {
                "town": 4,
                "catalogues": 48,
                "keywords[0][keys]": f"{programming_language}",
                "keywords[0][srws]": 1,
                "keywords[0][skwc]": "particular",
                "count": 20,
                "page": page
            }
            try:
                sj_response = requests.get(url, headers=headers, params=params)
                sj_response.raise_for_status
                received_vacancies = sj_response.json()
            except requests.exceptions.RequestException as error:
                print("Произошла ошибка при выполнении запроса:", str(error))
            if received_vacancies["total"] == len(found_vacancies):
                break
            vacancies = received_vacancies["objects"]
            found_vacancies.extend(vacancies)
            sj_vacancies[programming_language] = found_vacancies
    return sj_vacancies


def predict_rub_salary_for_sj(vacancy):
    if not vacancy or vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    salary_predict_vacancy = predict_salary(salary_from, salary_to)
    return salary_predict_vacancy


def calculate_average_salary_sj(vacancies):
    if not vacancies:
        return 0, 0
    salary_predict_sum = 0
    processed_vacancies_count = 0
    for vacancy in vacancies:
        vacancy_salary_predict = predict_rub_salary_for_sj(vacancy)
        if not vacancy_salary_predict:
            if len(vacancies) == 1:
                return 0, 0
            continue
        salary_predict_sum += vacancy_salary_predict
        processed_vacancies_count += 1
    average_salary = int(salary_predict_sum / processed_vacancies_count)
    return processed_vacancies_count, average_salary


def process_vacancy_statistics_sj(sj_app_id, programming_languages):
    programming_language_statistics = {}
    sj_vacancies = fetch_vacancies_sj(sj_app_id, programming_languages)
    for (
        programming_language_vacancy,
        found_vacancies
    ) in sj_vacancies.items():
        vacancies_found = len(found_vacancies)
        vacancies_processed, average_salary = calculate_average_salary_sj(
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
        description='Программа собирает статистику по вакансиям c superjob.ru'
    )
    parser.add_argument(
        '-pl',
        '--program_languages',
        nargs='+',
        default=default_languages,
        help='Язык программрования который быдет указан в названии вакансии'
    )

    args = parser.parse_args()
    programming_languages = args.program_languages
    sj_table_title = "SuperJob Moscow"
    load_dotenv()
    sj_app_id = os.environ['SJ_APP_ID']
    if not sj_app_id:
        print("Отсутствует авторизация на SuperJob")
        return

    programming_language_statistics = process_vacancy_statistics_sj(
        sj_app_id,
        programming_languages
    )

    sj_vacansies_table = convert_to_table(
        sj_table_title,
        programming_language_statistics
    )
    print(sj_vacansies_table)


if __name__ == '__main__':
    main()
