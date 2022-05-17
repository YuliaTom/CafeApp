import os
from csv_utils import *
from input_utils import *


main_menu_options = ["Exit", "Products", "Couriers", "Orders"]
status_list = ["Preparing", "Out for delivery", "Delivered"]


script_dir = os.path.dirname(__file__)
categories = {
    "product":
        {"path": os.path.join(script_dir, "res/products.csv"),
         "options": ["Return to the main menu",
                     "View product list",
                     "Create a new product",
                     "Update an existing product",
                     "Delete product"]
         },
    "courier":
    {"path": os.path.join(script_dir, "res/couriers.csv"),
            "options": ["Return to the main menu",
                        "View courier list",
                        "Create a new courier",
                        "Update an existing courier",
                        "Delete courier"]
     },
    "order":
    {"path": os.path.join(script_dir, "res/orders.csv"),
            "options": ["Return to the main menu",
                        "View orders list",
                        "Create a new order",
                        "Update order status",
                        "Update an existing order",
                        "Delete order"]
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
            sub_menu("product", categories["product"]
                     ["path"], add_new_row_to_csv_float)
        elif options_input == "2":
            sub_menu("courier", categories["courier"]
                     ["path"], add_new_row_to_csv_str)
        elif options_input == "3":
            order_menu("order", categories["order"]["path"])
        else:
            clear_console()
            print_valid()
            continue


def sub_menu(category: str, category_file: str, add_new_row_to_csv):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input("Please enter an option: ")
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_csv_file(category_file)
            continue_func()
        elif submenu_opt_input == "2":
            add_new_row_to_csv(
                category_file, f"Enter a new {category} {csv_headers(category_file)[0]}: ",
                f"Enter {csv_headers(category_file)[1]}: ")
            continue_func()
        elif submenu_opt_input == "3":
            print_csv_file(category_file)
            update_csv_file(
                category_file, f"Enter number of the {category} you want to update or 0 to exit: ")
            continue_func()
        elif submenu_opt_input == "4":
            print_csv_file(category_file)
            delete_dict(
                category_file, "Enter a position you want to delete or 0 to exit: ")
            continue_func()


def order_menu(category: str, category_file: str):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        order_opt_input = input("Please enter an option: ")
        clear_console()
        if order_opt_input == "0":
            break
        elif order_opt_input == "1":
            print_csv_file(category_file)
            continue_func()
        elif order_opt_input == "2":
            append_to_csv(category_file, create_order_dict().values())
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
        print_valid()
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
                    print_valid()
                    continue
            new_value = input(
                f"Enter new {key} or press ENTER to skip: ").title()
            if new_value == '':
                continue
            else:
                dict_list[idx][key] = new_value
    else:
        print_valid()
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
        print_valid()


def delete_dict(file_name: str, text: str):
    dict_list = read_file(file_name)
    idx = input_int(text) - 1
    if idx in range(len(dict_list)):
        dict_list.pop(idx)
    else:
        print_valid()
        return
    write_to_csv(file_name, dict_list)
    print("Deleted.")


def clear_console():
    os.system("clear")


def continue_func():
    continue_action = input("\nPress ENTER to continue: ")


def print_valid():
    print("Not a valid option :( \n")


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
