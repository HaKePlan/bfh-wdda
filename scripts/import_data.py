import curses
import datetime
import sqlite3

from typing import Any, List


# SERIALIZERS
class TableMethods:
    def __init__(self, child: Any, parent: str, parent_table_name: str, field_name: str):
        """Baseclass for most of the datasets and tables.
        This class includes a methode to create the relation between two datasets from two tables (FK relation).

        Parameters
        ----------
        parent : str
            value of parent to look up in parent table (identifier for specific data set in FK table)
        parent_table_name : str
            the name of the table to look for parent
        field_name : str
            the value parent should match to
        """
        self.parent_name = parent
        self.child_name = child
        self.parent_table = parent_table_name
        self.field = field_name

    def get_parent_id(self, con: sqlite3.Connection) -> int:
        """Methode to return the FK for the relational dataset.

        Parameters
        ----------
        con : sqlite3.Connection
            connection to the database

        Returns
        -------
        int
            The ID (FK) from the related dataset as an integer
        """
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from {self.parent_table} where {self.field} = '{self.parent_name}'"""):
            _id = row[0]

        return int(_id)


class Country:
    def __init__(self, country_name: str, currency: str) -> None:
        """Toplevel serializer for countries"""
        self.name = country_name
        self.currency = currency


class Unit:
    """Toplevel serializer for units"""
    def __init__(self, name: str) -> None:
        self.name = name


class CountyToCity:
    def __init__(self, county_name: str, city_name: str):
        """Many to many serializer for county to city relation

        Parameters
        ----------
        county_name : str
            name of the county
        city_name : str
            name of the city
        """
        self.county_name = county_name
        self.city_name = city_name

    def get_county_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the corresponding county id

        Parameters
        ----------
        con : sqlite3.Connection
            connection to the database

        Returns
        -------
        int
            The ID (FK) from the related dataset as an integer
        """
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from County where county_name = '{self.county_name}'"""):
            _id = row[0]
        return int(_id)

    def get_city_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the corresponding city id

        Parameters
        ----------
        con : sqlite3.Connection
            connection to the database

        Returns
        -------
        int
            The ID (FK) from the related dataset as an integer
        """
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from City where city_name = '{self.city_name}'"""):
            _id = row[0]
        return int(_id)


class State(TableMethods):
    def __init__(self, state_name: str, country_name: str) -> None:
        """State serializer
        Parameters
        ---------
        state_name : str
            name of the state
        country_name : str
            name of the country where the state is related to
        """
        parent_table = 'Country'
        table_field = 'country_name'
        super().__init__(state_name, country_name, parent_table, table_field)


class City(TableMethods):
    def __init__(self, city_name: str, state_name: str) -> None:
        """City serializer
        Parameters
        ---------
        city_name : str
            name of the city
        state_name : str
            name of the state where the city is related to
        """
        parent_table = 'State'
        table_field = 'state_name'
        super().__init__(city_name, state_name, parent_table, table_field)


class County(TableMethods):
    def __init__(self, county_name: str, state_name: str) -> None:
        """County serializer
        Parameters
        ---------
        county_name : str
            name of the county
        state_name : str
            name of the state where the county is related to
        """
        parent_table = 'State'
        table_field = 'state_name'
        super().__init__(county_name, state_name, parent_table, table_field)


class BuildingArea(TableMethods):
    def __init__(self, building_area_int: int, living_area: int, living_area_value: int, unit_name: str) -> None:
        """BuildingArea serializer"""
        parent_table = 'Unit'
        table_field = 'name'
        super().__init__(None, unit_name, parent_table, table_field)
        self.building_area_int = building_area_int
        self.living_area = living_area
        self.living_area_value = living_area_value


class House:
    def __init__(
            self,
            longitude: str,
            latitude: str,
            year_build: int,
            bathroom: int,
            has_bad_geocode: int,
            bedroom: int,
            parking: int,
            garage_space: int,
            has_garage: int,
            levels: str,
            pool: int,
            spa: int,
            zip_code: int,
            street_name: str,
            county_name: str,
            city_name: str,
            building_area_int: int,
            living_area: int,
            living_area_value: int,
            unit_name: str,
    ):
        """House serializer"""
        self.parent_county_name = county_name
        self.parent_city_name = city_name

        self.building_area_int = building_area_int
        self.living_area_value = living_area_value
        self.living_area = living_area
        self.unit_name = unit_name

        self.street_name = street_name
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.year_build = year_build
        self.bathroom = bathroom
        self.has_bad_geocode = has_bad_geocode
        self.bedroom = bedroom
        self.parking = parking
        self.garage_space = garage_space
        self.has_garage = has_garage
        self.levels = levels
        self.pool = pool
        self.spa = spa
        self.zip_code = zip_code if zip_code else 'null'

    def get_county_to_city_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the right id of the county and city where the house belongs to"""
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""
        select County_to_City.id 
            from County_to_City 
            inner join City C on County_to_City.city_id = C.id
            inner join County C2 on County_to_City.county_id = C2.id
            where city_name = '{self.parent_city_name}' and county_name = '{self.parent_county_name}'
            """):
            _id = row[0]

        return int(_id)

    def get_building_area_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the building area from the building"""
        cursor = con.cursor()
        _id = ''

        for row in cursor.execute(f"""
            select Building_Area.id from Building_Area
                inner join Unit on Unit.id = Building_Area.unit_id
                where living_area = {self.living_area} and living_area_value = {self.living_area_value} 
                and building_area = {self.building_area_int} and name = '{self.unit_name}'
                """):
            _id = row[0]

        return int(_id)


