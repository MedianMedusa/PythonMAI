import sys
import csv


def getDeps(file) -> list:
    """
    На входе получает путь до CSV-файла 
    Формирует список отделов из файла file 
    Возвращает лист со списком отделов
    """
    reader = csv.reader(file, delimiter=';')
    departments = {}
    for line in reader:
        departments[line[2]] = ''

    return list(departments.keys())


def makeAReport(file) -> dict:
    """
    На входе получает путь до CSV-файла
    Формирует отчёт на основе списка отделов, полученных 
    из функции getDeps
    Возвращает словарь со сводным отчётом по отделам
    """
    deps = getDeps(file)
    file.seek(0)
    reader = csv.reader(file, delimiter=';')

    report = {}
    for keys in deps:
        report[keys] = dict([
            ('num', 0), 
            ('min', 100_000_000),
            ('max', 0),
            ('avg', list()),
            ])

    for line in reader:
        zp = int(line[4])
        l2 = report[line[2]]
        report[line[2]] = dict([
            ('num', l2['num'] + 1), 
            ('min', l2['min'] if l2['min'] < zp else zp),
            ('max', l2['max'] if l2['max'] > zp else zp),
            ('avg', l2['avg'] + [zp]),
            ])

    
    for keys in report.keys():
        salaries = report[keys]['avg']
        report[keys]['avg'] = sum(salaries) / len(salaries)
    return report


def saveAReport(file) -> str:
    """
    На входе получает путь до CSV-файла
    Сохраняет сводный отчёт по отделам в файл с названием "result.csv"
    Возвращает "success", если всё удачно
    """

    reader = csv.reader(file, delimiter=';')
    report = makeAReport(file)
    output = open('result.csv', 'w')
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['подразделение',
                     'количество сотрудников',
                     'минимальная ЗП',
                     'максимальная ЗП',
                     'средняя ЗП'])
    for keys in report.keys():
        writer.writerow([
            keys, 
            report[keys]['num'],
            report[keys]['min'],
            report[keys]['max'],
            report[keys]['avg']
            ])
    output.close()
    return 'success'


def process() -> None:
    """
    Запускает программу, сохраняет первый параметр как путь до исходного
    CSV-файла, просит пользователя сделать выбор
    """
    file = None
    try:
        file = open(sys.argv[1], 'r')
    except FileNotFoundError:
        print('Нет такого файла')
        exit(1)


    print('Что делать?\n'
          '1 - вывести все отделы\n'
          '2 - вывести сводный отчёт по отделам\n'
          '3 - вывести сводный отчёт по отделам в CSV-файл\n')
    options = {
        '1': getDeps,
        '2': makeAReport,
        '3': saveAReport,
        }
    result = options[input()](file)
    print(result)
    file.close()


if __name__ == '__main__':
    if len (sys.argv) == 1:
        print('дайте файл')
        print('Нажмите Enter для падения')
        input()
    else:
        process()
