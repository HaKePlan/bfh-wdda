PRAGMA FOREIGN_KEY_CHECKS = OFF;
DROP TABLE IF EXISTS `House`;
DROP TABLE IF EXISTS `Country`;
DROP TABLE IF EXISTS `State`;
DROP TABLE IF EXISTS `County`;
DROP TABLE IF EXISTS `City`;
DROP TABLE IF EXISTS `Status`;
DROP TABLE IF EXISTS `Sale_Announcement`;
DROP TABLE IF EXISTS `Unit`;
DROP TABLE IF EXISTS `Building_Area`;
DROP TABLE IF EXISTS `Street`;
DROP TABLE IF EXISTS `Home_Type`;
PRAGMA FOREIGN_KEY_CHECKS = OFF;

CREATE TABLE `House` (
    `id` INTEGER NOT NULL,
    `street_id` INTEGER NOT NULL,
    `county_id` INTEGER NOT NULL,
    `longitude` FLOAT NOT NULL,
    `latitude` FLOAT NOT NULL,
    `year_build` INTEGER,
    `statusID` INTEGER NOT NULL,
    `bathroom` INTEGER NOT NULL,
    `has_bad_geocode` BOOLEAN NOT NULL,
    `bedroom` INTEGER NOT NULL,
    `parking` BOOLEAN NOT NULL,
    `garage_space` INTEGER NOT NULL,
    `has_garage` BOOLEAN NOT NULL,
    `levels` VARCHAR(20) NOT NULL,
    `pool` BOOLEAN NOT NULL,
    `spa` BOOLEAN NOT NULL,
    `building_area_id` INTEGER NOT NULL,
    `zip_code` INTEGER,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`street_id`) references `Street` (`id`),
    FOREIGN KEY (`county_id`) references `County` (`id`),
    FOREIGN KEY (`building_area_id`) references `Building_Area` (`id`)
);

CREATE TABLE `Country` (
    `id` INTEGER NOT NULL,
    `country_name` VARCHAR(20) NOT NULL,
    `currency` CHAR(3) NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    UNIQUE (`country_name`, `currency`)
);

CREATE TABLE `State` (
    `id` INTEGER NOT NULL,
    `state_name` VARCHAR(20) NOT NULL,
    `country_id` INTEGER NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`country_id`) references `Country` (`id`),
    UNIQUE (`state_name`)
);

CREATE TABLE `County` (
    `id` INTEGER NOT NULL,
    `county_name` VARCHAR(20) NOT NULL,
    `city_id` INTEGER NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`city_id`) references `City` (`id`)
);

CREATE TABLE `City` (
    `id` INTEGER NOT NULL,
    `city_name` VARCHAR(20) NOT NULL,
    `state_id` INTEGER NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`state_id`) references `State` (`id`)
);

CREATE TABLE `Status` (
    `id` INTEGER NOT NULL,
    `status_name` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    UNIQUE (`status_name`)
);

CREATE TABLE `Sale_Announcement` (
    `id` INTEGER NOT NULL,
    `house_id` INTEGER NOT NULL,
    `status_id` INTEGER NOT NULL,
    `date_posted` DATE,
    `price` INTEGER NOT NULL,
    `is_for_auction` BOOLEAN NOT NULL,
    `price_per_square` INTEGER,
    `description` VARCHAR(500),
    `is_bank_own` BOOLEAN NOT NULL,
    `is_new_construction` BOOLEAN NOT NULL,
    `has_pets_allowed` BOOLEAN NOT NULL,
    `home_type_id` INTEGER NOT NULL,
    `export_number` VARCHAR(30),
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`house_id`) references `House` (`id`),
    FOREIGN KEY (`status_id`) references `Status` (`id`),
    FOREIGN KEY (`home_type_id`) references `Home_Type` (`id`)
);

CREATE TABLE `Unit` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    UNIQUE (`name`)
);

CREATE TABLE `Building_Area` (
    `id` INTEGER NOT NULL,
    `living_area` INTEGER NOT NULL,
    `living_area_value` INTEGER NOT NULL,
    `unit_id` INTEGER NOT NULL,
    `building_area` INTEGER NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`unit_id`) references `Unit` (`id`)
);

CREATE TABLE `Street` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `county_id` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    FOREIGN KEY (`county_id`) references `County` (`id`)
);

CREATE TABLE `Home_Type` (
    `id` INTEGER NOT NULL,
    `home_type_name` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id` AUTOINCREMENT),
    UNIQUE (`home_type_name`)
);
