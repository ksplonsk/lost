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
arrive_dt timestamp,
depart_dt timestamp
);

CREATE TABLE convoys (
convoy_pk int,
request varchar(255),
source_fk int,
dest_fk int,
depart_dt timestamp, 
arrive_dt timestamp 
);

CREATE TABLE used_by (
vehicle_fk int,
convoy_fk int
);

CREATE TABLE asset_on (
asset_fk int,
convoy_fk int,
load_dt timestamp, 
unload_dt timestamp 
);

CREATE TABLE users (
user_pk int,
username varchar(255),
active boolean
);

CREATE TABLE roles (
role_pk int,
title varchar(255)
);

CREATE TABLE user_is (
user_fk int,
role_fk int
);

CREATE TABLE user_supports (
user_fk int,
facility_fk int
);

CREATE TABLE level (
level_pk int,
abbrv varchar(255),
comment varchar(255)
);

CREATE TABLE compartments (
compartment_pk int,
abbrv varchar(255),
comment varchar(255)
);

CREATE TABLE security_tags (
tag_pk int,
level_fk int,
compartment_fk int,
user_fk int,
product_fk int,
asset_fk int
);







