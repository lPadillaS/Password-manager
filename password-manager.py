import sqlite3
import pyjokes
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
                    new_account = input("What is the new account?:\n").lower()
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
                    read_account = input("What account would you like to see? (leave empty to see all):\n")
                    if read_account:
                        cur.execute("SELECT password FROM passwords WHERE account_name = ?", (read_account, ))
                        reading = cur.fetchall()
                        print(f"password: {reading[0][0]}")
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
    return True
def configureManager():
    ...
    
if __name__ == "__main__":
    main()
    
