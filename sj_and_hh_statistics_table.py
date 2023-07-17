import os

from dotenv import load_dotenv

from fetch_hh import process_vacancy_statistics_hh
from fetch_sj import process_vacancy_statistics_sj
from functions_predict_salary import convert_to_table
from languages import languages as default_languages


def main():
    load_dotenv()
    app_id = os.environ['APP_ID']
    if app_id is None:
        print("APP_ID в .env не задан")
        return
    title_hh = "HeadHunter Moscow"
    title_sj = "SuperJob Moscow"
    convert_to_table(title_hh,  programming_language_statistics)
    programming_language_statistics = process_vacancy_statistics_sj(app_id, default_languages)
    convert_to_table(title_sj,  programming_language_statistics)


if __name__ == '__main__':
    main()