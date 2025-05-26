# A complicated way to do a simple assignment

'''
Assignment
- You have $50
- You buy an item that is $15
- With a text of 3%
- Print how much money you have left
'''

class wallet():
    
    def __init__(self, balance = 0):
        ''' Instantiates the wallet class '''
        self.wallet_balance = balance
    
    def make_purchase(self, price, rate):
        ''' Evaluates Tax Amount, Total Amount to be Paid and makes purchase if balance is sufficient'''
        tax_amount = self.tax_value_per_item(rate, price)
        total_pay = tax_amount + price
        if self.wallet_balance >= total_pay:
            self.wallet_balce = self.wallet_balance - total_pay
            print(f"Transaction of {price} USD and tax amount of {tax_amount} succesful, your new balance is {self.wallet_balce} USD")
        else:
            print(f'Insufficient Account Balance')
            
    def tax_value_per_item(self, rate, price):
        '''Evaluate the tax per item'''
        tax_amount = (rate / 100) * price
        return tax_amount
    
    def top_up(self, amount):
        self.wallet_balance = amount + self.wallet_balance
    
kaycodesWallet = wallet(balance=50)
kaycodesWallet.make_purchase(15, 3)