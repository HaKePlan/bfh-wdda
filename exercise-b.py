import argparse
import sqlite3


def get_city_by_name(con: sqlite3.Connection, name: str) -> None:
    cursor = con.cursor()

    for row in cursor.execute("""
    SELECT 
        homeType, 
        price, 
        description 
    FROM view_California_real_estate 
    WHERE city = ?
    """, name):
        print(row)


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Extract announcements by arguments')
    parser.add_argument('-c', action='store')
    parser.add_argument('-y', action='store')
    args = parser.parse_args()

    connection = sqlite3.connect('./project_data.sqlite')

    if args.c:
        print(args.c)
    if args.y:
        print(args.y)
