-- Members of Parliament
CREATE TABLE IF NOT EXISTS MPs (
    mp_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(20), 
    given_names VARCHAR(50), 
    last_name VARCHAR(30), 
    party VARCHAR(4), 
    minister TINYINT(1), 
    phone_number VARCHAR(13), 
    email VARCHAR(40), 
    occupation VARCHAR(100), 
    year_of_birth INT(4), 
    place_of_birth VARCHAR(50), 
    place_of_residence VARCHAR(50), 
    constituency VARCHAR(50)
);

-- Interests (sidonnaisuudet)
CREATE TABLE IF NOT EXISTS Interests (
    mp_id INT, 
    category TEXT, 
    interest TEXT
);