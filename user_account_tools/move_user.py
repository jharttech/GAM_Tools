import sys
import subprocess
import csv
from user_account_tools import create_account
from helper_tools import misc

def get_current_ou():
    user_account = input("What user would you like to move? (Only username needed) ")
    user_info = subprocess.Popen(["gam", "info", "user", user_account], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    user_current_ou = subprocess.Popen(["grep", "Google Org Unit Path"], stdin=user_info.stdout, stdout=subprocess.PIPE)
    result = ("Users current " + str(user_current_ou.stdout.read().decode().strip()))
    return result,user_account

def move_user(campus_OUs,user):
    while True:
        new_ou = input("What Org Unit would you like the user to be moved into? ")
        if str(new_ou) not in campus_OUs:
            # If user input was not in the numeric keys, prompt them to enter a number
            # Between 1 and the length of the dictionary
            print("Invalid entry, please try again! (Enter 1-" + str(len(campus_OUs)) + ")")
        else:
            ou = campus_OUs.get(new_ou)
            break
    move = subprocess.Popen(["gam","update","user",user,"org",str(ou)], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    move.wait()
    print(move)


def main():
    try:
        current_ou = get_current_ou()
        print(current_ou[0])
        if "Student" in current_ou[0]:
            account_type = "student"
        else:
            account_type = "staff"
        campus_OUs = create_account.Campus_OUs().ou_dict(account_type)
        misc.Dict_Print(campus_OUs)
        move_user(campus_OUs,current_ou[1])
    except:
        print("Unknown error.  Please try again")
        main()
    print("User has been moved to the " + current_ou[0] + ". Thank you! -JHart")



if __name__ == "__main__":
    main()