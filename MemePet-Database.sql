--postgreSQL for MemePet project.

CREATE TABLE UserAccount(
user_id serial PRIMARY KEY,
username VARCHAR(20) UNIQUE NOT NULL,
password VARCHAR(50) NOT NULL,
email VARCHAR(355),
created_on TIMESTAMP NOT NULL,
last_login TIMESTAMP
);

CREATE TABLE PetModel(
pet_id serial PRIMARY KEY,
pet_name VARCHAR(20) UNIQUE NOT NULL,
import_on TIMESTAMP NOT NULL,
);

CREATE TABLE HavePet(
user_id integer NOT NULL,
pet_id integer Not NULL,
PRIMARY KEY(user_id, pet_id),
FOREIGN KEY(pet_id) REFERENCES petModel(pet_id) ON DELETE CASCADE,
FOREIGN KEY(user_id) REFERENCES userAccount(user_id) ON DELETE CASCADE
);

CREATE TABLE Location(
user_id integer PRIMARY KEY,
latitude numeric(9,6),
longitude numeric(9,6),
FOREIGN KEY(user_id) REFERENCES userAccount(user_id) ON DELETE CASCADE
);