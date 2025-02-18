Online Food Ordering System (Python, MySQL)
Developed a CRUD-based Online Food Ordering System using Python and MySQL following OOP principles.
Implemented modular design with separate classes for Database, Menu, Customers, and Orders to ensure scalability and maintainability.
Designed a CLI-based user interface for managing menu items, customers, and orders, including order placement, updates, and deletion.
Optimized total price calculation dynamically based on menu prices and order quantity.
Integrated error handling and input validation to enhance system reliability.





-================================-=========================-==========================-

Online Food Ordering System
Developed a Python-based food ordering application with MySQL backend

Key Achievements:

Designed and implemented a robust database with tables for menu items, customers, and orders using MySQL.
Developed CRUD functionalities for managing menu items, customer data, and orders.
Incorporated data validation and error handling to ensure seamless user experience and data integrity.
Applied Object-Oriented Programming principles to build a scalable and maintainable system.
Technologies: Python, MySQL, OOP, SQL, Data Validation


========================================================================================================

import hashlib

def add_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            print("User added successfully!")
        except Error as e:
            print(f"Error adding user: {e}")
        finally:
            conn.close()