from libs.panels.panel import Panel
from libs.helpers import safe_input, ex_input
from libs.menu_option import MenuOption
from libs.colors import colors as c

class NormalPanel(Panel):
    main_menu = MenuOption("Main Menu", "page", options=[
        MenuOption("Check balance", "action", action="check_balance"),
        MenuOption("Transfer", "action", action="transfer"),
        MenuOption("Change Password", "action", action="change_password"),
        MenuOption("Apply For A Loan", "action", action="apply_for_loan"),
    ])
    
    current_menu = main_menu
    current_command_input = "Enter option: "

    def __init__(self, user, bank):
        super().__init__(user)
        self.bank = bank

    def _show_menu(self):
        print(c.a("User Panel", c.bg.green) + c.a(" [exit] to logout" if self.current_menu.type == "page" else "", c.fg.red))
        print(self.current_menu)
        return self.current_command_input
    
    def check_balance(self):
        self.user.balance -= 1000
        print(f"Your balance is: {self.user.balance} RIL")
        input("Press Enter to continue...")
    
    def transfer(self):
        while True:
            query = ex_input("Enter card number or username: ")
            user = self.bank.get_user_by_card_number(query) or self.bank.get_user_by_username(query)
            if not user:
                print("User not found!")
                continue
            if user.username == self.user.username:
                print("You cannot transfer money to yourself!")
                continue
            while True:
                amount = int(safe_input("Enter amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
                if amount + self.bank.min_balance > self.user.balance:
                    print("Insufficient balance!")
                    continue
                self.user.balance -= amount
                user.balance += amount
                print(f"Transferred {amount} RIL to {user.username}")
                print(f"Your balance is: {self.user.balance} RIL")
                input("Press Enter to continue...")
                return
            
    def change_password(self):
        old_password = safe_input("Enter old password: ", lambda x: x == self.user.password, "Invalid password")
        new_password = safe_input("Enter new password: ", lambda x: len(x) >= 4, "Password must be at least 4 characters")
        self.user.password = new_password
        print("Password changed successfully!")
        input("Press Enter to continue...")

    def apply_for_loan(self):
        amount = int(safe_input("Enter loan amount: ", lambda x: x.isdigit() and int(x) > 0, "Invalid amount"))
        self.bank.new_loan(amount, self.user)
        print("Loan applied successfully!")
        print("waiting for admin approval...")
        input("Press Enter to continue...")
