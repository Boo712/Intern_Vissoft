CREATE DATABASE IF NOT EXISTS pokemon;

USE pokemon;

CREATE TABLE pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    type1 VARCHAR(50),
    type2 VARCHAR(50),
    total INT,
    hp INT,
    attack INT,
    defense INT,
    sp_atk INT,
    sp_def INT,
    speed INT,
    generation INT,
    legendary BOOLEAN
);

LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\pokemon.csv' 
INTO TABLE pokemon
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, @legendary)
SET legendary = IF(@legendary = 'TRUE', TRUE, IF(@legendary = 'FALSE', FALSE, NULL));

SELECT * FROM pokemon;
