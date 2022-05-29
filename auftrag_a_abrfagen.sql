-- WDDA – Semesterarbeit: Teil a
-- Frage 1:
-- A)
CREATE VIEW "view_California_real_estate" AS
select Sale_Announcement.export_number as id,
       C3.country_name as country,
       Sale_Announcement.date_posted as datePostedString,
       Sale_Announcement.is_bank_own as is_bankOwned,
       Sale_Announcement.is_for_auction as is_forAuction,
       S.status_name as event,
       Sale_Announcement.price as price,
       Sale_Announcement.price_per_square as pricePerSquareFoot,
       C2.city_name as city,
       S3.state_name as state,
       H.year_build as yearBuilt,
       S2.name as streetAddress,
       H.zip_code as zipcode,
       H.longitude as longitude,
       H.latitude as latitude,
       H.has_bad_geocode as hasBadGeocode,
       Sale_Announcement.description as description,
       C3.currency as currency,
       BA.living_area as livingArea,
       BA.living_area_value as livingAreaValue,
       U.name as lotAreaUnits,
       H.bathroom as bathrooms,
       H.bedroom as bedrooms,
       BA.building_area as buildingArea,
       H.parking as parking,
       H.garage_space as garageSpace,
       H.has_garage as hasGarage,
       H.levels as levels,
       H.pool as pool,
       H.spa as spa,
       Sale_Announcement.is_new_construction as isNewConstruction,
       Sale_Announcement.has_pets_allowed as hasPetsAllowed,
       HT.home_type_name as homeType,
       C.county_name as county
    from Sale_Announcement
    inner join Status S on S.id = Sale_Announcement.status_id
    inner join Home_Type HT on HT.id = Sale_Announcement.home_type_id
    inner join House H on H.id = Sale_Announcement.house_id
    inner join Building_Area BA on BA.id = H.building_area_id
    inner join Unit U on BA.unit_id = U.id
    inner join Street S2 on S2.id = H.street_id
    inner join County C on C.id = H.county_id
    inner join City C2 on C2.id = C.city_id
    inner join State S3 on S3.id = C2.state_id
    inner join Country C3 on C3.id = S3.country_id;

drop view view_California_real_estate;

-- B)
SELECT COUNT(*) AS anzahl FROM "view_California_real_estate";

-- C)
SELECT DISTINCT * FROM "view_California_real_estate" WHERE city = 'Bell Gardens';

-- Frage 2:
SELECT COUNT (year_build) AS anzahl_immobilien2020 FROM House WHERE House.year_build > 2020;


-- Frage 3:
select distinct county, city from import_data order by city;

select city_name, county_name from City inner join County C on C.id = City.county_id order by city_name;



-- Frage 4:
SELECT city, ROUND (AVG(price),2) as RealEstate_price

FROM RealEstate_California

GROUP BY city

ORDER BY RealEstate_price DESC



-- Frage 5:

SELECT city, ROUND (AVG(pricePerSquareFoot),2) as Average_per_SquareFoot

FROM RealEstate_California

GROUP BY city

ORDER BY Average_per_SquareFoot DESC



-- Frage 6:

SELECT homeType, price, description FROM RealEstate_California WHERE city = “Parlier”