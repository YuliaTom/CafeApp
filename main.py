import os
import pymysql
import pandas as pd
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
                     "Delete product"],
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
                 "Delete courier"],
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
                 "Delete order"],
        "columns": {"id": ("int", "id"),
                    "Customer name": ("str", "customer_name"),
                    "Customer address": ("str", "customer_address"),
                    "Customer phone": ("str", "customer_phone"),
                    "Courier name": ("str", "courier_name"),
                    "Status": ("str", "status"),
                    "Items": ("str", "items")}
     },
    "customers":
    {"options": ["Return to the main menu",
                 "View customer list",
                 "Create a new customer",
                 "Update an existing customer",
                 "Delete customer"],
        "columns": {"id": ("int", "id"),
                    "Customer name": ("str", "customer_name"),
                    "Address": ("str", "customer_address"),
                    "Phone": ("str", "customer_phone")}
     }
}


def main_menu():
    clear_console()
    while True:
        print_list(main_menu_options)
        options_input = input("Please enter an option: ")
        if options_input == "0":
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
        submenu_opt_input = input("Please enter an option: ")
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list("SELECT * FROM products"),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                'INSERT INTO products (product_name, product_price, product_qty) VALUES (%s, %s, %s)', get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list("SELECT * FROM products"),
                        categories[category]["columns"].keys())
            update_sql_row("SELECT * FROM products",
                           categories[category]["columns"], "products")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list("SELECT * FROM products"),
                        categories[category]["columns"].keys())
            delete_sql_row("SELECT * FROM products", "products")
            continue_func()


def courier_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input("Please enter an option: ")
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list("SELECT * FROM couriers"),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                'INSERT INTO couriers (courier_name, courier_phone) VALUES (%s, %s)', get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list("SELECT * FROM couriers"),
                        categories[category]["columns"].keys())
            update_sql_row("SELECT * FROM couriers",
                           categories[category]["columns"], "couriers")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list("SELECT * FROM couriers"),
                        categories[category]["columns"].keys())
            delete_sql_row("SELECT * FROM couriers", "couriers")
            continue_func()


def customer_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input("Please enter an option: ")
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_table(get_sql_list("SELECT * FROM customers"),
                        categories[category]["columns"].keys())
            continue_func()
        elif submenu_opt_input == "2":
            execute_sql(
                'INSERT INTO customers (customer_name, customer_address, customer_phone) VALUES (%s, %s, %s)', get_user_input(categories[category]["columns"]))
            continue_func()
        elif submenu_opt_input == "3":
            print_table(get_sql_list("SELECT * FROM customers"),
                        categories[category]["columns"].keys())
            update_sql_row("SELECT * FROM customers",
                           categories[category]["columns"], "customers")
            continue_func()
        elif submenu_opt_input == "4":
            print_table(get_sql_list("SELECT * FROM customers"),
                        categories[category]["columns"].keys())
            delete_sql_row("SELECT * FROM customers", "customers")
            continue_func()


