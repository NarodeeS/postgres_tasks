CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

INSERT INTO books(name) VALUES ('postgres to the top');
INSERT INTO books(name) VALUES ('mongo to the bottom');
