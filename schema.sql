
USE campuseats_graphql;

CREATE TABLE IF NOT EXISTS dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO dishes (name, price, available) VALUES
('Veg Burger', 60.00, TRUE),
('Paneer Roll', 90.00, TRUE),
('Masala Dosa', 70.00, TRUE),
('French Fries', 50.00, FALSE);
