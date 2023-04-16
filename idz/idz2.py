#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import os.path
from dotenv import load_dotenv


def add_wrk(pep,name,num,year):
    pep.append(
        {
            'name': name,
            'num': num,
            'year': year
        }
    )
    return pep

def li(pep):
     line = '+-{}-+-{}-+-{}-+-{}-+'.format(
                '-' * 4,
                '-' * 30,
                '-' * 20,
                '-' * 8
            )
     print(line)
     print(
          '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
              "№",
              "F.I.O.",
              "NUMBER",
              "BRDAY"
          )
     )
     print(line)
     for idx, chel in enumerate(pep, 1):
        print(
             '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                 idx,
                 chel.get('name', ''),
                 chel.get('num', ''),
                 chel.get('year', 0)
             )
        )
        print(line)


def sel(pep, numb):
     ot = []
     # Проверить сведения работников из списка.
     for chel in pep:
        if numb in str(chel.values()):
            ot.append(chel)
     return ot


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
# Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("pep")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new human"
    )
    add.add_argument(
        "-na",
        "--name",
        action="store",
        required=True,
        help="The human's name"
    )
    add.add_argument(
        "-n",
        "--num",
        action="store",
        type=int,
        required=True,
        help="The human's number"
    )
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=int,
        required=True,
        help="The date of human's birth"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all humans"
    )

    # Создать субпарсер для выбора людей.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the humans"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    data_file = args.data
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    if not data_file:
        data_file = os.environ.get("IDZ1")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех людей из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        pep = load_workers(data_file)
    else:
        pep = []

    # Добавить человека.
    if args.command == "add":
        pep = add_wrk(
            pep,
            args.name,
            args.num,
            args.year
        )
        is_dirty = True


    # Отобразить всех людей.
    elif args.command == "display":
        li(pep)

    # Выбрать требуемых людей.
    elif args.command == "select":
        selected = sel(pep, args.select)
        li(selected)

    # Сохранить данные в файл, если список людей был изменен.
    if is_dirty:
        save_workers(data_file, pep)


if __name__ == '__main__':
    main()