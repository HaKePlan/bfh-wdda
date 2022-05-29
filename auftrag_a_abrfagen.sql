-- WDDA – Semesterarbeit: Teil a
-- Frage 1:
-- A)
drop view view_California_real_estate;

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
       S2.state_name as state,
       H.year_build as yearBuilt,
       H.street_name as streetAddress,
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
    inner join County_to_City CtC on CtC.id = H.county_to_city_id
    inner join County C on CtC.county_id = C.id
    inner join City C2 on CtC.city_id = C2.id
    inner join State S2 on C.state_id = S2.id
    inner join Country C3 on C3.id = S2.country_id;

-- B)
SELECT COUNT(*) AS anzahl FROM "view_California_real_estate";

-- C)
SELECT DISTINCT * FROM "view_California_real_estate" WHERE city = 'Bell Gardens';

-- Frage 2:
SELECT COUNT (year_build) AS anzahl_immobilien2020 FROM House WHERE House.year_build > 2020;


-- Frage 3:
SELECT city_name, count as imos_in_num_county
    FROM (SELECT *, count(*) AS count FROM County_to_City GROUP BY city_id)
    INNER JOIN City ON city_id = City.id
    WHERE count > 1
    ORDER BY count DESC;


-- Frage 4:
SELECT city, ROUND (AVG(price),2) as RealEstate_price
FROM RealEstate_California
GROUP BY city
ORDER BY RealEstate_price DESC;





-- Frage 5:

SELECT city, ROUND (AVG(pricePerSquareFoot),2) as Average_per_SquareFoot

FROM RealEstate_California

GROUP BY city

ORDER BY Average_per_SquareFoot DESC



-- Frage 6:

SELECT homeType, price, description FROM RealEstate_California WHERE city = “Parlier”