# 📚 Fiction Fusion – Bookstore Management System

## 🚀 Overview

Fiction Fusion is a **CLI-based Bookstore Management System** built using Python and MySQL.
It supports **Admin and User roles** and simulates real-world bookstore operations like inventory management, cart handling, payments, and sales analytics.

---

## 🎯 Features

### 👨‍💼 Admin

* Add, update, and remove books
* View all books and filter by genre
* Manage users and VIP access
* View sales reports (charts using Matplotlib)

### 👤 User

* User signup & login with validation
* Browse books (title, author, genre)
* Search books by ISBN
* Sort books by rating

### 🛒 Cart & Orders

* Add/remove books from cart
* View cart details
* Automatic stock updates
* Order processing system

### 💳 Payment System

* Cash on Delivery
* UPI Payment
* Debit Card Payment

### 🧾 Billing

* View bill in console
* Generate bill as `.txt` file

### 📊 Data Visualization

* Sales report (Admin)
* Purchase history (User)

---

## 🛠️ Tech Stack

* Python 🐍
* MySQL 🗄️
* Matplotlib 📊
* Regex (Validation)

---

## 🗄️ Database

Database Name: `bms`

Tables:

* admin
* users
* books
* cart
* orders
* payments

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/NazzzShaikh/Fiction-Fusion-Bookstore-Management-System.git
cd Fiction-Fusion-Bookstore-Management-System
```

### 2. Install dependencies

```bash
pip install mysql-connector-python matplotlib
```

### 3. Setup Database

* Create database `bms`
* Run your SQL setup file

Default Admin:

* Username: `admin`
* Password: `admin123`

---

### 4. Configure Database

Update credentials in `main.py`:

```python
self.host = "127.0.0.1"
self.user = "root"
self.password = ""
self.database = "bms"
```

---

### 5. Run the project

```bash
python main.py
```

---

## 📂 Project Structure

```
📁 Fiction-Fusion
│── main.py
│── admin.py
│── user.py
│── extra.py
│── db.sql
```

---

## 🔐 Validation

* Name → Alphabets only
* Password → Min 8 chars + special character
* Email → Valid format
* Phone → 10 digits

---

## 💡 Future Improvements

* Convert to Web App (Django/React)
* Add JWT Authentication
* Payment Gateway Integration
* Recommendation System

---

## 👩‍💻 Author

Naznin Shaikh (Nezuko)
