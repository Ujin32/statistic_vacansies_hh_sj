import argparse
import os
from itertools import count

import requests
from dotenv import load_dotenv

from functions_predict_salary import convert_to_table, predict_salary
from languages import languages as default_languages


def fetch_all_vacancies_sj(app_id, programm_languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    sj_vacancies = {}
    headers = {
        "X-Api-App-Id": app_id
    }
    for _, programm_language in enumerate(programm_languages):
        programm_language_pages = []
        for page in count(0):
            params = {
                "town": 4,
                "catalogues": 48,
                "keywords[0][keys]": f"{programm_language}",
                "keywords[0][srws]": 1,
                "keywords[0][skwc]": "particular",
                "count": 20,
                "page": page
            }
            try:
                sj_response = requests.get(url, headers=headers, params=params)
                sj_response.raise_for_status
                vacancies_info = sj_response.json()
            except requests.exceptions.RequestException as error:
                print("Произошла ошибка при выполнении запроса:", str(error))
            if vacancies_info["total"] == len(programm_language_pages):
                break
            vacancies_page = vacancies_info["objects"]
            programm_language_pages.extend(vacancies_page)
            sj_vacancies[programm_language] = programm_language_pages
    return sj_vacancies


def predict_rub_salary_for_sj(vacancy):
    if vacancy is None or vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    salary_predict_vacancy = predict_salary(salary_from, salary_to)
    return salary_predict_vacancy


def calculate_average_salary_sj(vacancies):
    if not vacancies:
        return 0, 0
    sum_predict_salary = 0
    processed_vacancies_count = 0
    for _, vacancy in enumerate(vacancies):
        salary_predict_vacancy = predict_rub_salary_for_sj(vacancy)
        if salary_predict_vacancy is None:
            if len(vacancies) == 1:
                return 0, 0
            continue
        sum_predict_salary += salary_predict_vacancy
        processed_vacancies_count += 1
    average_salary = int(sum_predict_salary / processed_vacancies_count)
    return processed_vacancies_count, average_salary


def process_vacancy_statistics_sj(app_id, programm_languages):
    programming_language_statistics = {}
    sj_vacancies = fetch_all_vacancies_sj(app_id, programm_languages)
    for (
        programm_language_vacancies,
        all_vacancies_program_language
    ) in sj_vacancies.items():
        vacancies_found = len(all_vacancies_program_language)
        vacancies_processed, average_salary = calculate_average_salary_sj(
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
        description='Программа собирает статистику по вакансиям c superjob.ru'
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
    title = "SuperJob Moscow"
    load_dotenv()
    app_id = os.environ['APP_ID']
    if app_id is None:
        print("Отсутствует авторизация на SuperJob")
        return
    programming_language_statistics = process_vacancy_statistics_sj(
        app_id,
        programming_languages
    )
    convert_to_table(title, programming_language_statistics)

    
if __name__ == '__main__':
    main()
