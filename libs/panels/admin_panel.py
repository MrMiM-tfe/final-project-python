from libs.panels.panel import Panel
from libs.helpers import safe_input, ex_input
from libs.menu_option import MenuOption
from libs.colors import colors as c
from libs.user import CustomerUser

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
    current_command_input = "Enter option: "

    def __init__(self, user, bank):
        super().__init__(user)
        self.bank = bank

    def _show_menu(self):
        print(c.a("Admin Panel", c.bg.purple) + c.a(" [exit] to logout\n" if self.current_menu.type == "page" else "\n", c.fg.red))
        print(self.current_menu)
        return self.current_command_input
                
    def make_transaction(self, receiver_user, sender_user, amount):
        if sender_user.balance < amount + self.bank.min_balance:
            print("Insufficient balance")
            return
        sender_user.balance -= amount
        receiver_user.balance += amount
        print(f"Transaction successful. {sender_user.username} sent ${amount} to {receiver_user.username}")
        input("Press enter to continue...")
        return True
    

    # actions
    # ----------------------------------
    def deposit_to_user(self):
        while True:
            query = ex_input("Enter card number or username: ")
            user = self.bank.get_user_by_card_number(query)
            if user is None:
                user = self.bank.get_user_by_username(query)
            if user is None:
                print("User not found")
                continue
            amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
            user.balance += amount
            print(f"Deposit successful. {user.username} balance is now ${user.balance}")
            input("Press enter to continue...")
            break

    def withdraw_from_user(self):
        while True:
            query = ex_input("Enter card number or username: ")
            user = self.bank.get_user_by_card_number(query)
            if user is None:
                user = self.bank.get_user_by_username(query)
            if user is None:
                print("User not found")
                continue
            amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
            if user.balance < amount + self.bank.min_balance:
                print("Insufficient balance")
                continue
            user.balance -= amount
            print(f"Withdraw successful. {user.username} balance is now ${user.balance}")
            input("Press enter to continue...")
            break

    def search_customer(self):
        while True:
            query = ex_input("Enter query: ")
            results = self.bank.search_users(query)
            if len(results) == 0:
                print("No results found")
                continue
            for user in results:
                print(user)
        
    def make_transaction_by_card_number(self):
        card_number = safe_input("Enter sender's card number: ", lambda x: x in [user.card_number for user in self.bank.get_users()], "Card number not found")
        sender_user = self.bank.get_user_by_card_number(card_number)
        card_number = safe_input("Enter receiver's card number: ", lambda x: x in [user.card_number for user in self.bank.get_users()], "Card number not found")
        receiver_user = self.bank.get_user_by_card_number(card_number)
        while True:
            amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
            result = self.make_transaction(receiver_user, sender_user, amount)
            if result:
                break
            else:
                print("Transaction failed")

    def make_transaction_by_username(self):
        username = safe_input("Enter sender's username: ", lambda x: x in [user.username for user in self.bank.users], "Username not found")
        sender_user = self.bank.get_user_by_username(username)
        username = safe_input("Enter receiver's username: ", lambda x: x in [user.username for user in self.bank.users], "Username not found")
        receiver_user = self.bank.get_user_by_username(username)
        while True:
            amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
            result = self.make_transaction(receiver_user, sender_user, amount)
            if result:
                break
            else:
                print("Transaction failed")

    def get_bank_balance(self):
        balance = sum([user.balance for user in self.bank.get_users()])
        print(f"Bank balance: {balance} RIL")
        input("Press Enter to continue...")    

    def add_customer(self):
        name = ex_input("Enter customer name: ")
        lastname = ex_input("Enter customer lastname: ")
        username = safe_input("Enter customer username: ", lambda x: x not in [user.username for user in self.bank.users], "Username already exists")
        password = safe_input("Enter customer password: ", lambda x: len(x) > 3, "password must be at least 4 characters")
        card_number = safe_input("Enter customer card number: ", lambda x: len(x) == 5 and x not in self.bank.get_users() , "Card number must be 4 digits and unique")
        balance = float(safe_input("Enter customer balance: ", lambda x: float(x) >= self.bank.min_balance, "Balance must be at least 100,000 RIL"))
        customer = CustomerUser(name, lastname, username, password, card_number, balance)
        self.bank.users.append(customer)
        print("Customer added successfully!")
        print(customer)
        input("Press Enter to continue...")
    
    def remove_customer(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                self.bank.users.remove(user)
                print("Customer removed successfully!")
                print(user)
                ex_input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")
    
    def list_customers(self):
        for user in self.bank.get_users(): print(user)
        while True:
            sort_by = ex_input("Sort by (name, lastname, username, card_number, balance): ")
            users = self.bank.get_sorted_users(sort_by)
            if users is None: continue
            for user in users: print(user)

    # Edit Customer
    def edit_customer_name(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_name = ex_input("Enter new name: ")
                user.name = new_name
                print("Customer name updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")
    
    def edit_customer_lastname(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_lastname = ex_input("Enter new lastname: ")
                user.lastname = new_lastname
                print("Customer lastname updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")

    def edit_customer_username(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_username = safe_input("Enter new username: ", lambda x: x not in [user.username for user in self.bank.users], "Username already exists")
                user.username = new_username
                print("Customer username updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")
    
    def edit_customer_balance(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_balance = float(safe_input("Enter new balance: ", lambda x: float(x) >= self.bank.min_balance, "Balance must be at least 100,000 RIL"))
                user.balance = new_balance
                print("Customer balance updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")
    
    def edit_customer_card_number(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_card_number = safe_input("Enter new card number: ", lambda x: len(x) == 5 and x not in self.bank.get_users() , "Card number must be 4 digits and unique")
                user.card_number = new_card_number
                print("Customer card number updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")

    def edit_customer_password(self):
        username = ex_input("Enter customer username: ")
        for user in self.bank.get_users():
            if user.username == username:
                new_password = safe_input("Enter new password: ", lambda x: len(x) >= 8, "Password must be at least 8 characters")
                user.password = new_password
                print("Customer password updated successfully!")
                print(user)
                input("Press Enter to continue...")
                return
        print("Customer not found!")
        input("Press Enter to continue...")
