import sys
import csv

def getDeps(file):
    op = open(file, 'r')
    reader = csv.reader(op, delimiter=';')
    departments = {}
    for line in reader:
        departments[line[2]] = ''
    return departments

def makeAReport(file):
    report = getDeps(file)
    op = open(file, 'r')
    reader = csv.reader(op, delimiter=';')

    for keys in report.keys():
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
        report[keys]['avg'] = sum(report[keys]['avg']) / len(report[keys]['avg'])
    return report

def printAReport(file):
    makeAReport(file)

def saveAReport(file):
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
            report[keys]['avg'],
            ])
    output.close()
    return 'success'


def process():
    file = sys.argv[1]
    print('Что делать?\n'
          '1 - вывести все отделы\n'
          '2 - вывести сводный отчёт по отделам\n'
          '3 - вывести сводный отчёт по отделам в csv-файл\n')
    options = {
        '1': getDeps,
        '2': printAReport,
        '3': saveAReport,
        }
    result = options[input()](file)
    print(result)

if len (sys.argv) == 1:
    print('дайте файл')
    sys.exit(1)

process()
