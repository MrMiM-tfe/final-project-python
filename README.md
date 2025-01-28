# Python Bank Management System
*final project python class in university (2025)*

*KNTU university - Math - professor Ghazi*

This project is a command-line based bank management system. 

## Code Structure

The project is organized into several modules:

* **`main.py`**: The main entry point of the application. It initializes the bank, creates default users, and starts the interactive user interface.
* **`libs/`**: Contains the core logic and data structures of the system.
    * **`libs/user.py`**: Defines the `User`, `CustomerUser`, and `AdminUser` classes, representing different user roles within the system.
    * **`libs/loan.py`**: Defines the `Loan` class, which represents a loan application.
    * **`libs/menu_option.py`**: Defines the `MenuOption` class, used for creating interactive menus in the console.
    * **`libs/helpers.py`**: Contains helper functions for tasks like clearing the screen, handling user input, and managing exit conditions.
    * **`libs/colors.py`**: Defines the `colors` class, providing ANSI color codes for styling console output.
    * **`libs/panels/`**: Contains the panel classes for different user roles.
        * **`libs/panels/panel.py`**: Defines the base `Panel` class, providing common functionality for user panels.
        * **`libs/panels/admin_panel.py`**: Defines the `AdminPanel` class, handling administrative operations.
        * **`libs/panels/customer_panel.py`**: Defines the `NormalPanel` class (representing the customer panel), handling customer operations.


## Features

### Customer Features:

* **Check Balance:** View current account balance (with a simulated transaction fee).
* **Transfer:** Transfer funds to other users by card number or username.
* **Change Password:** Update account password.
* **Apply for Loan:** Submit a loan application for a specified amount.

### Admin Features:

* **Customer Management:**
    * Add new customers.
    * Remove existing customers.
    * List all customers.
    * Edit customer information (name, lastname, username, password, card number, balance).
* **Transactions:**
    * Make transactions between users by card number or username.
    * Deposit funds into user accounts.
    * Withdraw funds from user accounts.
* **Search:** Search for customers by name, lastname, username, or card number.
* **Bank Balance:** View the total balance of the bank.

## Usage

1.  **Run the `main.py` script.**  This will start the bank application and present the login screen.
2.  **Login** with a predefined username and password or create a new customer account via the admin panel.
    *  **Admin Login:**
        *  Username: `admin`
        *  Password: `kntu`
3.  **Navigate the menus** to perform desired operations.
4.  Type `exit` at any menu prompt to logout or exit the application.

## code explanation

in the end we do this:
```python
bank = Bank()

# register admin user with username: admin and password: kntu
bank.register_admin("John", "Doe", "admin", "kntu")

# some predefined customers to work with
bank.register_customer("Mahdi", "Khakbaz", "mahdi", "1234", 100_000_000, "11111")
bank.register_customer("Ali", "Rezaei", "ali", "1234", 100_000_000, "22222")
bank.register_customer("Mohammad", "Hosseini", "mohammad", "1234", 100_000_000, "33333")
bank.register_customer("Seyed", "Ahmadi", "seyed", "1234", 100_000_000, "44444")
bank.register_customer("Hossein", "Karimi", "hossein", "1234", 100_000_000, "55555")

bank.show_panel()
```

`show_panel` will show the login menu and ask for username and password
then the login function will check if the user is admin or customer and return the appropriate panel (`AdminPanel` or `NormalPanel`)

then we run `panel.show_panel()`
```python
def show_panel(self):
        while True:
            clear_screen()
            print(c.bg.cyan + c.bold + " Welcome to the Bank " + c.reset + c.fg.green + "\nplease login" + c.reset)
            username = input("Username: ").strip()
            password = input("Password: ")

            panel = self.login(username, password)
            if panel:
                panel.show_panel()
            else:
                print(c.fg.red + "Invalid username or password." + c.reset)
                input("Press Enter to continue...")
```

`show_panel` is implemented in the `Panel` class and it is the base class for all panels
it will clear the screen and show the menu and header and handle the commands

`_show_menu` is implemented in the inherited classes (`AdminPanel` and `NormalPanel`)

