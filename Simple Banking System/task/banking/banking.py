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
        try:
            current_number = None
            cur.execute("SELECT number FROM card WHERE number = ? AND pin = ?", (num_card, pin_card))
            current_number = cur.fetchone()
            conn.commit()
            if current_number == None:
                return False
            else:
                self.number = current_number[0]
            return True
        except ValueError:
            return False

    def check_card_dest(self, card_transfer):
        card_ok = None
        cur.execute("SELECT number FROM card WHERE number=?", (card_transfer,))
        card_ok = cur.fetchone()
        conn.commit()
        if card_ok == None:
            return False
        else:
            return True


    def add_income(self, money):
        self.balance += money
        cur.execute("UPDATE card SET balance=? WHERE number=?", (self.balance, self.number))
        conn.commit()

    def do_transfer(self, money_transfer, account):
        if self.balance < money_transfer:
            print("Not enough money!")
        else:
            cur.execute("UPDATE card SET balance=? WHERE number=?", (money_transfer, account))
            cur.execute("UPDATE card SET balance=? WHERE number=?", (self.balance - money_transfer, self.number))
            conn.commit()
            print("Success!")

    def check_money(self):
        print(self.number)
        cur.execute("SELECT balance FROM card WHERE number=?", (self.number,))
        money_box = cur.fetchone()
        print(money_box)
        conn.commit()
        self.balance = money_box[0]

    # Method to close the current account
    def close_account(self):
        print(self.number)
        cur.execute("DELETE FROM card WHERE number=?", (self.number,))
        conn.commit()

# Luhn algorithm to check if card number is correct
def luhn_algorithm(number_card):
    step_1 = number_card[:len(number_card) - 1]

    # Multiply odd digits by 2. Take into account the list start with 0, so you will get even indexes
    step_2 = [int(num) * 2 if i == 0 or i % 2 == 0 else int(num) for i, num in enumerate(step_1)]

    # Substract 9 to numbers over 9
    step_3 = [int(num) - 9 if num > 9 else num for num in step_2]

    # Add all numbers
    step_3.append(int(number_card[len(number_card) - 1]))

    # Sum the numbers and check the mod
    if sum(step_3) % 10 == 0:
        return True
    else:
        return False

def check_balance():
    option_balance = None
    while option_balance != 0:
        print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        option_balance = int(input())
        if option_balance == 0:
            return False

        if option_balance == 1:
            card.check_money()
            print(f"\nBalance: {card.balance}")

        if option_balance == 2:
            print("Enter income:")
            money = int(input())
            card.add_income(money)
            print("Income was added!")

        if option_balance == 3:
            print("\nTransfer")
            print("Enter card number")
            card_transfer = input()

            if luhn_algorithm(card_transfer) == False:
                print("Probably you made a mistake in the card number. Please try again!")
            elif card.number == card_transfer:
                print("You can't transfer money to the same account!")
            elif card.check_card_dest(card_transfer):
                print("Enter how much money you want transfer:")
                money_transfer = int(input())
                card.do_transfer(money_transfer, card_transfer)
            else:
                print("Such a card does not exist.")



        if option_balance == 4:
            card.close_account()
            print("The account has been closed!")
            break

        if option_balance == 5:
            print("\nYou have successfully logged out!")
            break

option = None
card = CreditCard()
id_card = 1
while option != 0:
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    option = int(input())

    if option == 1:
        card.random_values()
        while (luhn_algorithm(card.number) == False):
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

