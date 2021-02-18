# Third Stage of Credit card exercise
import random
import sqlite3

# Database connection
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("DROP TABLE card")
cur.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()
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

    # Luhn algorithm to check if card number is correct
    def luhn_algorithm(self):
        step_1 = self.number[:len(self.number) - 1]
        
        # Multiply odd digits by 2. Take into account the list start with 0, so you will get even indexes
        step_2 = [int(num) * 2 if i == 0 or i % 2 == 0 else int(num) for i, num in enumerate(step_1)]
        
        # Substract 9 to numbers over 9
        step_3 = [int(num) - 9 if num > 9 else num for num in step_2]
        
        # Add all numbers
        step_3.append(int(self.number[len(self.number) - 1]))
        
        # Sum the numbers and check the mod
        if sum(step_3) % 10 == 0:
            return True
        else:
            return False

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
id_card = 0

while option != 0:
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    option = int(input())

    if option == 1:
        card.random_values()
        while (card.luhn_algorithm() == False):
            card.random_values()
        print("\nYour card has been created\nYour card number:")
        print(card.number)
        print("Your card PIN:")
        print(card.pin)
        cur.execute("INSERT INTO card (id, number, pin) VALUES (?, ?, ?);", (id_card, card.number, card.pin))
        conn.commit()
        id_card += 1
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




