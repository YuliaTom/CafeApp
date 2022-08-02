import os
import pymysql
import pandas as pd
import csv
from csv_utils import *
from input_utils import *
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

connection = pymysql.connect(
    host,
    user,
    password,
    database
)

cursor = connection.cursor()

main_menu_options = ["Exit", "Products", "Couriers", "Customers", "Orders"]
status_list = ["Preparing", "Out for delivery", "Delivered"]


script_dir = os.path.dirname(__file__)
categories = {
    "products":
        {"options": ["Return to the main menu",
                     "View product list",
                     "Create a new product",
                     "Update an existing product",
                     "Delete product",
                     "Export data",
                     "Import data"],
         "columns": {"id": ("int", "id"),
                     "Product name": ("str", "product_name"),
                     "Price": ("float", "product_price"),
                     "Quantity": ("int", "product_qty")}
         },
    "couriers":
    {"options": ["Return to the main menu",
                 "View courier list",
                 "Create a new courier",
                 "Update an existing courier",
                 "Delete courier",
                 "Export data"],
        "columns": {"id": ("int", "id"),
                    "Courier name": ("str", "courier_name"),
                    "Phone": ("str", "courier_phone")}
     },
    "orders":
    {"options": ["Return to the main menu",
                 "View orders list",
                 "Create a new order",
                 "Update order status",
                 "Update an existing order",
                 "Delete order",
                 "Export data"],
        "columns": {"id": ("int", "id"),
                    "Customer name": ("str", "customer_name"),
                    "Customer address": ("str", "customer_address"),
                    "Customer phone": ("str", "customer_phone"),
                    "Courier name": ("str", "courier_name"),
                    "Status": ("str", "status"),
                    "Total": ("float", "total"),
                    "Items": ("str", "items")}
     },
    "customers":
    {"options": ["Return to the main menu",
                 "View customer list",
                 "Create a new customer",
                 "Update an existing customer",
                 "Delete customer",
                 "Export data",
                 "Import data"],
        "columns": {"id": ("int", "id"),
                    "Customer name": ("str", "customer_name"),
                    "Address": ("str", "customer_address"),
                    "Phone": ("str", "customer_phone")}
     }
}

SELECT_ORDER_QUERY = '''SELECT o.id AS order_id, c.customer_name AS customer_name, c.customer_address AS customer_address,
c.customer_phone AS customer_phone, cr.courier_name AS courier_name, o.status AS status, SUM(p.product_price) AS total
FROM customers c
JOIN orders o
ON o.customer_id = c.id
LEFT JOIN couriers cr
ON o.courier_id = cr.id
LEFT JOIN order_items oi
ON oi.Order_id = o.id
LEFT JOIN products p
ON p.id = oi.product_id
GROUP BY o.id'''

SELECT_ORDER_PRODUCTS_QUERY = '''SELECT o.id AS order_id, p.product_name, p.product_price
FROM products p
LEFT JOIN order_items oi
ON p.id = oi.product_id
JOIN orders o 
ON o.id = oi.order_id'''

SELECT_ALL_PRODUCTS = "SELECT * FROM products"
SELECT_ALL_COURIERS = "SELECT * FROM couriers"
SELECT_ALL_CUSTOMERS = "SELECT * FROM customers"
SELECT_ALL_ORDERS = "SELECT * FROM orders"

INSERT_PRODUCT = "INSERT INTO products (product_name, product_price, product_qty) VALUES (%s, %s, %s)"
INSERT_COURIER = "INSERT INTO couriers (courier_name, courier_phone) VALUES (%s, %s)"
INSERT_CUSTOMER = "INSERT INTO customers (customer_name, customer_address, customer_phone) VALUES (%s, %s, %s)"
INSERT_ORDER = "INSERT INTO orders (customer_id, courier_id, status) VALUES (%s, %s, %s)"

PLEASE_ENTER_AN_OPTION = "Please enter an option: "


def main_menu():
    clear_console()
    while True:
        print_list(main_menu_options)
        options_input = input(PLEASE_ENTER_AN_OPTION)
        if options_input == "0":
            cursor.close()
            connection.close()
            print("Exiting program")
            break
        elif options_input == "1":
            product_menu("products")
        elif options_input == "2":
            courier_menu("couriers")
        elif options_input == "3":
            customer_menu("customers")
        elif options_input == "4":
            order_menu("orders")
        else:
            clear_console()
            print_invalid()
            continue


