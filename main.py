import curses
import datetime
import sqlite3

from typing import Any, List


class TableMethods:
    def __init__(self, child: Any, parent: str, parent_table_name: str, field_name: str):
        self.parent_name = parent
        self.child_name = child
        self.parent_table = parent_table_name
        self.field = field_name

    def get_parent_id(self, con: sqlite3.Connection) -> int:
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from {self.parent_table} where {self.field} = '{self.parent_name}'"""):
            _id = row[0]

        return int(_id)


class Country:
    def __init__(self, country_name: str, currency: str) -> None:
        self.name = country_name
        self.currency = currency


class Unit:
    def __init__(self, name: str) -> None:
        self.name = name


class State(TableMethods):
    def __init__(self, state_name: str, country_name: str) -> None:
        parent_table = 'Country'
        table_field = 'country_name'
        super().__init__(state_name, country_name, parent_table, table_field)


class City(TableMethods):
    def __init__(self, city_name: str, state_name: str) -> None:
        parent_table = 'State'
        table_field = 'state_name'
        super().__init__(city_name, state_name, parent_table, table_field)


class County(TableMethods):
    def __init__(self, county_name: str, city_name: str) -> None:
        parent_table = 'City'
        table_field = 'city_name'
        super().__init__(county_name, city_name, parent_table, table_field)


class Street(TableMethods):
    def __init__(self, street_name: str, county_name: str) -> None:
        parent_table = 'County'
        table_field = 'county_name'
        super().__init__(street_name, county_name, parent_table, table_field)


class BuildingArea(TableMethods):
    def __init__(self, building_area_int: int, living_area: int, living_area_value: int, unit_name: str) -> None:
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
            building_area_int: int,
            living_area: int,
            living_area_value: int,
            unit_name: str,
    ):
        self.parent_street_name = street_name
        self.parent_county_name = county_name

        self.building_area_int = building_area_int
        self.living_area_value = living_area_value
        self.living_area = living_area
        self.unit_name = unit_name

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

    def get_street_id(self, con: sqlite3.Connection):
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from Street where name = '{self.parent_street_name}'"""):
            _id = row[0]

        return int(_id)

    def get_county_id(self, con: sqlite3.Connection):
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from County where county_name = '{self.parent_county_name}'"""):
            _id = row[0]

        return int(_id)

    def get_building_area_id(self, con: sqlite3.Connection):
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
        self.name = status_name if status_name else 'null'


class HomeType:
    def __init__(self, type_name: str):
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

    def get_status_id(self, con: sqlite3.Connection):
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from Status where status_name = '{self.status_name}'"""):
            _id = row[0]
        return int(_id)

    def get_home_type_id(self, con: sqlite3.Connection):
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from Home_Type where home_type_name = '{self.home_type_name}'"""):
            _id = row[0]
        return int(_id)

    def get_house_id(self, con: sqlite3.Connection):
        cursor = con.cursor()
        _id = ''
        for row in cursor.execute(f"""select id from House where latitude = {self.house_lat} and longitude = '{self.house_long}'"""):
            _id = row[0]
        return int(_id)


def delete_data(con):
    # Prepare db for execution
    cursor = con.cursor()

    tables = ['House', 'Country', 'State', 'City', 'County', 'Status', 'Sale_Announcement', 'Unit', 'Building_Area',
              'Street', 'Home_Type']

    for table in tables:
        cursor.execute(f"""delete from {table}""")
        con.commit()


def read_data(
        con,
        country_list: List,
        state_list: List,
        county_list: List,
        city_list: List,
        street_list: List,
        unit_list: List,
        building_area_list: List,
        house_list: List,
        status_list: List,
        home_type_list: List,
        sale_announcement_list: List,
) -> None:
    cursor = con.cursor()

    for row in cursor.execute('''select distinct country, currency from import_data'''):
        country_list.append(Country(row[0], row[1]))

    for row in cursor.execute("""select distinct state, country from import_data"""):
        state_list.append(State(row[0], row[1]))

    for row in cursor.execute("""select distinct city, state from import_data"""):
        city_list.append(City(row[0], row[1]))

    for row in cursor.execute("""select distinct county, city from import_data"""):
        county_list.append(County(row[0], row[1]))

    for row in cursor.execute("""select distinct streetAddress, county from import_data"""):
        street_list.append(Street(row[0], row[1]))

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
                buildingArea, 
                livingArea, 
                livingAreaValue, 
                lotAreaUnits 
                from import_data"""):
        house_list.append(House(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]))

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


def import_data(
        con: sqlite3.Connection,
        country_list: List[Country],
        state_list: List[State],
        county_list: List[County],
        city_list: List[City],
        street_list: List[Street],
        unit_list: List[Unit],
        building_area_list: List[BuildingArea],
        house_list: List[House],
        status_list: List[Status],
        home_type_list: List[HomeType],
        sale_announcement_list: List[SaleAnnouncement],
) -> None:
    cursor = con.cursor()

    for entry in country_list:
        cursor.execute(f"""insert into Country values (null, '{entry.name}','{entry.currency}')""")

    con.commit()

    for entry in state_list:
        cursor.execute(f"""insert into State values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    con.commit()

    for entry in city_list:
        cursor.execute(f"""insert into City values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    con.commit()

    for entry in county_list:
        cursor.execute(f"""insert into County values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    con.commit()

    for entry in street_list:
        cursor.execute(f"""insert into Street values (null, '{entry.child_name}', {entry.get_parent_id(con)})""")

    con.commit()

    for entry in unit_list:
        cursor.execute(f"""insert into Unit values (null, '{entry.name}')""")

    con.commit()

    for entry in building_area_list:
        cursor.execute(f"""insert into Building_Area values (null, {entry.living_area}, {entry.living_area_value}, {entry.get_parent_id(con)}, {entry.building_area_int})""")

    con.commit()

    for entry in house_list:
        cursor.execute(f"""insert into House values (null, {entry.get_street_id(con)}, {entry.get_county_id(con)}, 
        {entry.longitude}, {entry.latitude}, {entry.year_build}, {entry.bathroom}, {entry.has_bad_geocode}, 
        {entry.bedroom}, {entry.parking}, {entry.garage_space}, {entry.has_garage}, '{entry.levels}', {entry.pool}, 
        {entry.spa}, {entry.get_building_area_id(con)}, {entry.zip_code})""")

    con.commit()

    for entry in status_list:
        cursor.execute(f"""insert into Status values (null, '{entry.name}')""")

    con.commit()

    for entry in home_type_list:
        cursor.execute(f"""insert into Home_Type values (null, '{entry.name}')""")

    con.commit()

    # TODO: check date posted (only year is saved)
    for entry in sale_announcement_list:
        cursor.execute(f"""insert into Sale_Announcement values (null, {entry.get_house_id(con)}, {entry.get_status_id(con)}, 
        {entry.date_posted}, {entry.price}, {entry.is_for_auction}, {entry.price_per_square}, '{entry.description}', 
        {entry.bank_owned}, {entry.new_build}, {entry.pets}, {entry.get_home_type_id(con)}, {entry.announcement_id})""")

    con.commit()


if __name__ == '__main__':
    connection = sqlite3.connect('./project_data.sqlite')

    countries = []
    states = []
    counties = []
    cities = []
    streets = []
    units = []
    building_area = []
    houses = []
    status = []
    home_types = []
    sale_announcements = []

    delete_data(connection)
    read_data(connection, countries, states, counties, cities, streets, units, building_area, houses, status, home_types, sale_announcements)
    import_data(connection, countries, states, counties, cities, streets, units, building_area, houses, status, home_types, sale_announcements)

    connection.close()
