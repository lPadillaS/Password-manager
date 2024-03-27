import sqlite3
import pyjokes
import csv
from werkzeug.security import generate_password_hash, check_password_hash
db = sqlite3.connect("passwords-db/passwords.db")
cur = db.cursor()

def main():
    if checkManagerPassword():
        while True:
            action = input(
            "What would you like to do?\n'add' to add a new account\n'del'to delete an account\n'upp' to modify an account\n'read' to get an account's password\n'q' to quit\n"
            ).lower()
            match action:
                case "add":
                    new_account = input("What is the new account? (spaces will be replaced by underscores):\n").lower()
                    new_account = new_account.replace(" ", "_")
                    new_password = input("What is the password?:\n")
                    cur.execute("INSERT INTO passwords (account_name, password) VALUES (?, ?)", (new_account, new_password))
                    db.commit()
                case "del":
                    del_account = input("input the name of the account you would like to delete:\n").lower()
                    while True:
                        confirm = input("Are you sure you would like to delete this account? (yes/no):\n").lower()
                        if confirm == "yes":
                            cur.execute("DELETE FROM passwords WHERE account_name = ?", (del_account, ))
                            db.commit()
                            break
                        elif confirm == "no":
                            break
                case "upp":
                    up_account = input("Which account would you like to update?:\n").lower()
                    up_password = input("Input the new password:\n")
                    cur.execute("UPDATE passwords SET password = ? WHERE account_name = ?", (up_password, up_account))
                    db.commit()
                case "read":
                    read_account = input("What account would you like to see? (leave empty to see all):\n").lower()
                    if read_account:
                        cur.execute("SELECT password FROM passwords WHERE account_name = ?", (read_account, ))
                        reading = cur.fetchall()
                        try:
                            print(f"password: {reading[0][0]}")
                        except IndexError:
                            print(f"No {read_account} account in the database, make sure your spelling is correct")
                    else:
                        cur.execute("SELECT account_name, password FROM passwords WHERE account_id > 0")
                        reading = cur.fetchall()
                        for row in reading:
                            print(f"account: {row[0]}\npassword: {row[1]}\n---------------")
                case "q":
                    break
            print("~~~~~~~~~~~~~~~~~~~~~~")
    else:
        print("Wrong password and/or key")
def checkManagerPassword() -> bool:
    configureManager()
    check = input("What is the manager password?:\n")
    with open("manager_password.csv", 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=['password'])
        for row in reader:
            if check_password_hash(row['password'], check):
                return True
        return False
    
def configureManager():
    with open("manager_password.csv", "r+", newline='') as M_pw:
        reader = csv.DictReader(M_pw, fieldnames=['password'])
        for row in reader:
            if row['password']:
                return True
        else:
            while True:
                new_password = input("Please create a new password for your manager:\n")
                check_password = input("Please input your password again to make sure they are the same:\n")
                if new_password == check_password: 
                    password_hash = generate_password_hash(new_password, 'scrypt', 12)
                    writer = csv.DictWriter(M_pw, fieldnames=['password'])
                    writer.writerow({'password': password_hash})
                    print("Your password has been created!\n-----------------------------")
                    return True
                else:
                    print("The passwords do not match")
                
        
if __name__ == "__main__":
    main()
    
