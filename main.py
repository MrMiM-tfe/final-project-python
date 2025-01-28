from libs.colors import colors as c
from libs.user import CustomerUser, AdminUser
from libs.helpers import clear_screen
from libs.loan import Loan
from libs.panels.admin_panel  import AdminPanel
from libs.panels.customer_panel import NormalPanel

class Bank:
    min_balance = 100_000
    loans = []

    def __init__(self):
        self.users = []

    def register_admin(self, name, lastname, username, password):
        admin = AdminUser(name, lastname, username, password)
        self.users.append(admin)

    def register_customer(self, name, lastname, username, password, balance, card_number):
        if balance < self.min_balance:
            print("Balance must be at least 100,000 RIL")
            return
        if card_number in [user.card_number for user in self.get_users()]:
            print("Card number must be unique")
            return
        customer = CustomerUser(name, lastname, username, password, card_number, balance)
        self.users.append(customer)
        
    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                if user.is_admin:
                    return AdminPanel(user, self)
                else:
                    return NormalPanel(user, self)
        return None
    
    def new_loan(self, amount, user):
        loan = Loan(amount, 0.01, user)
        self.loans.append(loan)

    def get_sorted_users(self, by):
        if by not in ["username", "name", "lastname", "balance", "card_number"]:
            print("Invalid sorting option. Please try again.")
            return None
        return sorted(self.get_users(), key=lambda user: getattr(user, by))

    def get_users(self):
        return [user for user in self.users if not user.is_admin]
    
    def search_users(self, query):
        return [user for user in self.users if query in user.username or query in user.name or query in user.lastname or (not user.is_admin and query in user.card_number)]

    def get_user_by_card_number(self, card_number):
        for user in self.get_users():
            if user.card_number == card_number:
                return user
        return None

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
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

bank = Bank()

bank.register_admin("John", "Doe", "admin", "kntu")

# some predefined customers to work with
bank.register_customer("Mahdi", "Khakbaz", "mahdi", "1234", 100_000_000, "11111")
bank.register_customer("Ali", "Rezaei", "ali", "1234", 100_000_000, "22222")
bank.register_customer("Mohammad", "Hosseini", "mohammad", "1234", 100_000_000, "33333")
bank.register_customer("Seyed", "Ahmadi", "seyed", "1234", 100_000_000, "44444")
bank.register_customer("Hossein", "Karimi", "hossein", "1234", 100_000_000, "55555")

bank.show_panel()