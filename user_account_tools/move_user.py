import sys
import subprocess
import csv
import create_account

def get_current_ou():
    user_account = input("What user would you like to move? (Only username needed) ")
    user_info = subprocess.Popen(["gam", "info", "user", user_account], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    user_current_ou = subprocess.Popen(["grep", "Google Org Unit Path"], stdin=user_info.stdout, stdout=subprocess.PIPE)
    result = ("Users current " + str(user_current_ou.stdout.read().decode().strip()))
    return result


def move_user():
    while True:
        new_ou = input("What Org Unit would you like the user to be moved into? (Please provide full path) ")
        #if str(new_ou) not in 



def main():
    current_ou = get_current_ou()
    print(current_ou)
    if "Student" in current_ou:
        account_type = "student"
    else:
        account_type = "staff"
    #Campus_OUs().ou_dict(account_type)
    #move_user()
    print(account_type)


if __name__ == "__main__":
    main()