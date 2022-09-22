import random
import string
import datetime

class BankAccount(object):

    def __init__(self, acc_name, age, IBAN, pin, acc_number, funds):
        self.acc_name = acc_name
        self.age = age
        self.IBAN = IBAN
        self.pin = pin
        self.acc_number = acc_number
        self.funds = funds

    def withdraw(self, amount):

        if amount <= 0:
            print("You can only withdraw a positive value")
            return

        transaction = ("withdraw", amount)
        self.transactions.append(transaction)

        self.funds -= amount

    def deposit(self, amount):

        if amount <= 0:
            print("You can only deposit a positive value")
            return

        self.funds += amount

    def transfer(self, amount):

        if amount <= 0:
            print("You can only transfer a positive amount")
            return

        self.funds -= amount

    #provide account details if user wishes to view them
    def __str__(self):
        result =  "Unique ID:        " + account[0][0] + "\n"
        result +=  "Account Name:    " + self.acc_name + "\n"
        result += "Holder's age:    " + self.age + "\n"
        result += "IBAN:            " + self.IBAN + "\n"
        result += "Account number:  " + str(self.acc_number) + "\n"
        result += "Funds:            " + str(self.funds) + "\n"

        return result


class CheckingsAccount(BankAccount):

    def __init__(self, acc_name, age, IBAN, pin, acc_number, funds, minimum_balance=-1000):
        BankAccount.__init__(self, acc_name, age, IBAN, pin, acc_number, funds)
        #users may withdraw even in the negatives up to -1000
        self.minimum_balance = minimum_balance

    def __str__(self):
        return_str = BankAccount.__str__(self)
        return_str += "Minimum balance:  " + str(self.minimum_balance)
        return return_str

    def withdraw(self, amount):

        if amount <= 0:
            print("You can only withdraw a positive value")
            return
        #warn user that they are in the negatives
        if self.funds < 0:
            print("WARNING: Your balance is currently in the negatives")
            print("Maximum negative balance is " + str(self.minimum_balance))

        if self.funds - amount < self.minimum_balance:
            print("Sorry, you can't withdraw that much")
            return
        
        self.funds -= amount


class SavingsAccount(BankAccount):

    def __init__(self, acc_name, age, IBAN, pin, acc_number, funds, minimum_balance=0):
        BankAccount.__init__(self, acc_name, age, IBAN, pin, acc_number, funds)
        self.minimum_balance = minimum_balance

    def __str__(self):
        return_str = BankAccount.__str__(self)
        return_str += "Minimum balance: " + str(self.minimum_balance)
        return return_str

    def withdraw(self, amount):

        if amount <= 0:
            print("You can only withdraw a positive value")
            return

        if self.funds - amount < self.minimum_balance:
            print("Sorry, you can't withdraw that much")
            return
        
        #get the current month and year and check if there's already a transaction made this month
        time = datetime.datetime.now()
        current_month = time.strftime("%B")
        current_year = time.strftime("%Y")

        with open("transactions.txt", "r") as file:
            for line in file:
                data = file.readlines()

        #if there is a transaction found for this month, tell user and return
        for line in data:
            if(account[0][0] in line):
                if(current_month in line and current_year in line and 'withdrawn' in line):
                    print("Sorry, saving accounts are limited to 1 withdrawal each month")
                    return

        self.funds -= amount


def menu():
    choice = 0

    #display a simple menu
    while True:
        print("***********************************")
        print("Choose an option and hit enter\n")
        print("1: View account details")
        print("2: Withdraw / Deposit")
        print("3: View transactions")
        print("4: Transfer funds")
        print("5: Delete an account")
        print("6: Log out -> []\n")

        #try and prevent any unexpected input
        try:
            choice = int(input())
        except:
            choice = 0
            print("Please choose a valid option")
        if choice > 6:
            choice = 0
            print("Please choose a valid option")

        if(choice == 1):
            print(openAcc)
        elif(choice == 2):
            accountOperation()
        elif(choice == 3):
            viewTransactions()
        elif(choice == 4):
            transferFunds()
        elif(choice == 5):
            deleteAcc()
            return
        elif(choice == 6):
            return


def addTransaction(choice, amount):
    #to get the data and time of transaction
    time = datetime.datetime.now()

    #add a new transaction withs its date and type
    with open("transactions.txt", "a") as file:
        if(choice == 1):
            transaction_type = 'withdrawn'
            file.write(account[0][0] + "-" + "Successfully " + transaction_type + " " + amount + " at " + (time.strftime("%Y-%B-%d %H:%M:%S")) + "\n")
        elif(choice == 2):
            transaction_type = 'deposited'
            file.write(account[0][0] + "-" + "Successfully " + transaction_type + " " + amount + " at " + (time.strftime("%Y-%B-%d %H:%M:%S")) + "\n")
        elif(choice == 3):
            transaction_type = 'transferred'
            file.write(account[0][0] + "-" + "Successfully " + transaction_type + " " + amount + " at " + (time.strftime("%Y-%B-%d %H:%M:%S")) + "\n")
    return