class Status:
    def __init__(self, status_name: str):
        """Status serializer"""
        self.name = status_name if status_name else 'null'


class HomeType:
    def __init__(self, type_name: str):
        """HomeType serializer"""
        self.name = type_name if type_name else 'null'


class SaleAnnouncement:
    def __init__(
            self,
            announcement_id: str,
            date_posted: str,
            price: int,
            is_for_auction: int,
            price_per_square: int,
            description: str,
            bank_owned: int,
            new_build: int,
            pets: int,
            status_name: str,
            home_type_name: str,
            house_lat: float,
            house_long: float,
    ):
        """SaleAnnouncement serializer"""
        self.announcement_id = announcement_id
        self.date_posted = datetime.datetime.strptime(date_posted, '%d.%m.%Y').strftime('%Y-%m-%d') if date_posted else 'null'
        self.price = price
        self.is_for_auction = is_for_auction
        self.price_per_square = price_per_square
        self.description = description
        self.bank_owned = bank_owned
        self.new_build = new_build
        self.pets = pets

        self.status_name = status_name if status_name else 'null'
        self.home_type_name = home_type_name if home_type_name else 'null'
        self.house_lat = float(house_lat)
        self.house_long = float(house_long)

    def get_status_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the status id (FK)"""
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from Status where status_name = '{self.status_name}'"""):
            _id = row[0]
        return int(_id)

    def get_home_type_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the home type id (FK)"""
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from Home_Type where home_type_name = '{self.home_type_name}'"""):
            _id = row[0]
        return int(_id)

    def get_house_id(self, con: sqlite3.Connection) -> int:
        """Methode to get the hose id (FK)"""
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from House where latitude = {self.house_lat} and longitude = '{self.house_long}'"""):
            _id = row[0]
        return int(_id)


# DELETE ALL DATE IN DATABASE
def delete_data(con: sqlite3.Connection):
    """Delete all data in tables to write new data in it

    Parameters
    ----------
    con : sqlite3.Connection
        connection to database
    """
    # Prepare db for execution
    cursor = con.cursor()

    tables = ['House', 'Country', 'State', 'City', 'County', 'Status', 'Sale_Announcement', 'Unit', 'Building_Area',
              'County_to_City', 'Home_Type']

    for table in tables:
        cursor.execute(f"""delete from {table}""")
        con.commit()


# READ DATA FROM DATA BASE AND INITIALIZE SERIALIZERS
def read_data(
        con: sqlite3.Connection,
        country_list: List,
        state_list: List,
        county_list: List,
        city_list: List,
        county_to_city_list: List,
        unit_list: List,
        building_area_list: List,
        house_list: List,
        status_list: List,
        home_type_list: List,
        sale_announcement_list: List,
) -> None:
    """Read all data from import table and initialize the right serializer.
    Store all initialized serializers in the right list.

    Parameters
    ----------
    con : sqlite3.Connection
        connection to sql database
    country_list : List
    state_list : List
    county_list : List
    city_list : List
    county_to_city_list : List
    unit_list : List
    building_area_list : List
    house_list : List
    status_list : List
    home_type_list : List
    sale_announcement_list : List
    """
    cursor = con.cursor()

    for row in cursor.execute('''select distinct country, currency from import_data'''):
        country_list.append(Country(row[0], row[1]))

    for row in cursor.execute("""select distinct state, country from import_data"""):
        state_list.append(State(row[0], row[1]))

    for row in cursor.execute("""select distinct city, state from import_data"""):
        city_list.append(City(row[0], row[1]))

    for row in cursor.execute("""select distinct county, state from import_data"""):
        county_list.append(County(row[0], row[1]))

    for row in cursor.execute("""select distinct county, city from import_data"""):
        county_to_city_list.append(CountyToCity(row[0], row[1]))

    for row in cursor.execute("""select distinct lotAreaUnits from import_data"""):
        unit_list.append(Unit(row[0]))

    for row in cursor.execute(
            """select distinct buildingArea, livingArea, livingAreaValue, lotAreaUnits from import_data"""):
        building_area_list.append(BuildingArea(row[0], row[1], row[2], row[3]))

    for row in cursor.execute(
            """select 
                longitude, 
                latitude, 
                yearBuilt, 
                bathrooms, 
                hasBadGeocode, 
                bedrooms, 
                parking, 
                garageSpaces, 
                hasGarage, 
                levels, 
                pool, 
                spa, 
                zipcode, 
                streetAddress, 
                county,
                city,
                buildingArea, 
                livingArea, 
                livingAreaValue, 
                lotAreaUnits 
                from import_data"""):
        house_list.append(House(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]))

    for row in cursor.execute("""select distinct event from import_data"""):
        status_list.append(Status(row[0]))

    for row in cursor.execute("""select distinct homeType from import_data"""):
        home_type_list.append(Status(row[0]))

    for row in cursor.execute("""select distinct 
    id,
    datePostedString, 
    price, 
    is_forAuction, 
    pricePerSquareFoot,
    description,
    is_bankOwned,
    isNewConstruction,
    hasPetsAllowed,
    event,
    homeType,
    latitude,
    longitude
    from import_data"""):
        sale_announcement_list.append(SaleAnnouncement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                       row[8], row[9], row[10], row[11], row[12]))

    con.commit()


# WRITE ALL DATA FROM SERIALIZERS TO DATABASE
def import_data(
        con: sqlite3.Connection,
        country_list: List[Country],
        state_list: List[State],
        county_list: List[County],
        city_list: List[City],
        county_to_city_list: List[CountyToCity],
        unit_list: List[Unit],
        building_area_list: List[BuildingArea],
        house_list: List[House],
        status_list: List[Status],
        home_type_list: List[HomeType],
        sale_announcement_list: List[SaleAnnouncement],
) -> None:
    """Write data stored in serializer list to database.

    Parameters
    ----------
    con : sqlite3.Connection
        connection to the database
    country_list : List[Country]
        List of serialized countries
    state_list : List[State]
        List of serialized states
    county_list : List[County]
        List of serialized counties
    city_list : List[City]
        List of serialized cities
    county_to_city_list : List[CountyToCity]
        List of serialized counties to cities
    unit_list : List[Unit]
        List of serialized units
    building_area_list : List[BuildingArea]
        List of serialized building areas
    house_list : List[House]
        List of serialized houses
    status_list : List[Status]
        List of serialized statuses
    home_type_list : List[HomeType]
        List of serialized home types
    sale_announcement_list : List[SaleAnnouncement]
        List of serialized sale announcements
    """
    cursor = con.cursor()

    # write serialized data to database
    # use null as first statement, since the first value to insert should be the dataset id. SQL will set the id for us.
    for entry in country_list:
        cursor.execute(f"""insert into Country values (null, '{entry.name}','{entry.currency}')""")

    for entry in state_list:
        cursor.execute(f"""insert into State values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    for entry in city_list:
        cursor.execute(f"""insert into City values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    for entry in county_list:
        cursor.execute(f"""insert into County values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    # create many to many connection from city to county and vis a versa.
    # A city can have more than one county and a county can have more than one city
    for entry in county_to_city_list:
        cursor.execute(f"""insert into County_to_City values (null, '{entry.get_city_id(con)}',
        '{entry.get_county_id(con)}')""")

    for entry in unit_list:
        cursor.execute(f"""insert into Unit values (null, '{entry.name}')""")

    for entry in building_area_list:
        cursor.execute(f"""insert into Building_Area values (null, {entry.living_area}, {entry.living_area_value}, 
        {entry.get_parent_id(con)}, {entry.building_area_int})""")

    for entry in house_list:
        cursor.execute(f"""insert into House values (null, '{entry.street_name}', {entry.get_county_to_city_id(con)}, 
        {entry.longitude}, {entry.latitude}, {entry.year_build}, {entry.bathroom}, {entry.has_bad_geocode}, 
        {entry.bedroom}, {entry.parking}, {entry.garage_space}, {entry.has_garage}, '{entry.levels}', {entry.pool}, 
        {entry.spa}, {entry.get_building_area_id(con)}, {entry.zip_code})""")

    for entry in status_list:
        cursor.execute(f"""insert into Status values (null, '{entry.name}')""")

    for entry in home_type_list:
        cursor.execute(f"""insert into Home_Type values (null, '{entry.name}')""")

    for entry in sale_announcement_list:
        cursor.execute(f"""insert into Sale_Announcement values (null, {entry.get_house_id(con)}, 
        {entry.get_status_id(con)}, '{entry.date_posted}', {entry.price}, {entry.is_for_auction}, 
        {entry.price_per_square}, '{entry.description}', {entry.bank_owned}, {entry.new_build}, {entry.pets},
        {entry.get_home_type_id(con)}, '{entry.announcement_id}')""")

    # commit the insert changes on the database
    con.commit()


if __name__ == '__main__':

    # make sure, this script is only executed when the user is certain to do so
    sure = input('are you sure to execute this script? [yes/No]: ')
    if not sure == 'yes':
        print('aborting script')
        exit(0)

    # create connection to database
    connection = sqlite3.connect('../project_data.sqlite')

    # initialize empty arrays for storing serializers in it
    countries = []
    states = []
    counties = []
    cities = []
    counties_to_cities = []
    units = []
    building_area = []
    houses = []
    status = []
    home_types = []
    sale_announcements = []

    # call the actual functions to let the script work
    delete_data(connection)
    read_data(connection, countries, states, counties, cities, counties_to_cities, units, building_area, houses, status,
              home_types, sale_announcements)
    import_data(connection, countries, states, counties, cities, counties_to_cities, units, building_area, houses,
                status, home_types, sale_announcements)

    # close connection
    connection.close()
