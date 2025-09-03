import sys
import mysql.connector
from admin import Admin
from user import User

import re

class DBConnect:
    def __init__(self):
        self.host = "localhost"  
        self.user = "root"  
        self.password = ""  
        self.database = "bms"  

    def connection(self):
        try:
            con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return con
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            sys.exit(1)  # Exit if DB connection fails


def welcome_msg_print():
    print("*********************************************************")
    print("*                                                       *")
    print("*   ╔═══════════════════════════════════════════════╗   *")
    print("*   ║                                               ║   *")
    print("*   ║      Welcome to the Fiction Fusion System !   ║   *")
    print("*   ║                                               ║   *")
    print("*   ╚═══════════════════════════════════════════════╝   *")
    print("*                                                       *")
    print("*********************************************************")
    print()
    print("Explore our vast collection of books and manage your bookstore with ease.")
    print("Please select an option from the menu to get started.")
    print()

def display_main_menu():
    print("""
    -----------------------------------------
        Are you a user or an admin?
        1 --> Admin
        2 --> User
        3 --> Exit
    -----------------------------------------
    """)
    choice = input("Enter your choice: ")
    return choice

def authenticate_admin(con, username, password):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT password FROM admin WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if password == stored_password:
                return True  # Login successful
            else:
                print("Incorrect password. Please try again.")
                return False
        else:
            print("Username not found.")
            return False
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

def admin_login(con):
    print("\n--- Admin Login ---")
    admin_username = input("Enter Admin Username: ")
    admin_password = input("Enter Admin Password: ")

    if authenticate_admin(con, admin_username, admin_password):  
        print("\nLogin successful! Welcome, Admin.")

        admin_instance = Admin(con)  # Create an instance of Admin class
        admin_instance.admin_menu()  # Call the method using the instance

    else:
        print("Invalid Admin credentials. Please try again.")


def main():
    db = DBConnect()
    con = db.connection()

    if con:
        print("Connected to the database")
        welcome_msg_print()

        while True:
            try:
                role_choice = display_main_menu()

                if role_choice == "1":
                    admin_login(con)
                elif role_choice == "2":
                    user_interaction(con)
                elif role_choice == "3":
                    print("Exiting the system...")
                    print("THANK YOU FOR USING SYSTEM")
                    sys.exit()
                else:
                    print("Invalid choice! Please choose either Admin or User.")
            except ValueError:
                print("An error occurred: invalid input. Please enter a number.")
def user_interaction(con):
    while True:
        print("""
        -----------------------------------------
        1 --> Login to existing account
        2 --> Sign up for a new account
        3 --> Back to Main Menu
        -----------------------------------------
        """)
        choice = input("Enter your choice: ")

        if choice == "1":
            user_login(con)
        elif choice == "2":
            user_sign_up(con)
        elif choice == "3":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please try again.")

def user_login(con):
    # conn = get_db_connection()
    cursor = con.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        print("Login successful! Redirecting to user menu...")
        user_instance = User(con,username)  # Create an instance of Admin class
        user_instance.user_menu()  # Call the method using the instance

    else:
        print("Invalid user credentials. Please try again.")
    
    # cursor.close()
    # con.close()

def user_sign_up(con):
    # conn = get_db_connection()
    cursor = con.cursor()

    while True:
        name = input("Enter Your Name (alphabets only): ")
        if is_valid_name(name):
            break

    username = input("Enter a new username: ")

    while True:
        password = input("Enter a new password (at least 8 characters, including a special character): ")
        if is_valid_password(password):
            break

    while True:
        email = input("Enter Your Email (e.g., name@gmail.com): ")
        if is_valid_email(email):
            break

    while True:
        phone_number = input("Enter Your Phone Number (10 digits): ")
        if is_valid_phone_number(phone_number):
            break

    address = input("Enter Your Address: ")

    vip_pass = input("Do you want to apply for VIP pass? (yes/no): ").strip().lower()
    is_vip_pass = 1 if vip_pass == "yes" else 0

    try:
        query = "INSERT INTO users (username, password, userFullname, email, phone_number, address, vip_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, name, email, phone_number, address, is_vip_pass))
        con.commit()
        print("User account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def is_valid_name(name):
    if re.fullmatch(r'^[a-zA-Z\s]+$', name):
        return True
    print("Invalid name. It should only contain alphabets and spaces.")
    return False

def is_valid_password(password):
    if re.fullmatch(r'^(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$', password):
        return True
    print("Invalid password. Must be at least 8 characters long and contain at least one special character.")
    return False

def is_valid_email(email):
    if re.fullmatch(r'^[\w.-]+@[\w-]+\.[a-zA-Z]{2,}$', email):
        return True
    print("Invalid email. Must be in the format name@domain.com.")
    return False

def is_valid_phone_number(phone_number):
    if re.fullmatch(r'^\d{10}$', phone_number):
        return True
    print("Invalid phone number. It must be exactly 10 digits long.")
    return False


if __name__ == "__main__":
    main()
