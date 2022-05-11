import os
import json


main_manu_options = ["Exit", "Products", "Couriers", "Orders"]
status_list = ["Preparing", "Out for delivery", "Delivered"]


script_dir = os.path.dirname(__file__)
categories = {
    "product":
        {"path": os.path.join(script_dir, "res/products.txt"),
         "options": ["Return to the main menu",
                     "View product list",
                     "Create a new product",
                     "Update an existing product",
                     "Delete product"]},
    "courier":
    {"path": os.path.join(script_dir, "res/couriers.txt"),
            "options": ["Return to the main menu",
                        "View courier list",
                        "Create a new courier",
                        "Update an existing courier",
                        "Delete courier"]},
    "order":
    {"path": os.path.join(script_dir, "res/orders.json"),
            "options": ["Return to the main menu",
                        "View orders list",
                        "Create a new order",
                        "Update order status",
                        "Update an existing order",
                        "Delete order"]}
}


def main_manu():
    clear_console()
    while True:
        print_list(main_manu_options)
        options_input = input("Please enter an option: ")
        if options_input == "0":
            print("Exiting program")
            break
        elif options_input == "1":
            sub_manu("product", categories["product"]["path"])
        elif options_input == "2":
            sub_manu("courier", categories["courier"]["path"])
        elif options_input == "3":
            order_manu("order", categories["order"]["path"])
        else:
            clear_console()
            print_valid()
            continue


def sub_manu(category, category_file):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        submenu_opt_input = input("Please enter an option: ")
        clear_console()
        if submenu_opt_input == "0":
            break
        elif submenu_opt_input == "1":
            print_list(read_file(category_file))
            continue_func()
        elif submenu_opt_input == "2":
            add_new_list_item(
                category_file, f"Please enter a new {category} name: ")
            continue_func()
        elif submenu_opt_input == "3":
            print_list(read_file(category_file))
            update_list_item(category_file, f"Enter number of the {category} you want to update: ",
                             f"Please enter a new {category} name: ")
            continue_func()
        elif submenu_opt_input == "4":
            print_list(read_file(category_file))
            delete_list_item(
                category_file, "Please enter a position you want to delete: ")
            continue_func()


def order_manu(category, category_file):
    while True:
        clear_console()
        print_list(categories[category]["options"])
        order_opt_input = input("Please enter an option: ")
        clear_console()
        if order_opt_input == "0":
            break
        elif order_opt_input == "1":
            print_list_dictioneries(read_json_file(category_file))
            continue_func()
        elif order_opt_input == "2":
            add_new_dict_item(category_file, create_order_dict(category_file))
            continue_func()
        elif order_opt_input == "3":
            update_dict(
                category_file, f"Enter {category} number : ", "Enter new status option ")
            continue_func()
        elif order_opt_input == "4":
            print_list_dictioneries(read_json_file(category_file))
            update_order_dict(category_file, "Enter order number: ")
            continue_func()
        elif order_opt_input == "5":
            print_list_dictioneries(read_json_file(category_file))
            delete_dict(category_file, "Enter order number: ")
            continue_func()


def read_file(file_name) -> list[str]:
    try:
        with open(file_name, "r") as file:
            result = [line.strip() for line in file]
            return result
    except IOError as e:
        return []


def save_to_file(file_name, item_list):
    with open(file_name, "w") as file:
        for i in item_list:
            file.write(i + '\n')


def read_json_file(file_name):
    try:
        with open(file_name, "r+") as file:
            result = json.load(file)
            return result
    except:
        return []


def is_duplicate(item_list, item) -> bool:
    if item in item_list:
        return True


def add_new_list_item(file_name, input_text):
    new_item_name = input(input_text).title()
    if is_duplicate(read_file(file_name), new_item_name):
        print("Item already exists.")
        return
    try:
        with open(file_name, "a") as file:
            file.write(new_item_name + "\n")
            print("New item has been created.")
    except:
        file_not_found()


