CREATE TABLE users (
user_pk serial primary key, -- chose to use a numeric pk, I am more comfortable using numeric pk's
username varchar(16), -- length of 16 characters specified in project specs
password varchar(16) -- length of 16 characters specified in project specs
);
