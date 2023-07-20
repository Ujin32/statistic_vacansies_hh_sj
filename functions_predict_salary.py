from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    elif salary_from and salary_to:
        final_salary = (salary_to + salary_from)/2
        return final_salary
    elif salary_from and not salary_to:
        final_salary = salary_from*1.2
        return final_salary
    elif not salary_from and salary_to:
        final_salary = salary_to*0.8
        return final_salary


def convert_to_table(title, statistics_vacansies):
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for programm_language, statistics in statistics_vacansies.items():
        programming_language_statistics = [
            programm_language,
            statistics['vacancies_found'],
            statistics['vacancies_processed'],
            statistics['average_salary']
        ]
        table_data.append(programming_language_statistics)

    table = AsciiTable(table_data, title)
    return table