def create_order_dict(file_name) -> dict:
    new_order_dict = dict()
    new_order_dict["id"] = order_id_increment(file_name)
    new_order_dict["customer_name"] = input("Enter customer name: ").title()
    new_order_dict["customer_address"] = input(
        "Enter customer address: ").title()
    new_order_dict["customer_phone"] = input("Enter customer phone: ").title()
    couriers = read_file(categories["courier"]["path"])
    print_list(couriers)
    new_order_dict["courier"] = input("Enter courier number: ")
    new_order_dict["status"] = status_list[0]
    return new_order_dict


def update_order_dict(file_name, text1) -> dict:
    data = read_json_file(file_name)
    try:
        idx = int(input(text1)) - 1
    except:
        print_valid()
        return
    if idx in range(len(data)):
        for key in data[idx].keys():
            if key == "id":
                continue
            new_value = input(
                f"Enter new {key} or press ENTER to skip: ").title()
            if new_value == '':
                continue
            else:
                data[idx][key] = new_value
    else:
        print_valid()
        return
    load_list_to_json(file_name, data)


def add_new_dict_item(file_name, dictionery):
    data = read_json_file(file_name)
    data.append(dictionery)
    load_list_to_json(file_name, data)


def load_list_to_json(file_name, data):
    try:
        with open(file_name, "w+") as file:
            result = json.dump(data, file, indent=4)
            return result
    except IOError:
        file_not_found()


def update_list_item(file_name, input_text1, input_text2):
    try:
        position = int(input(input_text1))
    except ValueError:
        print_valid()
        return
    items = read_file(file_name)
    if position < len(items) and position >= 0:
        new_item_input = input(input_text2).title()
        if is_duplicate(items, new_item_input):
            print("Item already exists.")
        else:
            items[position] = new_item_input
            save_to_file(file_name, items)
            print("The item has been updated.")
    else:
        print_valid()


def update_dict(file_name, input_text1, input_text2):
    data = read_json_file(file_name)
    try:
        order_id = int(input(input_text1))
    except:
        print_valid()
        return
    if 0 < order_id <= len(data):
        for dictionery in data:
            if dictionery["id"] == order_id:
                print_dict(dictionery)
                print_list(status_list)
                try:
                    status_idx = int(input(input_text2))
                    if 0 <= status_idx < len(status_list):
                        dictionery["status"] = status_list[status_idx]
                        load_list_to_json(file_name, data)
                except:
                    print_valid()
                    return
    else:
        print_valid()
        return


def delete_list_item(file_name, input_text):
    try:
        position = int(input(input_text))
        items = read_file(file_name)
        if position < len(items) and position >= 0:
            items.remove(items[position])
            save_to_file(file_name, items)
            print("The item has been deleted.")
        else:
            print_valid()
    except ValueError:
        print_valid()
    except IOError:
        file_not_found()


def delete_dict(file_name, text1):
    data = read_json_file(file_name)
    try:
        idx = int(input(text1)) - 1
    except:
        print_valid()
        return
    if idx in range(len(data)):
        data.pop(idx)
    else:
        print_valid()
        return
    load_list_to_json(file_name, data)


def clear_console():
    os.system("clear")


def continue_func():
    continue_action = input("Press ENTER to continue: ")


def print_valid():
    print("Not a valid option :( \n")


def file_not_found():
    print("File has not been found.")


def order_id_increment(file_name) -> int:
    try:
        data = read_json_file(file_name)
        next_id = int(data[len(data)-1]["id"]) + 1
        return next_id
    except:
        return 1


def print_list(item_list):
    for index, item in enumerate(item_list):
        print(index, item)
    print("")


def print_list_dictioneries(list_dict: list):
    try:
        for item in list_dict:
            print_dict(item)
    except:
        print(list_dict)


def print_dict(dict):
    for k, v in dict.items():
        if k == "id":
            print(v)
        else:
            print(f'{k}: {v}')
    print()


if __name__ == '__main__':
    main_manu()
