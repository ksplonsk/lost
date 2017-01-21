CREATE TABLE products (
product_pk int,
vendor varchar(255),
description varchar(255),
alt_description varchar(255)
);

CREATE TABLE assets (
asset_pk int,
product_fk int,
asset_tag varchar(255),
description varchar(255),
alt_description varchar(255)
);

CREATE TABLE vehicles (
vehicle_pk int,
asset_fk int
);

CREATE TABLE facilities (
facility_pk int,
fcode varchar(255),
common_name varchar(255),
location varchar(255)
);

CREATE TABLE asset_at (
asset_fk int,
facility_fk int,
arrive_dt int,
depart_dt int
);