def order_menu(category: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        order_opt_input = input("Please enter an option: ")
        clear_console()
        if order_opt_input == "0":
            break
        elif order_opt_input == "1":
            print_table(get_sql_order_list('''SELECT o.id AS order_id, c.customer_name AS customer_name, c.customer_address AS customer_address, 
c.customer_phone AS customer_phone, cr.courier_name AS courier_name, o.status AS status
FROM customers c JOIN orders o ON o.customer_id = c.id JOIN couriers cr ON o.courier_id = cr.id''', '''SELECT o.id AS order_id, p.product_name
FROM products p
JOIN order_items oi
ON p.id = oi.product_id
JOIN orders o 
ON o.id = oi.order_id'''),
                        categories[category]["columns"].keys())
            continue_func()
        elif order_opt_input == "2":
            execute_sql(
                "INSERT INTO orders (customer_id, courier_id, status) VALUES (%s, %s, %s)", get_user_input_order())
            continue_func()
        elif order_opt_input == "3":
            print_csv_file(category_file)
            update_status_dict(
                category_file, f"Enter {category} number : ", "Enter new status option ")
            continue_func()
        elif order_opt_input == "4":
            print_csv_file(category_file)
            update_order_dict(category_file, "Enter order number: ")
            continue_func()
        elif order_opt_input == "5":
            print_csv_file(category_file)
            delete_dict(category_file, "Enter order number: ")
            continue_func()


def get_sql_list(sql_command: str) -> list:
    cursor.execute(sql_command)
    rows = cursor.fetchall()
    return rows


def get_sql_order_list(sql_command1: str, sql_command2: str) -> list:
    cursor.execute(sql_command1)
    rows = cursor.fetchall()
    cursor.execute(sql_command2)
    new_rows = cursor.fetchall()
    products = dict()
    for row in new_rows:
        if row[0] in list(products.keys()):
            products[row[0]].append(row[1])
        else:
            products[row[0]] = [row[1]]
    joined_rows = []
    for row in rows:
        row = list(row)
        for k, v in products.items():
            if k == row[0]:
                row.append(v)
                joined_rows.append(row)
    return joined_rows


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


def get_user_input_order():
    customer_rows = get_sql_list("SELECT * FROM customers")
    print_table(customer_rows, categories["customers"]["columns"].keys())
    while True:
        cust_position = input_int("Enter customer number: ") - 1
        if cust_position in range(len(customer_rows)):
            cust_id = customer_rows[cust_position][0]
            break
        else:
            print_invalid()
    courier_rows = get_sql_list("SELECT * FROM couriers")
    print_table(courier_rows, categories["couriers"]["columns"].keys())
    while True:
        cour_position = input_int("Enter courier number: ") - 1
        if cour_position in range(len(courier_rows)):
            cour_id = courier_rows[cour_position][0]
            break
        else:
            print_invalid()
    status = status_list[0]
    product_rows = get_sql_list("SELECT * FROM products")
    print_table(product_rows, categories["products"]["columns"].keys())
    prod_ids = []
    while True:
        prod_position = input_int("Enter product number: ") - 1
        if cust_position in range(len(product_rows)):
            prod_ids(product_rows[prod_position][0])
        else:
            print_invalid()

    return [cust_id, cour_id, status]


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


def is_duplicate(item_list: list[dict], item: str) -> bool:
    for dict in item_list:
        if dict["name"] == item:
            return True


def append_to_csv(file_name: str, item_list: list[str]) -> bool:
    try:
        with open(file_name, "a") as file:
            writer = csv.writer(file)
            writer.writerow(item_list)
            return True
    except:
        file_not_found()
        return False


def add_new_row_to_csv_float(file_name: str, input_text1: str, input_text2: str):
    new_val1 = input_str(input_text1).title()
    if is_duplicate(read_file(file_name), new_val1):
        print("Already exists.")
        return
    new_val2 = input_float(input_text2)
    is_added = append_to_csv(
        file_name, [new_val1, new_val2])
    if is_added:
        print("Added!")


def add_new_row_to_csv_str(file_name: str, input_text1: str, input_text2: str):
    new_val1 = input_str(input_text1).title()
    if is_duplicate(read_file(file_name), new_val1):
        print("Already exists.")
        return
    new_val2 = input_str(input_text2)
    is_added = append_to_csv(
        file_name, [new_val1, new_val2])
    if is_added:
        print("Added!")


def create_order_dict() -> dict:
    new_order_dict = dict()
    new_order_dict["customer name"] = input("Enter customer name: ").title()
    new_order_dict["customer address"] = input(
        "Enter customer address: ").title()
    new_order_dict["customer phone"] = input("Enter customer phone: ").title()
    print_csv_file(categories["product"]["path"])
    new_order_dict["items"] = input(
        "Enter products for this order separated by coma: ")
    print_csv_file(categories["courier"]["path"])
    new_order_dict["courier"] = input("Enter courier number: ")
    new_order_dict["status"] = status_list[0]
    return new_order_dict


def update_status_dict(file_name: str, input_text1: str, input_text2: str):
    dict_list = read_file(file_name)
    idx = input_int(input_text1) - 1
    if idx in range(len(dict_list)):
        print_dict(dict_list[idx])
        print_list(status_list)
        status_idx = input_int(input_text2)
        if status_idx in range(len(status_list)):
            dict_list[idx]["status"] = status_list[status_idx]
            write_to_csv(file_name, dict_list)
    else:
        print_invalid()
        return


def update_order_dict(file_name: str, input_text: str) -> dict:
    dict_list = read_file(file_name)
    idx = input_int(input_text) - 1
    if idx in range(len(dict_list)):
        for key in dict_list[idx].keys():
            if key == "items":
                print_csv_file(categories["product"]["path"])
            elif key == "courier":
                print_csv_file(categories["courier"]["path"])
            elif key == "status":
                print_list(status_list)
                try:
                    new_value = int(
                        input(f"Enter new {key} number or press ENTER to skip: "))
                    if new_value == '':
                        continue
                    elif new_value > 0:
                        dict_list[idx][key] = status_list[new_value]
                    continue
                except ValueError:
                    print_invalid()
                    continue
            new_value = input(
                f"Enter new {key} or press ENTER to skip: ").title()
            if new_value == '':
                continue
            else:
                dict_list[idx][key] = new_value
    else:
        print_invalid()
        return
    write_to_csv(file_name, dict_list)


def update_csv_file(file_name: str, input_text: str):
    position = input_int(input_text) - 1
    dict_list = read_file(file_name)
    if position < 0:
        return
    elif position < len(dict_list) and position >= 0:
        for col in dict_list[position].keys():
            new_col_input = input(
                f"Enter new {col} or press ENTER to skip: ").title()
            if new_col_input == "":
                continue
            if col == "name" and is_duplicate(dict_list, new_col_input):
                print("Already exists.")
                return
            else:
                dict_list[position][col] = new_col_input
                write_to_csv(file_name, dict_list)
        print("Updated!")
    else:
        print_invalid()


def delete_dict(file_name: str, text: str):
    dict_list = read_file(file_name)
    idx = input_int(text) - 1
    if idx in range(len(dict_list)):
        dict_list.pop(idx)
    else:
        print_invalid()
        return
    write_to_csv(file_name, dict_list)
    print("Deleted.")


def clear_console():
    os.system("clear")


def continue_func():
    continue_action = input("\nPress ENTER to continue: ")


def print_invalid():
    print("Not a valid option")


def print_duplicate():
    print("Already exists! Data has not been updated.")


def file_not_found():
    print("File has not been found.")


def print_list(item_list: list):
    for index, item in enumerate(item_list):
        print(index, item)
    print("")


def print_dict(dict: dict):
    for k, v in dict.items():
        if k == "id":
            print(v)
        else:
            print(f'{k}: {v}')
    print()


if __name__ == '__main__':
    main_menu()
