CREATE TABLE roles (
role_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
title varchar(32) -- title of role
);

INSERT INTO roles (title) VALUES ('Logistics Officer');
INSERT INTO roles (title) VALUES ('Facilities Officer');

CREATE TABLE users (
user_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
role_fk integer REFERENCES roles(role_pk) not null, -- connects roles to users
username varchar(16), -- length of 16 characters specified in project specs
password varchar(16) -- length of 16 characters specified in project specs
);

CREATE TABLE facilities (
facility_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
fcode varchar(6), -- facility code
common_name varchar(32), -- common name for the facility
location varchar(255) -- location of the facility
);

CREATE TABLE assets (
asset_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
asset_tag varchar(16), -- tag for the asset
description text, -- description of the asset
disposed boolean default false -- shows if asset is disposed or not
);

CREATE TABLE asset_at (
asset_fk integer REFERENCES assets (asset_pk) not null, -- connects assets to asset_at
facility_fk integer REFERENCES facilities (facility_pk) not null, -- connects facilities to asset_at
arrival timestamp default null, -- arrival time of asset
departure timestamp default null -- departure time of asset
);

CREATE TABLE transfers (
transfer_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
requester_fk integer REFERENCES users (user_pk) not null, -- connects user that is reqquester to transfers
request_dt timestamp, -- time of request made
source_fk integer REFERENCES facilities (facility_pk) not null, -- connects source facility to transfers
destination_fk integer REFERENCES facilities (facility_pk) not null, -- connects destination facility to transfers
asset_fk integer REFERENCES assets (asset_pk) not null, -- connects assets to transfers
approver_fk integer REFERENCES users (user_pk) default null, -- connects user that is approver to transfers
approved_dt timestamp default null -- time of request approved
);

CREATE TABLE in_transit (
transfer_fk integer REFERENCES transfers (transfer_pk) not null, -- connects transfers to in_transit
load_dt timestamp, -- time of loading
unload_dt timestamp -- time of unloading
);




