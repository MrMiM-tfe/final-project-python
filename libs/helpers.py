import os
from libs.colors import colors as c

class ExitException(Exception):
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ex_input(prompt):
    v = input(prompt)
    if v == "exit":
        raise ExitException()
    return v

def safe_input(prompt, condition, error_message):
    while True:
        try:
            value = ex_input(prompt)
            if condition(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print(c.a("Invalid input. Please enter a valid value.", c.fg.red))

