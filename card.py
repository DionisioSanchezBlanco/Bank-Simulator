# First Stage of Credit card exercise
import random

class CreditCard:
    def __init__(self):
        self.number = None
        self.pin = None
        self.balance = 0
        self.number_dict = {self.number: self.pin}

    def random_values(self):
        random.seed()

        # Random PIN
        self.pin = str(random.randrange(0, 9999))
        self.number = str(random.randrange(4000000000000000, 4000009999999999))

        # Add zeros to the PIN if the values is less than 1000
        # 3 -> 0003, 99 -> 0099, 112 -> 0112
        if len(self.pin) < 4:
            zeros = 4 - len(self.pin)
            self.pin = "0" * zeros + self.pin

    def check_card(self, num_card, pin_card):
        return self.number == num_card and self.pin == pin_card

def check_balance():
    option_balance = None
    while option_balance != 0:
        print("\n1. Balance\n2. Log out\n0. Exit")
        option_balance = int(input())
        if option_balance == 0:
            return False

        if option_balance == 1:
            print(f"\nBalance: {card.balance}")
            
        if option_balance == 2:
            print("\nYou have successfully logged out!")
            break            

option = None
card = CreditCard()

while option != 0:
    print("""\n1. Create an account
2. Log into account
0. Exit""")
    option = int(input())

    if option == 1:
        card.random_values()
        print("\nYour card has been created\nYour card number:")
        print(card.number)
        print("Your card PIN:")
        print(card.pin)

    if option == 2:
        print("\nEnter your card number:")
        num_card = input()
        print("Enter your PIN:")
        pin_card = input()
        if card.check_card(num_card, pin_card):
            print("\nYou have successfully logged in!")
            if check_balance() == False:
                break
        else:
            print("\nWrong card number or PIN!")

print("\nBye!")




