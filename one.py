import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='ordering_db'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Validation functions
def validate_price(price):
    try:
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        return True
    except ValueError:
        print("Invalid price. Please enter a valid number.")
        return False

def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return True
    except ValueError:
        print("Invalid quantity. Please enter a valid integer.")
        return False

# CRUD Operations

# Create (Insert)
def add_menu_item():
    name = input("Enter item name: ")
    price = input("Enter item price: ")
    if not validate_price(price):
        return
    description = input("Enter item description: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO menu_items (name, price, description) VALUES (%s, %s, %s)', (name, price, description))
        conn.commit()
        print("Menu item added successfully!")
        conn.close()

def add_customer():
    name = input("Enter customer name: ")
    phone = input("Enter customer phone: ")
    email = input("Enter customer email: ")
    address = input("Enter customer address: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, phone, email, address) VALUES (%s, %s, %s, %s)', (name, phone, email, address))
        conn.commit()
        print("Customer added successfully!")
        conn.close()

def place_order():
    customer_id = input("Enter customer ID: ")
    item_id = input("Enter item ID: ")
    quantity = input("Enter quantity: ")
    if not validate_quantity(quantity):
        return
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # Fetch item price 
        cursor.execute('SELECT price FROM menu_items WHERE item_id = %s', (item_id,))
        price = cursor.fetchone()[0]
        total_price = float(price) * int(quantity)
        cursor.execute('INSERT INTO orders (customer_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)', (customer_id, item_id, quantity, total_price))
        conn.commit()
        print("Order placed successfully!")
        conn.close()

# Read (View)
def view_menu_items():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items')
        items = cursor.fetchall()
        conn.close()
        print("\nMenu Items:")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Description: {item[3]}")
    else:
        print("No menu items found.")

def view_orders():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        conn.close()
        print("\nOrders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Customer ID: {order[1]}, Item ID: {order[2]}, Quantity: {order[3]}, Total Price: {order[4]}, Date: {order[5]}")
    else:
        print("No orders found.")

def view_customers():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        conn.close()
        print("\nCustomers:")
        for customer in customers:
            print(f"ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}, Address: {customer[4]}")
    else:
        print("No customers found.")

# Update
def update_menu_item():
    item_id = input("Enter item ID to update: ")
    name = input("Enter new name (leave blank to skip): ")
    price = input("Enter new price (leave blank to skip): ")
    if price and not validate_price(price):
        return
    description = input("Enter new description (leave blank to skip): ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE menu_items SET name = %s WHERE item_id = %s', (name, item_id))
        if price:
            cursor.execute('UPDATE menu_items SET price = %s WHERE item_id = %s', (price, item_id))
        if description:
            cursor.execute('UPDATE menu_items SET description = %s WHERE item_id = %s', (description, item_id))
        conn.commit()
        print("Menu item updated successfully!")
        conn.close()

def update_customer():
    customer_id = input("Enter customer ID to update: ")
    name = input("Enter new name (leave blank to skip): ")
    phone = input("Enter new phone (leave blank to skip): ")
    email = input("Enter new email (leave blank to skip): ")
    address = input("Enter new address (leave blank to skip): ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE customers SET name = %s WHERE customer_id = %s', (name, customer_id))
        if phone:
            cursor.execute('UPDATE customers SET phone = %s WHERE customer_id = %s', (phone, customer_id))
        if email:
            cursor.execute('UPDATE customers SET email = %s WHERE customer_id = %s', (email, customer_id))
        if address:
            cursor.execute('UPDATE customers SET address = %s WHERE customer_id = %s', (address, customer_id))
        conn.commit()
        print("Customer updated successfully!")
        conn.close()

# Delete
def delete_menu_item():
    item_id = input("Enter item ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM menu_items WHERE item_id = %s', (item_id,))
        conn.commit()
        print("Menu item deleted successfully!")
        conn.close()

def delete_customer():
    customer_id = input("Enter customer ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE customer_id = %s', (customer_id,))
        conn.commit()
        print("Customer deleted successfully!")
        conn.close()

def delete_order():
    order_id = input("Enter order ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE order_id = %s', (order_id,))
        conn.commit()
        print("Order deleted successfully!")
        conn.close()

# CLI Menu
def display_menu():
    print("\nOnline Food Ordering System")
    print("1. Add Menu Item")
    print("2. Add Customer")
    print("3. Place Order")
    print("4. View Menu Items")
    print("5. View Orders")
    print("6. View Customers")
    print("7. Update Menu Item")
    print("8. Update Customer")
    print("9. Delete Menu Item")
    print("10. Delete Customer")
    print("11. Delete Order")
    print("12. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_menu_item()
        elif choice == '2':
            add_customer()
        elif choice == '3':
            place_order()
        elif choice == '4':
            view_menu_items()
        elif choice == '5':
            view_orders()
        elif choice == '6':
            view_customers()
        elif choice == '7':
            update_menu_item()
        elif choice == '8':
            update_customer()
        elif choice == '9':
            delete_menu_item()
        elif choice == '10':
            delete_customer()
        elif choice == '11':
            delete_order()
        elif choice == '12':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
    
    



#------------------------------MYSQL--------START------------------------------------

#execute the script in mysql
# CREATE DATABASE IF NOT EXISTS ordering_db;

# USE ordering_db;

# CREATE TABLE IF NOT EXISTS menu_items (
#     item_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     price DECIMAL(10, 2) NOT NULL,
#     description TEXT
# );

# CREATE TABLE IF NOT EXISTS customers (
#     customer_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     phone VARCHAR(15) NOT NULL,
#     email VARCHAR(100),
#     address TEXT
# );

# CREATE TABLE IF NOT EXISTS orders (
#     order_id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT NOT NULL,
#     item_id INT NOT NULL,
#     quantity INT NOT NULL,
#     total_price DECIMAL(10, 2) NOT NULL,
#     order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
#     FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
# );

#------------------------------MYSQL-------------END-------------------------------