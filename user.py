import mysql.connector
import datetime
import time
import matplotlib.pyplot as plt
class User:
    def __init__(self, con, username):
        self.con = con
        self.username = username
        self.cart = []  # Using a list instead of a linked list
        self.load_previous_cart()
        # self.admin_instance = Admin(self.con)  # Create an instance of Admin class

    def load_previous_cart(self):
        """Loads the previous cart items from the database."""
        try:
            cursor = self.con.cursor()
            query = "SELECT book_id FROM cart WHERE username = %s"
            cursor.execute(query, (self.username,))
            self.cart = [row[0] for row in cursor.fetchall()]
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error loading cart: {err}")

    def user_menu(self):
        while True:
            print("\nUser Menu:")
            print("-----------------------------------------")
            print("1 --> Add Book to Cart")
            print("2 --> Remove Book from Cart")
            print("3 --> View Cart")
            print("4 --> View Bill")
            print("5 --> Make Payment")
            print("6 --> Display Books Menu")
            print("7 --> Search Book by ISBN")
            print("8 --> View Books by Rating")
            print("9 --> View Purchase History")
            print("10 --> Generate bill txt file")
            print("11 --> Logout")
            # print("10 --> View Books by Genre")
            # print("11 --> Logout")
            print("-----------------------------------------\n")

            choice = input("Choose an option: ")
            
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                self.add_to_cart()
            elif choice == 2:
                self.remove_book_from_cart()
                
            elif choice == 3:
                self.display_cart_details()
                
            elif choice == 4:
                self.view_bill()
                
            elif choice == 5:
                self.make_payment()
                
            elif choice == 6:
                self.display_books_menu(self.username)
                
            elif choice == 7:
                self.search_book_by_isbn(self.con)
                
            elif choice == 8:
                self.sort_books_by_rating_descending()
            elif choice == 9:
                self.view_purchase_history()
                
            elif choice == 10:
                self.generate_bill_txt()
            elif choice == 11:
                print("LOGOUT...")
                break
            else:
                print("Invalid option. Please try again.")
    
    def add_to_cart(self):
        """Allows a user to add a book to the cart with stock validation."""
        
        self.display_all_books()
        cursor = self.con.cursor(dictionary=True)
        
        # Retrieve user ID based on username
        sql1 = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql1, (self.username,))
        user = cursor.fetchone()
        
        if not user:
            print("User not found.")
            return
        
        user_id = user["user_id"]

        try:
            book_id = int(input("Enter Book ID: "))
            quantity = int(input("Enter Quantity: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return

        # Retrieve book details
        sql2 = "SELECT * FROM books WHERE book_id = %s"
        cursor.execute(sql2, (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book not found.")
            return

        stock_quantity = book["stock_quantity"]
        
        if quantity > stock_quantity:
            print(f"Sorry, only {stock_quantity} copies available. Please enter a lower quantity.")
            return
        
        book_name = book["title"]
        price = book["price"]
        total_price = price * quantity

        # Insert into cart table
        sql3 = "INSERT INTO cart (user_id, username, book_id, bookname, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql3, (user_id, self.username, book_id, book_name, quantity, total_price))
        self.con.commit()

        # Update stock in the books table
        sql4 = "UPDATE books SET stock_quantity = stock_quantity - %s WHERE book_id = %s"
        cursor.execute(sql4, (quantity, book_id))
        self.con.commit()

        # Add book to cart list
        self.cart.append({
            "user_id": user_id,
            "username": self.username,
            "book_id": book_id,
            "bookname": book_name,
            "quantity": quantity,
            "price": total_price
        })

        print(f"Book '{book_name}' added to cart successfully.")

    
    def is_empty(self):
        return len(self.items) == 0

    def clear_cart(self):
        self.items = []

    
    def get_user_id(self):
        """Fetch user ID from the database."""
        cursor = self.con.cursor(dictionary=True)
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (self.username,))
        user = cursor.fetchone()
        return user["user_id"] if user else None

    def fetch_cart(self):
        """Fetch cart items for the user."""
        cursor = self.con.cursor(dictionary=True)
        cursor.execute("SELECT book_id, bookname, quantity, price FROM cart WHERE username = %s", (self.username,))
        self.cart = cursor.fetchall()

    def display_bill(self, total_amount):
        """Prints the bill in a structured format."""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n --------------- ONLINE DIGITAL MALL BILL ----------------")
        print(f" User: {self.username}        Date: {current_date}")
        print("----------------------------------------------------------")
        
        for item in self.cart:
            print(f" Book ID: {item['book_id']}  |  Book Name: {item['bookname']}")
            print(f" Quantity: {item['quantity']} |  Price: ₹{item['price']:.2f}")
            print("----------------------------------------------------------")
        
        print(f"\n TOTAL AMOUNT OF YOUR BILL: ₹{total_amount:.2f}")

    def make_payment(self):
        """Handles payment selection and processing."""
        self.fetch_cart()
        if not self.cart:
            print(" NO ITEMS IN CART!")
            return

        user_id = self.get_user_id()
        if not user_id:
            print(" User not found.")
            return

        total_amount = sum(item["price"] for item in self.cart)
        self.display_bill(total_amount)

        print("\n Choose Payment Method:")
        print("1️ Cash on Delivery")
        print("2️ UPI")
        print("3️ Debit Card")

        try:
            choice = int(input("Enter payment option (1/2/3): "))
        except ValueError:
            print(" Invalid input. Please enter a number.")
            return

        match choice:
            case 1:
                self.process_cash_on_delivery(user_id, total_amount)

            case 2:
                self.process_upi_payment(user_id, total_amount)

            case 3:
                self.process_debit_card_payment(user_id, total_amount)

            case _:
                print(" Invalid Payment Method.")

    def process_cash_on_delivery(self, user_id, total_amount):
        """Handles Cash on Delivery payment."""
        print(" Order successfully placed with Cash on Delivery.")
        self.process_payment(user_id, total_amount, "Cash on Delivery")

    def process_upi_payment(self, user_id, total_amount):
        """Handles UPI payment."""
        upi_id = input(" Enter UPI ID: ")
        print("Processing payment via UPI...")
        time.sleep(5)
        print(" Payment Successful!")
        self.process_payment(user_id, total_amount, "UPI")

    def process_debit_card_payment(self, user_id, total_amount):
        """Handles Debit Card payment."""
        while True:
            card_number = input(" Enter 16-digit Debit Card Number: ")
            if len(card_number) == 16 and card_number.isdigit():
                break
            print(" Invalid card number. Must be 16 digits.")

        while True:
            try:
                amount = float(input(" Enter payment amount: "))
                if amount == total_amount:
                    print("Processing Debit Card payment...")
                    time.sleep(5)
                    print(" Payment Successful!")
                    self.process_payment(user_id, total_amount, "Debit Card")
                    break
                else:
                    print(" Amount does not match the total bill.")
            except ValueError:
                print(" Invalid amount.")

    def process_payment(self, user_id, total_amount, payment_method):
        """Handles order placement and payment processing."""
        try:
            cursor = self.con.cursor()

            # Insert into orders
            cursor.execute("INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, 'Paid')",
                           (user_id, total_amount))

            # Insert into payments
            cursor.execute("INSERT INTO payments (user_id, username, amount, payment_method, status) VALUES (%s, %s, %s, %s, 'Paid')",
                           (user_id, self.username, total_amount, payment_method))

            # Clear cart
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

            self.con.commit()
            self.cart.clear()
            print(" Order processed successfully! Thank you for shopping with us.")

        except mysql.connector.Error as e:
            print(" Database error:", e)
            self.con.rollback()
    
    def view_bill(self):
        """Displays the user's cart in bill format."""
        cursor = self.con.cursor(dictionary=True)

        # Fetch user's cart details from the database
        query = "SELECT book_id, bookname, quantity, price FROM cart WHERE username = %s"
        cursor.execute(query, (self.username,))
        self.cart = cursor.fetchall()

        if not self.cart:
            print(" No items found in the cart.")
            return False  # Indicates the cart is empty

        # Get the current date and time
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n --------------- FICTION FUSION BILL ----------------")
        print(f" User: {self.username}        Date: {current_date}")
        print("----------------------------------------------------------")
        print("{:<10} {:<25} {:<10} {:<10}".format("Book ID", "Book Name", "Quantity", "Price (₹)"))
        print("----------------------------------------------------------")

        total_amount = 0
        for item in self.cart:
            print("{:<10} {:<25} {:<10} {:<10.2f}".format(
                item["book_id"], item["bookname"], item["quantity"], item["price"]
            ))
            total_amount += item["price"] * item["quantity"]

        print("----------------------------------------------------------")
        print(f" TOTAL AMOUNT: ₹{total_amount:.2f}")
        print("----------------------------------------------------------")
        
        return True  # Indicates the cart has items

    
    def display_cart_details(self):
        """Displays the user's cart details in a formatted table."""
        
        query = "SELECT cart_id, bookname, quantity, price FROM cart WHERE username = %s"
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(query, (self.username,))
        self.cart = cursor.fetchall()

        if not self.cart:
            print("\n Your cart is empty.")
            return False  # Indicates the cart is empty

        # Display cart header
        print("\n Your Cart:")
        print("=" * 50)
        print(f"{'Cart ID':<10}{'Book Name':<25}{'Quantity':<10}{'Price'}")
        print("=" * 50)

        # Display cart items
        for item in self.cart:
            print(f"{item['cart_id']:<10}{item['bookname']:<25}{item['quantity']:<10}{item['price']:<10.2f}")

        print("=" * 50)
        
        return True  # Indicates the cart has items


    def remove_book_from_cart(self):
        """Removes a book from the cart based on user input."""
        if not self.display_cart_details():
            print("No items in the cart. Please add items first.")
            return

        choice = input("Do you want to remove a book from the cart? (yes/no): ").strip().lower()
        if choice != "yes":
            print("You have chosen not to remove any book from the cart.")
            return

        while True:
            try:
                remove_cart_id = int(input("Enter the Cart ID of the book you want to remove: "))

                # Check if the entered cart_id exists in self.cart
                if not any(item["cart_id"] == remove_cart_id for item in self.cart):
                    print("Cart ID not found. Please enter a valid Cart ID.")
                    continue  # Prompt the user again
                
                # Delete the book from the database
                query = "DELETE FROM cart WHERE username = %s AND cart_id = %s"
                cursor = self.con.cursor()
                cursor.execute(query, (self.username, remove_cart_id))
                self.con.commit()

                # Remove from the local list
                self.cart = [item for item in self.cart if item["cart_id"] != remove_cart_id]

                print(" Book removed from cart successfully.")
                break  # Exit the loop once successfully removed

            except ValueError:
                print(" Invalid input. Please enter a valid Cart ID (a number).")
            except mysql.connector.Error as err:
                print(f" Database error: {err}")
            except Exception as e:
                print(f" An unexpected error occurred: {e}")

    
    def search_book_by_isbn(self, con):
        """Search for a book by ISBN and display details from a MySQL database."""
        
        isbn = input("Enter ISBN: ")  # Get ISBN input from the user

        query = "SELECT * FROM books WHERE isbn = %s"

        try:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute(query, (isbn,))
                book = cursor.fetchone()  # Fetch the first matching row

                # Print table header
                print("{:<15} {:<30} {:<20} {:<15} {:<10} {:<6}".format(
                    "ISBN", "Title", "Author", "Genre", "Price", "Stock"
                ))
                print("-" * 80)

                if book:
                    print("{:<15} {:<30} {:<20} {:<15} Rs.{:<8.2f} {:<6}".format(
                        book["isbn"], book["title"], book["author"], book["genre"],
                        book["price"], book["stock_quantity"]
                    ))
                else:
                    print(f"No book found with ISBN: {isbn}")

        except mysql.connector.Error as e:
            print("Database error:", e)
    
    def sort_books_by_rating_descending(self):
        """Sorts books by rating in descending order and displays them."""

        query = "SELECT book_id, title, author, genre, price, stock_quantity, rating FROM books ORDER BY rating DESC"
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(query)
        books = cursor.fetchall()

        if not books:
            print("\n No books available.")
            return

        print("\n Books Sorted by Rating (High to Low):")
        print("=" * 90)
        print("{:<4} {:<30} {:<20} {:<15} {:<10} {:<6} {:<6}".format(
            "ID", "Title", "Author", "Genre", "Price", "Qty", "Rating"
        ))
        print("=" * 90)

        for book in books:
            print("{:<4} {:<30} {:<20} {:<15} Rs.{:<8.2f} {:<6} {:<6.1f}".format(
                book["book_id"], book["title"], book["author"], book["genre"],
                book["price"], book["stock_quantity"], book["rating"]
            ))

        print("=" * 90)


    
    def display_books_menu(self, username):
        """Displays books based on user-selected criteria."""
        while True:
            print("""
                How would you like to display books?
            -----------------------------------------
                    1 --> By Title
                    2 --> By Author
                    3 --> By Genre
                    4 --> Back to User Menu
            -----------------------------------------
            """)
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                continue  # Retry input

            if choice == 1:
                self.display_all_books()
                title_keyword = input("Enter title keyword: ").strip()
                query = "SELECT * FROM books WHERE title LIKE %s"
                self.print_book_results(query, ("%" + title_keyword + "%",))

            elif choice == 2:
                self.display_all_books()
                author_keyword = input("Enter author keyword: ").strip()
                query = "SELECT * FROM books WHERE author LIKE %s"
                self.print_book_results(query, ("%" + author_keyword + "%",))

            elif choice == 3:
                self.view_books_by_genre(username)

            elif choice == 4:
                print(" Returning to Main Menu...")
                return

            else:
                print(" Invalid option. Please try again.")

    def print_book_results(self, query, params):
        """Executes a query and prints book results in a formatted table."""
        cursor = self.con.cursor(dictionary=True)

        try:
            cursor.execute(query, params)
            books = cursor.fetchall()

            if not books:
                print("📚 No matching books found.")
                return

            print("\n" + "-" * 110)
            print("{:<5} {:<15} {:<30} {:<20} {:<15} {:<10} {:<6}".format(
                "BookID", "ISBN", "Title", "Author", "Genre", "Price", "Stock"
            ))
            print("-" * 110)

            for book in books:
                print("{:<5} {:<15} {:<30} {:<20} {:<15} Rs.{:<8.2f} {:<6}".format(
                    book["book_id"], book["isbn"], book["title"], book["author"],
                    book["genre"], book["price"], book["stock_quantity"]
                ))

            print("-" * 110)

        except mysql.connector.Error as e:
            print(f"❌ Error fetching books: {e}")
        

    def view_books_by_genre(self, username):
        """Retrieves and displays books by genre."""
        query = "SELECT DISTINCT genre FROM books"
        cursor = self.con.cursor(dictionary=True)

        try:
            cursor.execute(query)
            genres = cursor.fetchall()

            if not genres:
                print(" No genres available.")
                return

            print("\nAvailable Genres:")
            for index, genre in enumerate(genres, start=1):
                print(f"{index}. {genre['genre']}")

            try:
                choice = int(input("\nChoose a genre by number: ")) - 1
                if choice < 0 or choice >= len(genres):
                    print(" Invalid choice.")
                    return

                selected_genre = genres[choice]["genre"]
                query = "SELECT * FROM books WHERE genre = %s"
                self.print_book_results(query, (selected_genre,))

            except ValueError:
                print(" Invalid input. Please enter a number.")

        except mysql.connector.Error as e:
            print(f" Error fetching genres: {e}")
        
    
    def display_all_books(self):
        """Displays all available books in the store."""
        query = "SELECT book_id, isbn, title, author, genre, price, stock_quantity FROM books"
        cursor = self.con.cursor(dictionary=True)

        try:
            cursor.execute(query)
            books = cursor.fetchall()

            if not books:
                print("\n No books available in the store.")
                return

            print("\n" + "-" * 110)
            print("{:<5} {:<15} {:<30} {:<20} {:<15} {:<10} {:<6}".format(
                "BookID", "ISBN", "Title", "Author", "Genre", "Price", "Stock"
            ))
            print("-" * 110)

            for book in books:
                print("{:<5} {:<15} {:<30} {:<20} {:<15} Rs.{:<8.2f} {:<6}".format(
                    book["book_id"], book["isbn"], book["title"], book["author"],
                    book["genre"], book["price"], book["stock_quantity"]
                ))

            print("-" * 110)

        except mysql.connector.Error as e:
            print(f" Error fetching books: {e}")
        
    def view_purchase_history(self):
        """Fetches and displays the user's purchase history using Matplotlib."""
        cursor = self.con.cursor(dictionary=True)

        # Get user_id from username
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (self.username,))
        user = cursor.fetchone()

        if not user:
            print(" User not found.")
            return

        user_id = user["user_id"]

        # Fetch order data for the user
        cursor.execute("""
            SELECT order_date, total_amount 
            FROM orders 
            WHERE user_id = %s 
            ORDER BY order_date ASC
        """, (user_id,))
        
        orders = cursor.fetchall()

        if not orders:
            print(" No purchase history found.")
            return
        
        # Extract dates and amounts
        dates = [order["order_date"].date() for order in orders]  # Directly use .date()
        amounts = [order["total_amount"] for order in orders]

        # Plot purchase history
        plt.figure(figsize=(10, 5))
        plt.bar(dates, amounts, color='skyblue', alpha=0.8)

        plt.xlabel("Date")
        plt.ylabel("Total Amount Spent (₹)")
        plt.title(f" Purchase History for {self.username}")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.show()
        

    def generate_bill_txt(self):
        """Generates a bill and appends it to a .txt file named after the username."""
        cursor = self.con.cursor(dictionary=True)

        # Fetch cart details from the database
        query = "SELECT book_id, bookname, quantity, price FROM cart WHERE username = %s"
        cursor.execute(query, (self.username,))
        cart_items = cursor.fetchall()

        if not cart_items:
            print(" No items found in the cart.")
            return False  # Indicates the cart is empty

        # Get current date and format the filename
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{self.username}_ShoppingBill.txt"

        # Calculate total amount
        total_amount = sum(item["price"] * item["quantity"] for item in cart_items)

        # Write or append bill details to the file
        with open(filename, "a", encoding="utf-8") as file:  # "a" mode for appending
            file.write("\n --------------- FICTION FUSION BILL ----------------\n")
            file.write(f" User: {self.username}\n")
            file.write(f" Date: {current_date}\n")
            file.write("-" * 60 + "\n")
            file.write("{:<10} {:<25} {:<10} {:<10}\n".format("Book ID", "Book Name", "Quantity", "Price (₹)"))
            file.write("-" * 60 + "\n")

            for item in cart_items:
                file.write("{:<10} {:<25} {:<10} {:<10.2f}\n".format(
                    item["book_id"], item["bookname"], item["quantity"], item["price"]
                ))

            file.write("-" * 60 + "\n")
            file.write(f" TOTAL AMOUNT: ₹{total_amount:.2f}\n")
            file.write("-" * 60 + "\n")

        print(f" Bill generated and saved to: {filename}")
        return True