def product_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input(PLEASE_ENTER_AN_OPTION)
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list(SELECT_ALL_PRODUCTS),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                INSERT_PRODUCT, get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list(SELECT_ALL_PRODUCTS),
                        categories[category]["columns"].keys())
            update_sql_row(SELECT_ALL_PRODUCTS,
                           categories[category]["columns"], "products")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list(SELECT_ALL_PRODUCTS),
                        categories[category]["columns"].keys())
            delete_sql_row(SELECT_ALL_PRODUCTS, "products")
            continue_func()
        elif submenu_opt_input == "5":
            export_table(get_sql_list(SELECT_ALL_PRODUCTS),
                         categories[category]["columns"].keys())
        elif submenu_opt_input == "6":
            import_table(
                INSERT_PRODUCT, "res/products_upload.csv")
            print_table(get_sql_list(SELECT_ALL_PRODUCTS),
                        categories[category]["columns"].keys())
            continue_func()


def courier_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input(PLEASE_ENTER_AN_OPTION)
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list(SELECT_ALL_COURIERS),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                INSERT_COURIER, get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list(SELECT_ALL_COURIERS),
                        categories[category]["columns"].keys())
            update_sql_row(SELECT_ALL_COURIERS,
                           categories[category]["columns"], "couriers")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list(SELECT_ALL_COURIERS),
                        categories[category]["columns"].keys())
            delete_sql_row(SELECT_ALL_COURIERS, "couriers")
            continue_func()
        elif submenu_opt_input == "5":
            export_table(get_sql_list(SELECT_ALL_COURIERS),
                         categories[category]["columns"].keys())
        elif submenu_opt_input == "6":
            import_table(
                INSERT_COURIER, "res/couriers_upload.csv")
            print_table(get_sql_list(SELECT_ALL_COURIERS),
                        categories[category]["columns"].keys())
            continue_func()


def customer_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input(PLEASE_ENTER_AN_OPTION)
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                INSERT_CUSTOMER, get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                        categories[category]["columns"].keys())
            update_sql_row(SELECT_ALL_CUSTOMERS,
                           categories[category]["columns"], "customers")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                        categories[category]["columns"].keys())
            delete_sql_row(SELECT_ALL_CUSTOMERS, "customers")
            continue_func()
        elif submenu_opt_input == "5":
            export_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                         categories[category]["columns"].keys())
        elif submenu_opt_input == "6":
            import_table(
                INSERT_CUSTOMER, "res/customers_upload.csv")
            print_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                        categories[category]["columns"].keys())
            continue_func()


def order_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        order_opt_input = input(PLEASE_ENTER_AN_OPTION)
        clear_console()
        if order_opt_input == "0":
            break
        elif order_opt_input == "1":
            print_table(get_sql_order_list(),
                        categories[category]["columns"].keys())
            continue_func()
        elif order_opt_input == "2":
            get_user_input_order()
            continue_func()
        elif order_opt_input == "3":
            print_table(get_sql_order_list(),
                        categories[category]["columns"].keys())
            update_order_status()
            continue_func()
        elif order_opt_input == "4":
            print_table(get_sql_order_list(),
                        categories[category]["columns"].keys())
            update_order(SELECT_ALL_ORDERS, SELECT_ALL_CUSTOMERS,
                         SELECT_ALL_COURIERS, SELECT_ALL_PRODUCTS)
            continue_func()
        elif order_opt_input == "5":
            print_table(get_sql_order_list(),
                        categories[category]["columns"].keys())
            delete_sql_row(SELECT_ALL_ORDERS, "orders")
            continue_func()
        elif order_opt_input == "6":
            export_table(get_sql_order_list(),
                         categories[category]["columns"].keys())


def get_sql_list(sql_command: str) -> list:
    cursor.execute(sql_command)
    rows = cursor.fetchall()
    return rows


