import subprocess
from user_account_tools import create_account
from helper_tools import misc


# Define the function to get the users current Org Unit
def get_current_ou():
    # Ask what user to be moved
    user_account = input(f"What user would you like to move? (Only username needed) ")
    # Get the wanted users full info
    user_info = subprocess.Popen(
        ["gam", "info", "user", user_account],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Get the wanted users Org Unit
    user_current_ou = subprocess.Popen(
        ["grep", "Google Org Unit Path"], stdin=user_info.stdout, stdout=subprocess.PIPE
    )
    result = (
        f"\nUsers current {str(user_current_ou.stdout.read().decode().strip())}\n"
    )
    return result, user_account


# Define the function to move the wanted user to the new Org Unit
def move_user_ou(campus_OUs, user):
    while True:
        # Ask for what Org Unit the wanted user should be moved into
        new_ou = input(f"\nWhat Org Unit would you like the user to be moved into? ")
        # Check to make sure the input was valid
        if str(new_ou) not in campus_OUs:
            # If user input was not in the numeric keys, prompt them to enter a number
            # Between 1 and the length of the dictionary
            print(
                f"Invalid entry, please try again! (Enter 1-{str(len(campus_OUs))})"
            )
        else:
            ou = campus_OUs.get(new_ou)
            break
    # Move the wanted user into the new Org Unit
    move = subprocess.Popen(
        ["gam", "update", "user", user, "org", str(ou)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    move.wait()
    print(f"\n{move.stdout.read().decode().strip()}")
    return ou


def main():
    try:
        # run the get_current_ou function and assign the result to variable
        current_ou = get_current_ou()
        # Inform program user what Org Unit the wanted user is currently in
        print(current_ou[0])
        # Determines what type of account the wanted user is
        if "Student" in current_ou[0]:
            account_type = "student"
        else:
            account_type = "staff"
        # Pull the Org Units available for the account type 
        campus_OUs = create_account.Campus_OUs().ou_dict(account_type)
        # Print the Org Units available
        misc.Dict_Print(campus_OUs)
        # Run the move_user_ou function and assign result to variable
        ou = move_user_ou(campus_OUs, current_ou[1])
    except:
        # IF error is encountered restart the program
        print(f"Unknown error.  Please try again")
        main()
    print(f"\nUser has been moved to the {ou} OU.")
    misc.exit_message()


if __name__ == "__main__":
    main()
