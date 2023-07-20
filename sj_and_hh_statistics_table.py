import os

from dotenv import load_dotenv

from fetch_hh import process_vacancy_statistics_hh
from fetch_sj import process_vacancy_statistics_sj
from functions_predict_salary import convert_to_table
import search_settings


def main():
    default_languages = [
        "Python",
        "Golang",
        "Java",
        "JavaScript",
        "C",
        "Scala",
        "C++",
        "C#",
        "SQL",
    ]
    load_dotenv()
    sj_app_id = os.environ['SJ_APP_ID']
    if not sj_app_id:
        print("APP_ID в .env не задан")
        return
    hh_table_title = "HeadHunter Moscow"
    sj_table_title = "SuperJob Moscow"
    hh_search_settings = search_settings.HHSearchSettings(
        search_area=1,
        search_field="name",
        search_period=30,
        per_page_result_count=100
    )
    hh_programming_language_statistics = process_vacancy_statistics_hh(
        default_languages,
        hh_search_settings
    )
    hh_vacansies_table = convert_to_table(
        hh_table_title,
        hh_programming_language_statistics
    )
    sj_search_settings = search_settings.SJSearchSettings(
        search_town=4,
        search_catalogues=48,
        search_block=1,
        search_method="particular",
        per_page_result_count=20

    )
    sj_programming_language_statistics = process_vacancy_statistics_sj(
        sj_app_id,
        default_languages,
        sj_search_settings
    )
    sj_vacansies_table = convert_to_table(
        sj_table_title,
        sj_programming_language_statistics
    )
    print(hh_vacansies_table.table, sj_vacansies_table.table)


if __name__ == '__main__':
    main()
