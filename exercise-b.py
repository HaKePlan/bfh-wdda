import argparse
import sqlite3
from typing import Tuple, List


def execute_query(con: sqlite3.Connection, sql: str, _args: Tuple) -> List[Tuple]:
    cursor = con.cursor()

    announcements = []
    for _row in cursor.execute(sql, _args):
        announcements.append(_row)

    return announcements


def get_announcement_by_city_name(con: sqlite3.Connection, name: str) -> List[Tuple]:
    sql = "SELECT homeType, price, description FROM view_California_real_estate WHERE city LIKE ?;"
    _args = (name,)

    result = execute_query(con, sql, _args)
    return result


def get_announcement_by_year_build(con: sqlite3.Connection, year: int):
    sql = "SELECT COUNT (year_build) AS anzahl_immobilien FROM House WHERE House.year_build > ?;"
    _args = (year,)

    result = execute_query(con, sql, _args)
    return result


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Extract announcements by arguments')
    parser.add_argument('-c', action='store', type=str)
    parser.add_argument('-y', action='store', type=int)
    args = parser.parse_args()

    connection = sqlite3.connect('./project_data.sqlite')

    if args.c:
        city = args.c
        announcement_city = get_announcement_by_city_name(connection, city)
        print(f"announcements for city '{city}'")
        print(f"-------------------------------")
        for row in announcement_city:
            print(row)

    if args.y:
        try:
            year_build = int(args.y)
        except ValueError:
            raise Exception('Please provide only a numeric year (e.g. 2022, 2021, etc.)')
        announcement_year_build = get_announcement_by_year_build(connection, year_build)

        print()
        print(f"number of announcements with year build '{year_build}'")
        print(f"------------------------------------------------------")
        for row in announcement_year_build:
            print(row[0])
