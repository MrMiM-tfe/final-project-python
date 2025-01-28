class User:
    def __init__(self, name, lastname, username, password):        
        self.name = name
        self.lastname = lastname
        self.username = username
        self.password = password

class CustomerUser(User):
    def __init__(self, name, lastname, username, password, card_number, balance):
        super().__init__(name, lastname, username, password)
        self.is_admin = False
        self.card_number = card_number
        self.balance = balance

    def __str__(self):
        return f"{self.name} {self.lastname} ({self.username}):\n\tCard Number: {self.card_number}\n\tBalance: {self.balance}"

class AdminUser(User):
    def __init__(self, name, lastname, username, password):
        super().__init__(name, lastname, username, password)
        self.is_admin = True
