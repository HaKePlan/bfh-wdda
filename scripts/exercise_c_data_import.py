import csv
import sqlite3
from typing import List


class Voter:
    def __init__(self, county_name: str, eligible: str, total_registered: str):
        """Voter calss with all voter columns.

        Parameters
        ----------
        county_name : str
            Name of county
        eligible : str
            Number of eligible persons as string
        total_registered : str
            Number of registered persons as string
        """
        self.county_name = county_name
        self.eligible = int(eligible.replace('’', ''))
        self.total = int(total_registered.replace('’', ''))
        pass

    def get_county_id(self, con: sqlite3.Connection) -> int:
        """Methode to return the FK for the relational dataset

        Parameters
        ----------
        con : sqlite3.Connection
            connection to the database

        Returns
        -------
        int
            The ID (FK) from the related dataset as an integer
        """
        _cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from County where county_name like '{self.county_name} County'"""):
            _id = row[0]

        return int(_id)


def read_csv(path: str) -> List[Voter]:
    """Read CSV from path and return first three columns of each row in a list

    Parameters
    ----------
    path : str
        The path to the voters' data csv file as string

    Returns
    -------
    A list of Voter class instances with data from the csv
    """
    rows = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter=';')
        i = 0
        for row in reader:
            i += 1
            # check that the header is not in our data
            if i > 1:
                rows.append(Voter(row[0], row[1], row[2]))
            else:
                continue

    return rows


def write_voter(voter_data_list: List[Voter], con: sqlite3.Connection) -> None:
    """Write the list of Voter in database

    Parameters
    ----------
    voter_data_list : List[Voter]
        The list of the Voter instances as data for the database
    con : sqlite3.Connection
        connection to the database
    """
    _cursor = con.cursor()

    for row in voter_data_list:
        _cursor.execute(
            f"""insert into Voter values (null, '{row.eligible}', '{row.total}', {row.get_county_id(con)});"""
        )

    con.commit()


if __name__ == '__main__':
    voter_data_file = '../voters_by_county_clean.csv'
    connection = sqlite3.connect('../project_data.sqlite')
    cursor = connection.cursor()

    # try to delete table first
    try:
        cursor.execute("drop table Voter;")
        connection.commit()
    except sqlite3.OperationalError:
        print('Table "Voter" not found. Carry on with script')

    # assemble table creation command
    new_table_command = """
        CREATE TABLE `Voter` (
            `id` INTEGER NOT NULL,
            `eligible` INTEGER NOT NULL,
            `total_registered` INTEGER NOT NULL,
            `county_id` INTEGER NOT NULL,
            PRIMARY KEY (`id` AUTOINCREMENT),
            FOREIGN KEY (`county_id`) references `County` (`id`)
        );
    """

    if connection is not None:
        # create table
        cursor.execute(new_table_command)
        connection.commit()

        # read data from csv file
        voter_data = read_csv(voter_data_file)

        # write data from csv file to db
        write_voter(voter_data, connection)

    else:
        raise Exception('Connection to project_data.sqlite is not established. Please check if db is in right path.')





