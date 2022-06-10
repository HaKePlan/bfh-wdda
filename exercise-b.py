import argparse
import sqlite3
from typing import Tuple, List


def execute_query(con: sqlite3.Connection, sql: str, _args: Tuple) -> List[Tuple]:
    """Execute query with params and return rows in a list of tuples

    Parameters
    ----------
    con : sqlite3.Connection
        sqlite connection
    sql : str
        sql query as string
    _args : Tuple
        sql params as Tuple (more than one element is needed)

    Returns
    -------
    List[Tuple]
        a list of tuples for found entries
    """
    cursor = con.cursor()

    announcements = []
    for _row in cursor.execute(sql, _args):
        announcements.append(_row)

    return announcements


def get_announcement_by_city_name(con: sqlite3.Connection, name: str) -> List[Tuple]:
    """Get announcements for a specified city.
    Generate sql query and sql params. Call execute function and return received result

    Parameters
    ----------
    con : sqlite3.Connection
        sqlite connection
    name : str
        the name of the city

    Returns
    -------
    List[Tuple]
        a list of tuples for found entries
    """
    sql = "SELECT homeType, price, description FROM view_California_real_estate WHERE city LIKE ?;"
    _args = (name,)

    # make use of parametrized sql statements to avoid sql injection risks and improve performance
    result = execute_query(con, sql, _args)
    return result


def get_announcement_by_year_build(con: sqlite3.Connection, year: int):
    """Get number of announcements with houses build by specified year.
    Generate sql query and sql params. Call execute function and return received result

    Parameters
    ----------
    con : sqlite3.Connection
        sqlite connection
    year : int
        the year build

    Returns
    -------
    List[Tuple]
        a list of tuples for found entries
    """
    sql = "SELECT COUNT (year_build) AS anzahl_immobilien FROM House WHERE House.year_build > ?;"
    _args = (year,)

    result = execute_query(con, sql, _args)
    return result


if __name__ == '__main__':

    # generate possible arguments for this script
    parser = argparse.ArgumentParser('Extract announcements by arguments')
    parser.add_argument('-c', action='store', type=str, help='name of a city')
    parser.add_argument('-y', action='store', type=int, help='year to filter; shows all which are newer than year')

    # parse given arguments by calling this script
    args = parser.parse_args()

    # create connection to our sql database
    connection = sqlite3.connect('./project_data.sqlite')

    # execute function based on the given arguments
    if args.c:
        city = args.c

        # try to fetch announcements for given city name
        announcement_city = get_announcement_by_city_name(connection, city)
        print(f"announcements for city '{city}'")
        print(f"-------------------------------")
        for row in announcement_city:
            print(row)

    if args.y:
        # validate if year bild is truly an int and not something else
        try:
            year_build = int(args.y)
        except ValueError:
            raise Exception('Please provide only a numeric year (e.g. 2022, 2021, etc.)')
        announcement_year_build = get_announcement_by_year_build(connection, year_build)

        print()
        print(f"number of announcements with year build '{year_build}'")
        print(f"------------------------------------------------------")
        # fetch number of announcements for given year
        for row in announcement_year_build:
            print(row[0])

    # exit with statuscode 0 to tell the user that the script worked with no errors
    exit(0)
