CREATE TABLE hero (
	id_hero SERIAL PRIMARY KEY, 
	heroName varchar(15) NOT NULL, 
	age smallint NOT NULL,
    heroMoney NUMERIC(9, 2) DEFAULT 0
);

INSERT INTO hero(heroName, age, heroMoney) VALUES ('George', 20, 56.0), ('Kirill', 20, 56.2);
