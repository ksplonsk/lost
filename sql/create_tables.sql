CREATE TABLE users (
-- chose to use a numeric pk, I am more comfortable using numeric pk's
user_pk serial primary key,

-- length of 16 characters specified in project specs
username varchar(16),

-- length of 16 characters specified in project specs
password varchar(16), 
);
