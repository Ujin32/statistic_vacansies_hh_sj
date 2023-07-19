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


def convert_to_table(title, statistic_vacansies):
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for key, dict_values in statistic_vacansies.items():
        list_vacans = [
            key,
            dict_values['vacancies_found'],
            dict_values['vacancies_processed'],
            dict_values['average_salary']
        ]
        table_data.append(list_vacans)

    table = AsciiTable(table_data, title)
    return table
