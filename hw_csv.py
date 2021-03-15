from faker import Faker
import csv

"""Генерирует csv файл"""
def gen_csv():
    fake = Faker("ru_RU")
    dep = (
        "Отдел логики и логистики",
        "Отдел по борьбе с борьбой",
        "Отдел внедрения велосипедов",
        "Отдел смешных имён и фамилий",
        "Отдел по названию отделов",
    )

    with open("work.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for _ in range(100):
            writer.writerow(
                [
                    fake.name_nonbinary(),
                    fake.job(),
                    dep[fake.pyint(max_value=4)],
                    fake.pyint(min_value=1, max_value=5),
                    fake.pyint(min_value=20589, max_value=99999),
                ]
            )


"""Считывает csv файл"""
def read_csv() -> dict:
    res = {}
    with open("work.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in reader:
            salary = int(row[4])
            """Проверка на повторение отдела:
               Если встречается первый раз, то добавляем в словарь,
               Иначе обновляем информацию."""
            if row[2] not in res.keys():
                res.update({row[2]: [1, salary, salary, salary]})
            else:
                val = res[row[2]]
                val[0] += 1
                val[1] = min(val[1], salary)
                val[2] = max(val[2], salary)
                val[3] += salary
                res.update({row[2]: val})
    return res


"""Выводит названия всех департаментов"""
def print_dep(res: dict):
    for dep in res.keys():
        print(dep)


"""Выводит сводный отчет по отделам"""
def print_rep(res: dict):
    print("\n\tНазвание отдела \t|  Численность\t|\tВилка зарплат\t|\tСредняя зарплата")
    for key, val in res.items():
        avg_sal = float(
            "{:.2f}".format(val[3] / val[0])
        )  # т.к зарплата может быть только в рублях и копейках, то откидываем лишнее
        print(key, val[0], f"{val[1]}-{val[2]}", avg_sal, sep=" \t|\t ")


"""Сохраняет сводный отчет по отделам в csv файл"""
def save_rep(res: dict):
    with open("report.csv", "w", newline="") as csvfile:
        fieldnames = [
            "название отдела",
            "численность",
            "вилка зарплат",
            "средняя зарплата",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, val in res.items():
            avg_sal = float(
                "{:.2f}".format(val[3] / val[0])
            )  # т.к зарплата может быть только в рублях и копейках, то откидываем лишнее
            writer.writerow(
                {
                    "название отдела": key,
                    "численность": val[0],
                    "вилка зарплат": f"{val[1]}-{val[2]}",
                    "средняя зарплата": avg_sal,
                }
            )


if __name__ == "__main__":
    print(
        """\n    Это программа по работе с отчетами компании 'BRAD'.
    Если у вас нет файла со всеми сотрудниками компании, то нажмите 1.
    В этом случае произойдет автоматическая генерация файла.

    Если у вас есть файл со всеми сотрудниками компании, то нажмите 2.
    При этом убедитесь, что он называется 'work.csv', иначе фокуса не произойдет.\n"""
    )
    n = input("    Введите номер пункта меню: ")
    if n == "1":
        gen_csv()
    res = read_csv()
    while True:
        print(
            """\n    Для дальнейшей работы выберите один из следующих пунктов меню: 
        ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
        1 - вывести список отделов компании
        2 - вывести сводный отчёт по отделам
        3 - сохранить отчёт в файл "report.csv"
        0 - выйти из приложения
        ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n
        """
        )
        n = input("    Введите номер пункта меню: ")
        if n == "1":
            print_dep(res)
        elif n == "2":
            print_rep(res)
        elif n == "3":
            save_rep(res)
        elif n == "0":
            break
        else:
            pass