def createAccount():
    print("\n")
    print("***********************************")

    choice = 0
    print("Please choose an account type\n")
    print("1: Checking account")
    print("2: Savings Account")

    #try and prevent any unexpected input
    try:
        choice = int(input())
    except:
        choice = 0
        print("Please choose a valid option")
        return
    if choice > 2:
        choice = 0
        print("Please choose a valid option")
        return

    if(choice == 1):
        Type = "Checking"
    elif(choice == 2):
        Type = "Savings"

    FirstName = input("First Name: ")
    Surname = input("Surname: ")
    AccountName = FirstName + ' ' + Surname + ' ' + Type
    Age = input("Age: ")
    Pin = int(input("Please choose a 4 number pin: "))

    #check if they are over the age of 18 first
    if(int(Age) < 18 and Type == "Checking"):
        print("Sorry, you must be 18 or over to open a checking account")
        return

    #genrate a unique ID using random
    uniqueID = random.choice(string.ascii_uppercase) + str(random.randint(1000, 9999))
    IBAN = "IE" + str(random.randint(100000000, 999999999))
    AccNo = str(random.randint(100000000, 999999999))

    #give the user some account details
    print("Your account name is ", AccountName)
    print("Your unique ID is ", uniqueID)
    print("Your IBAN is: ", IBAN)

    #put down a new customer into the file
    with open("customers.txt", "a") as file:
        file.write(uniqueID + ', ' + AccountName + '\n')

    #put down a new account into the file
    with open("accounts.txt", "a") as file:
        file.write(uniqueID + ', ' + AccountName + ', ' + Age + ', ' + IBAN + ', ' + str(Pin) + ', ' + AccNo + ', ' + '0, ' + '\n')
        
    return


def accountOperation():

    accountFile = open("accounts.txt", "r")
    
    funds = openAcc.funds
    print("You currently have", funds, " funds in your account")

    choice = 0
    print("Please choose and option")
    print("1: Withdraw")
    print("2: Deposit")
    print("3: Return\n")

    while True:
        #try and prevent any unexpected input
        try:
            choice = int(input())
        except:
            choice = 0
            print("Please choose a valid option")
        if choice > 2:
            choice = 0
            print("Please choose a valid option")

        #choice to withdraw
        if(choice == 1):
            amount = input("Amount to withdraw: ")
            openAcc.withdraw(int(amount))
            newAmount = openAcc.funds
            newLine = line.replace(account[0][6], str(newAmount), 1)
            #take all the lines from accounts.txt
            with open("accounts.txt", "r") as file:
                data = file.readlines()
            #replace the line with the opened account
            data[line_num] = newLine
            newData = open("accounts.txt", "w")
            newData.writelines(data)
            #close all files
            accountFile.close()
            newData.close()
            addTransaction(choice, amount)
            break
        #choice to deposit
        elif(choice == 2):
            amount = input("Amount to deposit: ")
            openAcc.deposit(int(amount))
            newAmount = openAcc.funds
            newLine = line.replace(account[0][6], str(newAmount), 1)
            #take all the lines from accounts.txt
            with open("accounts.txt", "r") as file:
                data = file.readlines()
            #replace the line with the opened account
            data[line_num] = newLine
            newData = open("accounts.txt", "w")
            newData.writelines(data)
            #close all files
            accountFile.close()
            newData.close()
            addTransaction(choice, amount)
            break
        elif(choice == 3):
            return
    return


def viewTransactions():
    #open file and check for all transactions with the same ID
    with open("transactions.txt", "r") as file:
        for line in file:
            if(account[0][0] in line):
                print(line)

