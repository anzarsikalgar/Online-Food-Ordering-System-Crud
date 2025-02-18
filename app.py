import mysql.connector
from mysql.connector import Error

# Function to create a connection to MySQL
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root'  # Replace with your MySQL password
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to create a database and tables
def setup_database():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        try:
            # Create a new database (if it doesn't exist)
            cursor.execute("CREATE DATABASE IF NOT EXISTS Online_Food_Ordering_System")
            print("Database 'Online_Food_Ordering_System' created successfully!")

            # Use the new database
            cursor.execute("USE Online_Food_Ordering_System")

            # Create 'menu_items' table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT
            )
            ''')
            print("'menu_items' table created successfully!")

            # Create 'customers' table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                email VARCHAR(100),
                address TEXT
            )
            ''')
            print("'customers' table created successfully!")

            # Create 'orders' table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                item_id INT NOT NULL,
                quantity INT NOT NULL,
                total_price DECIMAL(10, 2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE ON UPDATE CASCADE
            )
            ''')
            print("'orders' table created successfully!")

        except Error as e:
            print(f"Error creating database or tables: {e}")
        finally:
            conn.close()

# Run the setup to create the database and tables
setup_database()


















# Improved email validation using regex
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        print("Invalid email format.")
        return False

# Improved phone number validation using regex
def validate_phone(phone):
    phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 international format
    if re.match(phone_regex, phone):
        return True
    else:
        print("Invalid phone number format.")
        return False

# Efficient update_menu_item
def update_menu_item():
    item_id = input("Enter item ID to update: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items WHERE item_id = %s', (item_id,))
        item = cursor.fetchone()
        
        if not item:
            print("Item not found.")
            conn.close()
            return
        
        print(f"Current name: {item[1]}, Current price: {item[2]}, Current description: {item[3]}")
        name = input("Enter new name (leave blank to skip): ")
        price = input("Enter new price (leave blank to skip): ")
        if price and not validate_price(price):
            conn.close()
            return
        description = input("Enter new description (leave blank to skip): ")

        update_fields = []
        update_values = []

        if name:
            update_fields.append("name = %s")
            update_values.append(name)
        if price:
            update_fields.append("price = %s")
            update_values.append(price)
        if description:
            update_fields.append("description = %s")
            update_values.append(description)

        if update_fields:
            update_values.append(item_id)
            update_query = f"UPDATE menu_items SET {', '.join(update_fields)} WHERE item_id = %s"
            cursor.execute(update_query, tuple(update_values))
            conn.commit()
            print("Menu item updated successfully!")
        else:
            print("No changes made.")
        
        conn.close()

# Enhanced place_order with validation for customer and item IDs
def place_order():
    customer_id = input("Enter customer ID: ")
    item_id = input("Enter item ID: ")
    quantity = input("Enter quantity: ")
    if not validate_quantity(quantity):
        return
    
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # Validate customer
        cursor.execute('SELECT * FROM customers WHERE customer_id = %s', (customer_id,))
        if not cursor.fetchone():
            print("Invalid customer ID.")
            conn.close()
            return
        
        # Validate item
        cursor.execute('SELECT * FROM menu_items WHERE item_id = %s', (item_id,))
        item = cursor.fetchone()
        if not item:
            print("Invalid item ID.")
            conn.close()
            return
        
        # Fetch item price
        price = item[2]
        total_price = float(price) * int(quantity)
        
        cursor.execute('INSERT INTO orders (customer_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)', 
                       (customer_id, item_id, quantity, total_price))
        conn.commit()
        print("Order placed successfully!")
        conn.close()

# Updated price validation
def validate_price(price):
    try:
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        return True
    except ValueError:
        print("Invalid price. Please enter a valid number.")
        return False

# Updated quantity validation
def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return True
    except ValueError:
        print("Invalid quantity. Please enter a valid integer.")
        return False

# CRUD Operations (Modified)

# Create (Insert) Operations...


# Create (Insert) Operations

# Add Menu Item
def add_menu_item():
    name = input("Enter item name: ")
    price = input("Enter item price: ")
    if not validate_price(price):
        return
    description = input("Enter item description: ")
    
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO menu_items (name, price, description) VALUES (%s, %s, %s)', (name, price, description))
            conn.commit()
            print("Menu item added successfully!")
        except Error as e:
            print(f"Error adding menu item: {e}")
        finally:
            conn.close()

# Add Customer
def add_customer():
    name = input("Enter customer name: ")
    phone = input("Enter customer phone: ")
    if not validate_phone(phone):
        return
    email = input("Enter customer email: ")
    if email and not validate_email(email):
        return
    address = input("Enter customer address: ")

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO customers (name, phone, email, address) VALUES (%s, %s, %s, %s)', (name, phone, email, address))
            conn.commit()
            print("Customer added successfully!")
        except Error as e:
            print(f"Error adding customer: {e}")
        finally:
            conn.close()

# Place Order
def place_order():
    customer_id = input("Enter customer ID: ")
    item_id = input("Enter item ID: ")
    quantity = input("Enter quantity: ")
    if not validate_quantity(quantity):
        return
    
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        
        # Validate customer
        cursor.execute('SELECT * FROM customers WHERE customer_id = %s', (customer_id,))
        if not cursor.fetchone():
            print("Invalid customer ID.")
            conn.close()
            return
        
        # Validate item
        cursor.execute('SELECT * FROM menu_items WHERE item_id = %s', (item_id,))
        item = cursor.fetchone()
        if not item:
            print("Invalid item ID.")
            conn.close()
            return
        
        # Calculate total price
        price = item[2]  # assuming the price is the third column
        total_price = float(price) * int(quantity)

        try:
            cursor.execute('INSERT INTO orders (customer_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)', 
                           (customer_id, item_id, quantity, total_price))
            conn.commit()
            print("Order placed successfully!")
        except Error as e:
            print(f"Error placing order: {e}")
        finally:
            conn.close()


# Read (View) Operations

# View Menu Items
def view_menu_items():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM menu_items')
            items = cursor.fetchall()
            if items:
                print("\nMenu Items:")
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Description: {item[3]}")
            else:
                print("No menu items available.")
        except Error as e:
            print(f"Error fetching menu items: {e}")
        finally:
            conn.close()

# View Orders
def view_orders():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM orders')
            orders = cursor.fetchall()
            if orders:
                print("\nOrders:")
                for order in orders:
                    print(f"Order ID: {order[0]}, Customer ID: {order[1]}, Item ID: {order[2]}, Quantity: {order[3]}, Total Price: {order[4]}, Date: {order[5]}")
            else:
                print("No orders found.")
        except Error as e:
            print(f"Error fetching orders: {e}")
        finally:
            conn.close()

# View Customers
def view_customers():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM customers')
            customers = cursor.fetchall()
            if customers:
                print("\nCustomers:")
                for customer in customers:
                    print(f"ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}, Address: {customer[4]}")
            else:
                print("No customers found.")
        except Error as e:
            print(f"Error fetching customers: {e}")
        finally:
            conn.close()

# Update Operations

# Update Menu Item
def update_menu_item():
    item_id = input("Enter item ID to update: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM menu_items WHERE item_id = %s', (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found.")
                conn.close()
                return

            print(f"Current name: {item[1]}, Current price: {item[2]}, Current description: {item[3]}")
            name = input("Enter new name (leave blank to skip): ")
            price = input("Enter new price (leave blank to skip): ")
            if price and not validate_price(price):
                conn.close()
                return
            description = input("Enter new description (leave blank to skip): ")

            update_fields = []
            update_values = []

            if name:
                update_fields.append("name = %s")
                update_values.append(name)
            if price:
                update_fields.append("price = %s")
                update_values.append(price)
            if description:
                update_fields.append("description = %s")
                update_values.append(description)

            if update_fields:
                update_values.append(item_id)
                update_query = f"UPDATE menu_items SET {', '.join(update_fields)} WHERE item_id = %s"
                cursor.execute(update_query, tuple(update_values))
                conn.commit()
                print("Menu item updated successfully!")
            else:
                print("No changes made.")

        except Error as e:
            print(f"Error updating menu item: {e}")
        finally:
            conn.close()


# Delete Operations

# Delete Menu Item
def delete_menu_item():
    item_id = input("Enter item ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM menu_items WHERE item_id = %s', (item_id,))
            conn.commit()
            print("Menu item deleted successfully!")
        except Error as e:
            print(f"Error deleting menu item: {e}")
        finally:
            conn.close()

# Delete Customer
def delete_customer():
    customer_id = input("Enter customer ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM customers WHERE customer_id = %s', (customer_id,))
            conn.commit()
            print("Customer deleted successfully!")
        except Error as e:
            print(f"Error deleting customer: {e}")
        finally:
            conn.close()

# Delete Order
def delete_order():
    order_id = input("Enter order ID to delete: ")
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM orders WHERE order_id = %s', (order_id,))
            conn.commit()
            print("Order deleted successfully!")
        except Error as e:
            print(f"Error deleting order: {e}")
        finally:
            conn.close()




# CRUD functions remain the same as before

# CLI Menu
def main():
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
    # Initialize the database and tables
    setup_database()

    while True:
        display_menu()  # Display the CLI menu
        choice = input("Enter your choice: ")

        if choice == '1':
            add_menu_item()  # Add menu item
        elif choice == '2':
            add_customer()  # Add customer
        elif choice == '3':
            place_order()  # Place an order
        elif choice == '4':
            view_menu_items()  # View menu items
        elif choice == '5':
            view_orders()  # View orders
        elif choice == '6':
            view_customers()  # View customers
        elif choice == '7':
            update_menu_item()  # Update menu item
        elif choice == '8':
            update_customer()  # Update customer
        elif choice == '9':
            delete_menu_item()  # Delete menu item
        elif choice == '10':
            delete_customer()  # Delete customer
        elif choice == '11':
            delete_order()  # Delete order
        elif choice == '12':
            print("Exiting the system. Goodbye!")  # Exit the system
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()

# Main function remains the same