```python
class Panel:
    # ...
    def show_panel(self):
        while True:
            clear_screen()
            self._show_header()
            cmd_message = self._show_menu()
            cmd = input(cmd_message)
            if cmd == 'exit':
                break
            self._handle_command(cmd)

```

`_handle_command` will handle command dynamically based on the current menu
```python
class Panel:
    # ...
    def _handle_command(self, cmd):
            menu = self.current_menu.get_menu(cmd)
            if menu is None:
                return
            if menu.type == "page":
                self.current_menu = menu
            else:
                action_method = getattr(self, menu.action, None)
                print("type [exit] to go back")
                if callable(action_method):
                    try:
                        action_method()
                    except ExitException:
                        pass
                else:
                    print(f"Invalid action: {menu.action}")
```

### menu options
every panel has a list of `MenuOption` objects
and a `current_menu` which is the current menu
```python
class AdminPanel(Panel):
    main_menu = MenuOption("Main Menu", "page", options=[
            MenuOption("Customer Mynamenet", "page", options=[
                MenuOption("Add Customer", "action", action="add_customer"),
                MenuOption("Remove Customer", "action", action="remove_customer"),
                MenuOption("List Customers", "action", action="list_customers"),
                MenuOption("Edit Customer", "page", options=[
                    MenuOption("Edit Name", "action", action="edit_customer_name"),
                    MenuOption("Edit Lastname", "action", action="edit_customer_lastname"),
                    MenuOption("Edit Username", "action", action="edit_customer_username"),
                    MenuOption("Edit Password", "action", action="edit_customer_password"),
                    MenuOption("Edit Card Number", "action", action="edit_customer_card_number"),
                    MenuOption("Edit Balance", "action", action="edit_customer_balance")
                ]),
                MenuOption("Deposit To User", "action", action="deposit_to_user"),
                MenuOption("Withdraw From User", "action", action="withdraw_from_user"),
            ]),
            MenuOption("Make Transaction", "page", options=[
                MenuOption("By Card Number", "action", action="make_transaction_by_card_number"),
                MenuOption("By Username", "action", action="make_transaction_by_username"),
            ]),
            MenuOption("Search for customer", "action", action="search_customer"),
            MenuOption("Get Bank Balance", "action", action="get_bank_balance"),
        ])
        
    current_menu = main_menu
```

`MenuOption` is a class that represents a menu option
it has a title, a type, an action and a list of options

`type` can be `page` or `action`
and other properties are set based on the type

`parent` is set to the parent menu option if the type is `page`

`action` is set to the action method name if the type is `action`
and it will get ran by the `_handle_command` method in the `Panel` class
```python
class MenuOption:
    parent =  None

    def __init__(self, title, type, action=None, options=None, slug=None):
        self.title = title
        self.type = type
        self.slug = slug if slug else title.lower().replace(" ", "_")

        if self.type == "page":
            self.options = options
            for option in self.options:
                option.parent = self
        elif self.type == "action":
            self.action = action
        else:
            raise ValueError("Invalid menu option type")
```

i use `__str___` to print the menu options
```python
class MenuOption:
    # ...
    def __str__(self):
        # ...
```

### actions
action are methods that are called when a menu option is selected
and what they do is very self explanatory
```python
class AdminPanel(Panel):
    # ...
    def deposit_to_user(self):
        # ...
    def withdraw_from_user(self):
        # ...
    def search_customer(self):
        # ...
    def make_transaction_by_card_number(self):
        # ...
```

### helpers
#### clear screen
`clear_screen` is a helper function that clears the screen
```python
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

#### exit exception
`ExitException` is a custom exception that is raised when the user wants to exit the action this will catch in the `_handle_command` method and will go back to the menu

and i use `ex_input` for all my inputs to check if the user wants to exit the action in any moment


```python
def ex_input(prompt):
    v = input(prompt)
    if v == "exit":
        raise ExitException()
    return v
```

#### safe input
`safe_input` is a helper function that takes a prompt, a condition and an error message
and it will keep asking the user to enter a valid value until the condition is met

i used it in many places to make sure the user enters a valid value
for example:
```python
amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
```
```python
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
```

i think rest of the code is self explanatory