def transferFunds():

    accountFile = open("accounts.txt", "r")

    funds = openAcc.funds
    print("You currently have", funds, " funds in your account")

    print("Would you like to transfer funds?")
    print("1: YES")
    print("2: NO")

    #try and prevent any unexpected input
    try:
        choice = int(input())
    except:
        choice = 0
        print("Please choose a valid option")
    if choice > 2:
        choice = 0
        print("Please choose a valid option")
    
    if(choice == 2):
        return

    otherAccIBAN = input("Please enter the IBAN of the recipients account: ")
    otherAcc = []
    line_num2 = 0

    for line2 in accountFile:
        if(otherAccIBAN in line2):

            #open recipients bank account
            otherAcc.append(line2.split(','))
            if('Checking' in line2):
                otherOpenAcc = otherAcc[0][0]
                otherOpenAcc = CheckingsAccount(otherAcc[0][1],otherAcc[0][2],otherAcc[0][3],otherAcc[0][4],otherAcc[0][5],int(otherAcc[0][6]))
            elif('Savings' in line2):
                otherOpenAcc = otherAcc[0][0]
                otherOpenAcc = SavingsAccount(otherAcc[0][1],otherAcc[0][2],otherAcc[0][3],otherAcc[0][4],otherAcc[0][5],int(otherAcc[0][6]))
            amount = input("Please enter how much you wish to transfer: ")

            #withdraw amount from bank account
            openAcc.transfer(int(amount))
            newAmount = openAcc.funds
            newLine = line.replace(account[0][6], str(newAmount), 1)
            #take all the lines from accounts.txt
            with open("accounts.txt", "r") as file:
                data = file.readlines()
            #replace the line with the opened account
            data[line_num] = newLine
            newData = open("accounts.txt", "w")
            newData.writelines(data)
            newData.close()

            #deposit amount to other account
            otherOpenAcc.deposit(int(amount))
            #update text file
            newAmount2 = otherOpenAcc.funds
            newLine2 = line2.replace(otherAcc[0][6], str(newAmount2), 1)
            #take all the lines from accounts.txt
            with open("accounts.txt", "r") as file2:
                data2 = file2.readlines()
            #replace the line with the opened account
            data2[line_num2] = newLine2
            newData2 = open("accounts.txt", "w")
            newData2.writelines(data2)
            newData2.close()

            #close all files
            accountFile.close()
            addTransaction(3, amount)

            #can't call addTransaction function as my variables are local
            with open("transactions.txt", "a") as file:
                #to get the data and time of transaction
                time = datetime.datetime.now()
                file.write(otherAcc[0][0] + "-" + "Successfully " + "Received"+ " " + amount + " at " + (time.strftime("%Y-%m-%d %H:%M:%S")) + "\n")

            break
        line_num2 += 1
    else:
        print("No such account ID, please try again")
        return
    
    return

def deleteAcc():

    confirm = 0
    print("Are you sure you want to close this account?")

    while True:
        print("1: YES")
        print("2: NO")

        try:
            confirm = int(input())
        except:
            confirm = 0
            print("Please choose a valid option")
        if(confirm > 2):
            print("Please choose a valid option")

        #reconfirm user if they wish to delete their account
        if(confirm == 1):
            print("WARNING: Are you sure you wish to close this account?")
            print("1: YES")
            print("2: NO")

            #try and prevent any unexpected input
            try:
                confirm = int(input())
            except:
                confirm = 0
                print("Please choose a valid option")
            if(confirm > 2):
                print("Please choose a valid option")

            #make sure user has withdrawn all funds first
            if(openAcc.funds != 0):
                print("Please withdraw any remaining funds first")
                return
            #else delete
            else:
                #delete from accounts file
                with open("accounts.txt", "r") as file:
                    data = file.readlines()
                with open("accounts.txt", "w") as file:
                    for line in data:
                        if(line != data[line_num]):
                            file.write(line)

                #delete from customer file
                with open("customers.txt", "r") as file:
                    data = file.readlines()
                with open("customers.txt", "w") as file:
                    for line in data:
                        if(line != data[line_num]):
                            file.write(line)

                print("Account has been closed successfully")
        elif(confirm == 2):
            return

        return

        
#first menu, login or create an account
choice = 0

while True:
    print("***********************************")
    print("1: Login to an account")
    print("2: Create an account")

    #try and prevent any unexpected input
    try:
        choice = int(input())
    except:
        choice = 0
        print("Please choose a valid option")
    if(choice > 2):
        print("Please choose a valid option")

    if(choice == 1):
        accountFile = open("accounts.txt", "r")
        account = []
        line_num = 0

        accID = input("Please enter the account's unique ID: ")
        checkPin = input("Please enter the 4-pin: ")

        #check if theres an account with the ID and password
        for line in accountFile:
            if accID in line and checkPin in line:
                account.append(line.split(','))
                #close accountfile
                accountFile.close()

                #use the information to create an instance

                #open using checking subclass
                if('Checking' in line):
                    print("Opening checking account...\n")
                    openAcc = account[0][0]
                    openAcc = CheckingsAccount(account[0][1],account[0][2],account[0][3],account[0][4],account[0][5],int(account[0][6]))
                    menu()
                #open using savings subclass
                elif('Savings' in line):
                    print("Opening savings account...\n")
                    openAcc = account[0][0]
                    openAcc = SavingsAccount(account[0][1],account[0][2],account[0][3],account[0][4],account[0][5],int(account[0][6]))
                    menu()
                break
            line_num += 1
        else:
            print("Details maybe incorrect, please try again")

    elif(choice == 2):
        createAccount()