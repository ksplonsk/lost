CREATE TABLE roles (
role_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
title varchar(32) -- length of 16 characters specified in project specs
);

INSERT INTO roles (title) VALUES ('Logistics Officer');
INSERT INTO roles (title) VALUES ('Facilities Officer');

CREATE TABLE users (
user_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
role_fk integer REFERENCES roles(role_pk) not null, -- connects roles to users
username varchar(16), -- length of 16 characters specified in project specs
password varchar(16) -- length of 16 characters specified in project specs
);

CREATE TABLE assets (
asset_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
facility_fk integer REFERENCES facilities(facility_pk), -- connects facilities assets
asset_tag varchar(16), -- tag for the asset
description varchar(255) -- description of the asset
);

CREATE TABLE facilities (
facility_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
fcode varchar(6), -- facility code
common_name varchar(32), -- common name for the facility
location varchar(255) -- location of the facility
);




