CREATE TABLE roles (
role_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
title varchar(32) -- length of 16 characters specified in project specs
);

CREATE TABLE users (
user_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
role_fk integer REFERENCES roles(role_pk) not null,
username varchar(16), -- length of 16 characters specified in project specs
password varchar(16) -- length of 16 characters specified in project specs
);

CREATE TABLE assets (
asset_pk serial primary key,
asset_tag varchar(16),
description varchar(255)
);

CREATE TABLE facilities (
facility_pk serial primary key,
fcode varchar(6),
common_name varchar(32),
location varchar(255)
);




