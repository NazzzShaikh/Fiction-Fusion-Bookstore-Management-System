import mysql.connector
import matplotlib.pyplot as plt
from collections import defaultdict

class Admin:
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()

    def admin_menu(self):
        """Displays the Admin menu and handles admin actions."""
                    
        """8 --> View Sales History
        10--> view Sales by Genre self.view_sales_by_genre()
        """
        while True:
            print("""
                            Admin Menu
                ------------------------------------
                    1 --> Add Book
                    2 --> Remove Book
                    3 --> Update Book
                    4 --> View All Books
                    5 --> Display Books by Genre
                    6 --> View all Admins
                    7 --> Manage VIP Pass
                    8 --> Display All Users
                    9 --> View Sales Report
                    10 --> Logout
                -------------------------------------
            """)
            choice = input("Enter Your Choice: ")
            match choice:
                case "1": self.add_book()
                case "2": self.remove_book_by_isbn()
                case "3": self.update_book_by_isbn()
                case "4": self.display_all_books()
                case "5": self.display_books_by_genre()
                case "6": self.view_all_admins()
                case "7": self.manage_vip_pass()
                # case "8": self.view_sales_history()
                case "8": self.display_all_users()
                case "9":self.view_sales_report()
                case "10": break
                case "11": break
                case _: print("Enter Proper Choice")

    def add_book(self):
        """Adds a new book to the database."""
        isbn = input("Enter ISBN: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        genre = input("Enter Genre: ")
        published_date = input("Published Date (yyyy-mm-dd): ")
        publisher = input("Enter Publisher: ")
        price = float(input("Enter Price: "))
        rating = float(input("Enter Rating: "))
        stock = int(input("Enter Quantity: "))

        query = """INSERT INTO books (isbn, title, author, genre, price, stock_quantity, published_date, publisher, rating) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (isbn, title, author, genre, price, stock, published_date, publisher, rating)

        self.cursor.execute(query, values)
        self.con.commit()
        print(" Book added successfully.")

    def remove_book_by_isbn(self):
        """Removes a book from the inventory by ISBN."""
        self.display_all_books()
        ans = input("Do you want to remove any book? (yes/no): ").strip().lower()

        if ans != "yes":
            print("No book removed.")
            print("Returning to Admin Menu.")
            return

        isbn = input("Enter ISBN of the book to be removed: ").strip()

        try:
            delete_query = "DELETE FROM books WHERE isbn = %s"
            self.cursor.execute(delete_query, (isbn,))
            self.con.commit()

            if self.cursor.rowcount > 0:
                print(" Book removed successfully.")
            else:
                print(" No book found with the given ISBN.")

        except mysql.connector.Error as err:
            print(f" Database error: {err}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")

    def update_book_by_isbn(self):
        print("""Updates book details by ISBN.""")
        self.display_all_books()
        ans = input("Do you want to update any book? (yes/no): ").strip().lower()

        if ans != "yes":
            print("No book updated.")
            return

        update_isbn = input("Enter ISBN of the book to update: ").strip()

        try:
            fetch_query = "SELECT price, stock_quantity FROM books WHERE isbn = %s"
            self.cursor.execute(fetch_query, (update_isbn,))
            book = self.cursor.fetchone()

            if book is None:
                print(" Invalid ISBN. Book not found.")
                return

            price, stock_quantity = book  # Extract current price and stock

            new_price_input = input("Enter new price to update (or press Enter to skip): ").strip()
            new_quantity_input = input("Enter new quantity to update (or enter 0 to skip): ").strip()

            # Validate and update price
            if new_price_input:
                try:
                    price = float(new_price_input)
                except ValueError:
                    print(" Invalid price format. Keeping the existing price.")

            # Validate and update stock quantity
            if new_quantity_input:
                try:
                    new_quantity = int(new_quantity_input)
                    if new_quantity > 0:
                        stock_quantity = new_quantity
                except ValueError:
                    print("Invalid quantity format. Keeping the existing quantity.")

            update_query = "UPDATE books SET price = %s, stock_quantity = %s WHERE isbn = %s"
            self.cursor.execute(update_query, (price, stock_quantity, update_isbn))
            self.con.commit()

            if self.cursor.rowcount > 0:
                print(" Book updated successfully.")
            else:
                print(" No changes made.")

        except mysql.connector.Error as err:
            print(f" Database error: {err}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
            
    def display_all_books(self):
        """Displays all books from the database."""
        query = "SELECT isbn, title, author, genre, price, stock_quantity FROM books"
        try:
            self.cursor.execute(query)
            books = self.cursor.fetchall()
            
            if not books:
                print("📚 No books available.")
                return

            print("\n📖 List of Available Books:")
            print("-" * 90)
            print(f"{'ISBN':<15}{'Title':<30}{'Author':<20}{'Genre':<15}{'Price':<10}{'Stock':<6}")
            print("-" * 90)

            for book in books:
                isbn, title, author, genre, price, stock = book
                title = title if title else "N/A"
                author = author if author else "N/A"
                genre = genre if genre else "N/A"
                price = price if price is not None else 0.00
                stock = stock if stock is not None else 0
                
                print(f"{isbn:<15}{title[:28]:<30}{author[:18]:<20}{genre:<15}${price:<9.2f}{stock:<6}")

            print("-" * 90)
            print(f"📚 Total Books: {len(books)}\n")

        except mysql.connector.Error as err:
            print(f"❌ Database error: {err}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")


    def display_books_by_genre(self):
        """Displays books based on the selected genre."""

        print("""
                 Search By Genre
            --------------------------------
                1  --> Fiction
                2  --> Non-Fiction
                3  --> Science Fiction
                4  --> Fantasy
                5  --> Mystery
                6  --> Biography
                7  --> History
                8  --> Romance
                9  --> Back to Admin Menu
            --------------------------------
        """)

        try:
            choice = int(input("Enter choice: ").strip())
        except ValueError:
            print(" Invalid input. Please enter a number.")
            return

        genre_map = {
            1: "Fiction",
            2: "Non-Fiction",
            3: "Science Fiction",
            4: "Fantasy",
            5: "Mystery",
            6: "Biography",
            7: "History",
            8: "Romance"
        }

        if choice == 9:
            print(" Returning to Admin Menu...")
            return
        elif choice not in genre_map:
            print(" Invalid choice. Please try again.")
            return

        genre = genre_map[choice]

        query = "SELECT isbn, title, author, genre, price, stock_quantity FROM books WHERE genre = %s"
        try:
            self.cursor.execute(query, (genre,))
            books = self.cursor.fetchall()

            if not books:
                print(f" No books found in the '{genre}' genre.")
                return

            print("\n Books Available:")
            print("-" * 90)
            print(f"{'ISBN':<15}{'Title':<30}{'Author':<20}{'Genre':<15}{'Price':<10}{'Stock':<6}")
            print("-" * 90)

            for book in books:
                isbn, title, author, book_genre, price, stock = book
                print(f"{isbn:<15}{title[:28]:<30}{author[:18]:<20}{book_genre:<15}${price:<9.2f}{stock:<6}")

            print("-" * 90)
            print(f" Total Books in {genre}: {len(books)}\n")

        except mysql.connector.Error as err:
            print(f" Database error: {err}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")

    def view_all_admins(self):
        # print("""Displays all admin usernames from the database.""")
        query = "SELECT username FROM admin"

        try:
            self.cursor.execute(query)
            admins = self.cursor.fetchall()

            if not admins:
                print(" No admins found in the database.")
                return

            print("\n List of Admins:")
            print("-" * 30)

            for admin in admins:
                print(f" Admin Username: {admin[0]}")
                print("-" * 30)

        except mysql.connector.Error as err:
            print(f" Database error: {err}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
            
    def manage_vip_pass(self):
        # print("""Menu to manage VIP passes.""")
        while True:
            print("""
                 Manage VIP Pass
                -----------------------------------------
                1 --> Add VIP Pass
                2 --> Remove VIP Pass
                3 --> Display VIP Users
                4 --> Back to Admin Menu
                -----------------------------------------
            """)
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_vip_pass()
            elif choice == "2":
                self.remove_vip_pass()
            elif choice == "3":
                self.display_vip_users()
            elif choice == "4":
                print(" Returning to Admin Menu...")
                break
            else:
                print(" Invalid choice. Please enter a valid option.")

    def add_vip_pass(self):
        # print("""Adds a VIP pass to a user.""")
        self.display_all_users()
        ans = input("Do you want to add a VIP pass? (yes/no): ").strip().lower()
        
        if ans == "yes":
            username = input("Enter username: ").strip()
            query = "UPDATE users SET vip_pass = TRUE WHERE username = %s"
            
            self.cursor.execute(query, (username,))
            self.con.commit()

            if self.cursor.rowcount > 0:
                print(" VIP pass added successfully.")
            else:
                print(" User not found or VIP pass already exists.")
        else:
            print(" No VIP pass added.")

    def remove_vip_pass(self):
        # print("""Removes a VIP pass from a user.""")
        self.display_vip_users()
        ans = input("Do you want to remove a VIP pass? (yes/no): ").strip().lower()
        
        if ans == "yes":
            username = input("Enter username: ").strip()
            query = "UPDATE users SET vip_pass = FALSE WHERE username = %s"
            
            self.cursor.execute(query, (username,))
            self.con.commit()

            if self.cursor.rowcount > 0:
                print(" VIP pass removed successfully.")
            else:
                print(" User not found or VIP pass does not exist.")
        else:
            print(" No VIP pass removed.")

    def display_vip_users(self):
        # print("""Displays all users with a VIP pass.""")
        query = "SELECT * FROM users WHERE vip_pass = TRUE"
        self.cursor.execute(query)
        vip_users = self.cursor.fetchall()

        if not vip_users:
            print(" No VIP users found.")
            return
        
        print("\n VIP Users List:")
        print("-" * 100)
        print(f"{'User ID':<10}{'Username':<20}{'Full Name':<25}{'Email':<25}{'Phone':<15}{'VIP Pass':<10}")
        print("-" * 100)

        for user in vip_users:
            print(f"{user[0]:<10}{user[1]:<20}{user[2]:<25}{user[3]:<25}{user[4]:<15}{'Yes' if user[6] else 'No':<10}")

    def display_all_users(self):
        print("""Displays all users in the system.""")
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()

        if not users:
            print(" No users found.")
            return
        
        print("\n All Users List:")
        print("-" * 100)
        print(f"{'User ID':<10}{'Username':<20}{'Full Name':<25}{'Email':<25}{'Phone':<15}{'VIP Pass':<10}")
        print("-" * 100)

        for user in users:
            print(f"{user[0]:<10}{user[1]:<20}{user[2]:<25}{user[3]:<25}{user[4]:<15}{'Yes' if user[6] else 'No':<10}")

    def remove_user(self):
        """Removes a user from the system."""
        username = input("Enter username: ").strip()
        query = "DELETE FROM users WHERE username = %s"
        
        self.cursor.execute(query, (username,))
        self.con.commit()

        if self.cursor.rowcount > 0:
            print(" User removed successfully.")
        else:
            print(" User not found.")

    def display_all_users(self):
        """Displays all users from the database in a tabular format."""
        query = "SELECT user_id, username, userFullname, email, phone_number, address, vip_pass FROM users"

        try:
            self.cursor.execute(query)
            users = self.cursor.fetchall()

            if not users:
                print(" No users found in the database.")
                return

            print("\n List of Registered Users:")
            print("-" * 105)
            print(f"{'ID':<5}{'Username':<12}{'Full Name':<25}{'Email':<22}{'Phone':<15}{'Address':<30}{'VIP Pass':<10}")
            print("-" * 105)

            for user in users:
                user_id, username, full_name, email, phone, address, vip_pass = user
                print(f"{user_id:<5}{username:<12}{full_name[:23]:<25}{email[:20]:<22}{phone:<15}{address[:28]:<30}{'Yes' if vip_pass else 'No':<10}")

            print("-" * 105)

        except mysql.connector.Error as err:
            print(f" Database error: {err}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
            
    def view_sales_report(self):
        """Displays total sales over time using Matplotlib."""
        cursor = self.con.cursor(dictionary=True)

        # Fetch all sales data
        cursor.execute("""
            SELECT order_date, total_amount 
            FROM orders 
            ORDER BY order_date ASC
        """)

        orders = cursor.fetchall()

        if not orders:
            print("No sales data available.")
            return

        # Aggregate sales by date
        sales_data = defaultdict(float)  # Dictionary to store {date: total_sales}
        for order in orders:
            order_date = order["order_date"].date()  # Convert to date only
            sales_data[order_date] += float(order["total_amount"])

        # Extract data for plotting
        dates = list(sales_data.keys())
        sales = list(sales_data.values())

        # Generate unique colors for bars
        colors = plt.cm.viridis_r(range(len(dates)))

        # Plot sales report
        plt.figure(figsize=(12, 6))
        plt.bar(dates, sales, color=colors, alpha=0.8, width=0.6)  # Wider bars

        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Total Sales (₹)", fontsize=12)
        plt.title("📊 Total Sales Report", fontsize=14)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.show()
            
    def sales_by_genre(self):
        """Generates a pie chart showing sales distribution by book genre."""
        cursor = self.con.cursor()

        # Query to get total sales by genre
        query = """
        SELECT b.genre, SUM(o.total_amount) AS total_sales
        FROM orders o
        JOIN books b ON o.user_id = b.seller_id  -- Adjust this JOIN based on your database structure
        GROUP BY b.genre
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No sales data available.")
            return

        # Extract genres and sales values
        genres = []
        sales = []

        for row in results:
            genres.append(row[0])  # Genre name
            sales.append(float(row[1]))  # Convert sales to float

        # Define labels for the genres
        genre_labels = {
            "1": "Fiction",
            "2": "Non-Fiction",
            "3": "Science Fiction",
            "4": "Fantasy",
            "5": "Mystery",
            "6": "Biography",
            "7": "History",
            "8": "Romance"
        }
        labels = [genre_labels.get(str(genre), "Unknown") for genre in genres]

        # Create pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(sales, labels=labels, autopct='%1.1f%%', startangle=140, colors=[
            "#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6", "#ff6666", "#66ff66"
        ])
        plt.title(" Sales Distribution by Genre")
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.show()

        cursor.close()

    # def view_sales_history(self):
    #     """Displays the sales history in a properly formatted tabular format."""
    #     query = "SELECT order_id, user_id, total_amount, order_date, status FROM orders"

    #     try:
    #         self.cursor.execute(query)
    #         sales = self.cursor.fetchall()

    #         if not sales:
    #             print("📌 No sales history available.")
    #             return

    #         # Define column widths for consistent formatting
    #         col_widths = [10, 10, 15, 22, 12]  

    #         print("\n📦 Sales History:")
    #         print(f"+{'-' * col_widths[0]}+{'-' * col_widths[1]}+{'-' * col_widths[2]}+{'-' * col_widths[3]}+{'-' * col_widths[4]}+")
    #         print(f"| {'Order ID':^{col_widths[0]}} | {'User ID':^{col_widths[1]}} | {'Total Amount':^{col_widths[2]}} | {'Order Date':^{col_widths[3]}} | {'Status':^{col_widths[4]}} |")
    #         print(f"+{'-' * col_widths[0]}+{'-' * col_widths[1]}+{'-' * col_widths[2]}+{'-' * col_widths[3]}+{'-' * col_widths[4]}+")

    #         for sale in sales:
    #             order_id, user_id, total_amount, order_date, status = sale
    #             print(f"| {order_id:^{col_widths[0]}} | {user_id:^{col_widths[1]}} | ${total_amount:>{col_widths[2] - 2}.2f} | {order_date:^{col_widths[3]}} | {status:^{col_widths[4]}} |")

    #         print(f"+{'-' * col_widths[0]}+{'-' * col_widths[1]}+{'-' * col_widths[2]}+{'-' * col_widths[3]}+{'-' * col_widths[4]}+")

    #     except mysql.connector.Error as err:
    #         print(f"❌ Database error: {err}")
    #     except Exception as e:
    #         print(f"❌ An unexpected error occurred: {e}")
    



        