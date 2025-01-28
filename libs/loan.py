class Loan:
    def __init__(self, amount, interest_rate, user):
        self.amount = amount
        self.interest_rate = interest_rate
        self.user = user
        self.is_approved = False
    
    def approve(self):
        self.is_approved = True
        self.user.balance += self.amount