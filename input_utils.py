from main import print_invalid


def input_float(input_text: str) -> float:
    while True:
        try:
            user_input = float(input(input_text))
            return(user_input)
        except ValueError:
            print_invalid()


def input_int(input_text: str) -> int:
    while True:
        try:
            user_input = int(input(input_text))
            if user_input >= 0:
                return user_input
            else:
                raise ValueError
        except ValueError:
            print_invalid()


def input_str(input_text: str) -> str:
    while True:
        user_input = input(input_text)
        if user_input == "":
            print_invalid()
        else:
            return(user_input)