def export_table(rows: list, columns: list):
    file_name = input_str("Enter file name: ")
    with open(f"res/{file_name}.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


def import_table(sql_command: str, file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            execute_sql(sql_command, row)


def print_sql_order_item(order_id: int):
    order_rows = get_sql_order_list()
    for row in order_rows:
        if row[0] == order_id:
            print_table([row], categories["orders"]["columns"].keys())


def get_sql_order_list() -> list:
    cursor.execute(SELECT_ORDER_QUERY)
    order_rows = cursor.fetchall()
    cursor.execute(SELECT_ORDER_PRODUCTS_QUERY)
    product_rows = cursor.fetchall()
    products = dict()
    for product in product_rows:
        if product[0] in list(products.keys()):
            products[product[0]].append(product[1])
        else:
            products[product[0]] = [product[1]]
    order_rows = [list(order) for order in order_rows]
    for order in order_rows:
        order.append([])
    for order in order_rows:
        for k, v in products.items():
            if k == order[0]:
                order[-1].extend(v)
    return order_rows


def print_table(rows: list, columns: list):
    data = dict()
    columns = list(columns)
    for idx in range(len(columns)):
        data[columns[idx]] = [row[idx] for row in rows]
    df = pd.DataFrame.from_dict(data)
    df.index = df.index + 1
    print(df.loc[:, df.columns != 'id'])


def get_user_input(columns: dict) -> list:
    val = []
    for k, v in list(columns.items()):
        if k == "id":
            continue
        if v[0] == "float":
            new_val = input_float(f"Enter {k.lower()}: ")
        elif v[0] == "int":
            new_val = input_int(f"Enter {k.lower()}: ")
        else:
            if "phone" in v[1]:
                new_val = sort_phone(input_str(f"Enter {k.lower()}: "))
            else:
                new_val = input_str(f"Enter {k.lower()}: ").title()
        val.append(new_val)
    return val


def get_idx_input(rows: list, input_text: str):
    while True:
        position = input_int(input_text) - 1
        if position in range(len(rows)):
            return rows[position][0]
        else:
            print_invalid()


def stock_decrease(product_id: int):
    product_row = get_sql_list(
        f"SELECT product_qty FROM products WHERE id = {product_id}")
    execute_sql_no_commit(
        "UPDATE products SET product_qty = %s WHERE id = %s", (product_row[0][0]-1, product_id))


def stock_increase(product_id: int):
    product_row = get_sql_list(
        f"SELECT product_qty FROM products WHERE id = {product_id}")
    execute_sql_no_commit(
        "UPDATE products SET product_qty = %s WHERE id = %s", (product_row[0][0]+1, product_id))


def get_user_input_order():
    customer_rows = get_sql_list(SELECT_ALL_CUSTOMERS)
    print_table(customer_rows, categories["customers"]["columns"].keys())
    cust_id = get_idx_input(customer_rows, "Enter customer number: ")

    courier_rows = get_sql_list(SELECT_ALL_COURIERS)
    print_table(courier_rows, categories["couriers"]["columns"].keys())
    cour_id = get_idx_input(courier_rows, "Enter courier number: ")

    status = status_list[0]
    execute_sql_no_commit(
        INSERT_ORDER, [cust_id, cour_id, status])
    last_row_id = cursor.lastrowid

    product_rows = get_sql_list(SELECT_ALL_PRODUCTS)
    print_table(product_rows, categories["products"]["columns"].keys())

    is_product_added = False
    while True:
        prod_position = input_int("Enter product number or 0 to exit: ") - 1
        if prod_position < 0:
            break
        elif prod_position in range(len(product_rows)):
            prod_id = product_rows[prod_position][0]
            execute_sql_no_commit("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", [
                last_row_id, prod_id])
            stock_decrease(prod_id)
            is_product_added = True
            print("Added. Anything else?")
        else:
            print_invalid()
    if is_product_added:
        connection.commit()
    else:
        connection.rollback()


def update_order_status():
    position = input_int("Enter order number: ") - 1
    order_rows = get_sql_list(SELECT_ALL_ORDERS)
    if position in range(len(order_rows)):
        oder_id = order_rows[position][0]
        print_list(status_list)
        while True:
            status_idx = input_int("Enter new status number: ")
            if status_idx in range(len(status_list)):
                execute_sql(
                    f"UPDATE orders SET status = '{status_list[status_idx]}' WHERE id = {oder_id}", [])
                print("Updated!")
                break
            else:
                print_invalid()
    else:
        print_invalid()


def get_update_input(rows: list, category: str, column: str, order_id: int):
    while True:
        position = input(
            f"\nEnter new {category} number or press ENTER to skip: ")
        if position == "":
            break
        try:
            position = int(position) - 1
            if position in range(len(rows)):
                new_id = rows[position][0]
                execute_sql(
                    f"UPDATE orders SET {column} = %s WHERE id = %s ", [new_id, order_id])
                print("Updated!")
                break
        except Exception as e:
            print(f"An error occured: {e}")
            print_invalid()


def update_order(sql_command_ord, sql_command_cust, sql_command_cour, sql_command_prod):
    order_rows = get_sql_list(sql_command_ord)
    order_id = get_idx_input(order_rows, "\nEnter order number: ")
    clear_console()
    print_sql_order_item(order_id)
    print()
    customer_rows = get_sql_list(sql_command_cust)
    print_table(get_sql_list(SELECT_ALL_CUSTOMERS),
                categories["customers"]["columns"].keys())
    get_update_input(customer_rows, "customer", "customer_id", order_id)
    courier_rows = get_sql_list(sql_command_cour)
    print_table(get_sql_list(SELECT_ALL_COURIERS),
                categories["couriers"]["columns"].keys())
    get_update_input(courier_rows, "courier", "courier_id", order_id)
    clear_console()
    print_sql_order_item(order_id)
    choice = input(
        "\nDo you want to replace products for this order? (y/n): ").lower()
    if choice == "n":
        return
    elif choice == "y":
        prod_ids = [id for id in get_sql_list(
            f"SELECT product_id FROM order_items WHERE order_id = {order_id}")]
        for id in prod_ids:
            stock_increase(id[0])
        execute_sql_no_commit(
            f"DELETE FROM order_items WHERE order_id = {order_id}", [])
        product_rows = get_sql_list(sql_command_prod)
        print_table(get_sql_list(SELECT_ALL_PRODUCTS),
                    categories["products"]["columns"].keys())
        while True:
            prod_position = input_int(
                "Enter product number or 0 to exit: ") - 1
            if prod_position < 0:
                break
            elif prod_position in range(len(product_rows)):
                prod_id = product_rows[prod_position][0]
                execute_sql_no_commit("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", [
                    order_id, prod_id])
                is_product_added = True
                stock_decrease(prod_id)
                print("Added. Anything else?")
            else:
                print_invalid()
            if is_product_added:
                connection.commit()
            else:
                connection.rollback()
    else:
        print_invalid()


def sort_phone(phone_num):
    if phone_num == "":
        return ""
    else:
        return "+44" + " " + phone_num[-10:-5] + " " + phone_num[-5:]


def execute_sql(sql_command: str, values: list):
    try:
        cursor.execute(sql_command, values)
        connection.commit()
    except pymysql.err.IntegrityError:
        print_duplicate()


def execute_sql_no_commit(sql_command: str, values: list):
    try:
        cursor.execute(sql_command, values)
    except pymysql.err.IntegrityError:
        print_duplicate()


def update_sql_row(sql_command: str, columns: dict, table_name: str):
    rows = get_sql_list(sql_command)
    position = input_int(
        "\nEnter position you want to update or 0 to exit: ") - 1
    if position in range(len(rows)):
        id = rows[position][0]
        for k, v in list(columns.items()):
            if k == "id":
                continue
            while True:
                if "phone" in v[1]:
                    new_val = sort_phone(
                        input(f"Enter {k.lower()} or press ENTER to skip: "))
                else:
                    new_val = input(
                        f"Enter {k.lower()} or press ENTER to skip: ").title()
                if new_val != "":
                    sql = f"UPDATE {table_name} SET {v[1]} = '{new_val}' WHERE id = {id}"
                    try:
                        execute_sql(sql, [])
                        break
                    except pymysql.err.DataError:
                        print_invalid()
                else:
                    break
    elif position < 0:
        return
    else:
        print_invalid()


def delete_sql_row(sql_command: str, table_name: str):
    rows = get_sql_list(sql_command)
    while True:
        position = input_int(
            "\nEnter position you want to delete or 0 to exit: ") - 1
        if position in range(len(rows)):
            id = rows[position][0]
            sql = f"DELETE FROM {table_name} WHERE id = {id}"
            execute_sql(sql, [])
            print("Deleted!")
            return
        elif position < 0:
            return
        else:
            print_invalid()


def clear_console():
    os.system("clear")


def continue_func():
    continue_action = input("\nPress ENTER to continue: ")


def print_invalid():
    print("Not a valid option")


def print_duplicate():
    print("Already exists! Data has not been updated.")


def print_list(item_list: list):
    for index, item in enumerate(item_list):
        print(index, item)
    print("")


if __name__ == '__main__':
    main_menu()
