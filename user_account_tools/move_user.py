import sys
import subprocess
import csv


def move_user():
    user_account = input("What user would you like to move? (Only username needed) ")
    user_info = subprocess.Popen(["gam", "info", "user", user_account], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    user_current_ou = subprocess.Popen(["grep", "Google Org Unit Path"], stdin=user_info.stdout, stdout=subprocess.PIPE)
    result = str(user_current_ou.stdout.read().decode().strip())
    return result


def main():
    print(move_user())


if __name__ == "__main__":
    main()