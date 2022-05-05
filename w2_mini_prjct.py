import os

main_manu_options = ["Exit", "Products", "Couriers"]

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
                        "Delete courier"]}
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
            delete_list_item(category_file, "Please enter a position you want to delete: ")
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
        item_not_found()


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
        item_not_found()
    


def clear_console():
    os.system("clear")


def continue_func():
    continue_action = input("Press ENTER to continue: ")


def print_valid():
    print("Not a valid option :( \n")


def item_not_found():
    print("File has not been found.")


def print_list(item_list):
    for index, item in enumerate(item_list):
        print(index, item)
    print("")


if __name__ == '__main__':
    main_manu()
