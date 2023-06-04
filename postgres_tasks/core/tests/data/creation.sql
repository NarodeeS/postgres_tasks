CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255),
    order_date DATE,
    total_amount NUMERIC
);
