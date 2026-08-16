-- ==========================================
-- ACCOUNT SERVICE
-- Owner: Mahi Verma
-- ==========================================

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20)
);

CREATE TABLE addresses (
    address_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    address_text VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- ==========================================
-- CATALOGUE SERVICE
-- Owner: Abhishek Jadhao
-- ==========================================

CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255),
    status VARCHAR(30) NOT NULL
);

CREATE TABLE menu_items (
    item_id INT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
);


-- ==========================================
-- ORDERS SERVICE
-- Owner: Subham Kumar Mohanty
-- ==========================================

CREATE TABLE carts (
    cart_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    status VARCHAR(30) NOT NULL
);

CREATE TABLE cart_items (
    cart_item_id INT PRIMARY KEY,
    cart_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id)
        REFERENCES carts(cart_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    address_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- ==========================================
-- PAYMENTS & DELIVERY SERVICE
-- Owner: Harsh N Shende
-- ==========================================

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    order_reference INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE refunds (
    refund_id INT PRIMARY KEY,
    transaction_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
);

CREATE TABLE riders (
    rider_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(30) NOT NULL
);

CREATE TABLE assignments (
    assignment_id INT PRIMARY KEY,
    order_reference INT NOT NULL,
    rider_id INT NOT NULL,
    status VARCHAR(30) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id)
        REFERENCES riders(rider_id)
);


-- ==========================================
-- NOTIFICATION SERVICE
-- Owner: Rishabh Mishra
-- ==========================================

CREATE TABLE message_log (
    notification_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(30) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);