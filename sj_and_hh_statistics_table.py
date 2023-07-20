import os

from dotenv import load_dotenv

from fetch_hh import process_vacancy_statistics_hh
from fetch_sj import process_vacancy_statistics_sj
from functions_predict_salary import convert_to_table
from languages import languages as default_languages


def main():
    load_dotenv()
    sj_app_id = os.environ['SJ_APP_ID']
    if not sj_app_id:
        print("APP_ID в .env не задан")
        return
    hh_table_title = "HeadHunter Moscow"
    sj_table_title = "SuperJob Moscow"
    hh_programming_language_statistics = process_vacancy_statistics_hh(
        default_languages
    )
    hh_vacansies_table = convert_to_table(
        hh_table_title,
        hh_programming_language_statistics
    )
    sj_programming_language_statistics = process_vacancy_statistics_sj(
        sj_app_id,
        default_languages
    )
    sj_vacansies_table = convert_to_table(
        sj_table_title,
        sj_programming_language_statistics
    )
    print(hh_vacansies_table, sj_vacansies_table)


if __name__ == '__main__':
    main()
