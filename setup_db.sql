-- Create and use the database
CREATE DATABASE IF NOT EXISTS bms;
USE bms;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    userFullname VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    address VARCHAR(255),
    vip_pass TINYINT(1) DEFAULT 0
);

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(150),
    author VARCHAR(100),
    genre VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    published_date DATE,
    publisher VARCHAR(100),
    rating DECIMAL(3,1)
);

-- Cart table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),
    book_id INT,
    bookname VARCHAR(150),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10,2),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    status VARCHAR(50),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Default admin account (username: admin, password: admin123)
INSERT IGNORE INTO admin (username, password) VALUES ('admin', 'admin123');

-- Sample books
INSERT IGNORE INTO books (isbn, title, author, genre, price, stock_quantity, published_date, publisher, rating) VALUES
('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 299.00, 10, '1960-07-11', 'J.B. Lippincott', 4.8),
('978-0-7432-7356-5', '1984', 'George Orwell', 'Fiction', 249.00, 15, '1949-06-08', 'Secker & Warburg', 4.7),
('978-0-14-028329-7', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 199.00, 8, '1925-04-10', 'Scribner', 4.5),
('978-0-439-02348-1', 'Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 'Fantasy', 399.00, 20, '1997-06-26', 'Bloomsbury', 4.9),
('978-0-06-093546-9', 'To Kill a Mockingbird', 'Harper Lee', 'Mystery', 279.00, 5, '1960-07-11', 'HarperCollins', 4.6),
('978-0-385-33348-1', 'The Da Vinci Code', 'Dan Brown', 'Mystery', 349.00, 12, '2003-03-18', 'Doubleday', 4.3),
('978-0-7432-7357-2', 'A Brief History of Time', 'Stephen Hawking', 'Science Fiction', 299.00, 7, '1988-04-01', 'Bantam Books', 4.7),
('978-1-5011-6922-2', 'Sapiens', 'Yuval Noah Harari', 'History', 499.00, 18, '2011-01-01', 'Harper', 4.8);
