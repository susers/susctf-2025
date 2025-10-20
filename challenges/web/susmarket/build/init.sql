CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    stock INT NOT NULL,
    description TEXT
);

INSERT INTO products (product_name, price, stock, description) VALUES
('Laptop', 999.99, 5, 'A simple laptop'),
('Smartphone', 599.99, 10, 'oPhone 114514'),
('Headphones', 199.99, 20, 'Siny WH1000-XM9'),
('Gaming Mouse', 49.99, 15, 'Legotech G403'),
('Mechanical Keyboard', 129.99, 7, 'KBHH Keyboard'),
('SUSCTF flag', 1919.81, 0, 'susctf{L0L_7ry_hard3r}');
