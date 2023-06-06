CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255),
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

INSERT INTO orders(customer_name, book_id) VALUES ('ivan', 1);
INSERT INTO orders(customer_name, book_id) VALUES ('george', 2);
INSERT INTO orders(customer_name, book_id) VALUES ('kirill', 2);