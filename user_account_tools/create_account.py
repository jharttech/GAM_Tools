import sys
import subprocess
import re
import csv
import datetime

sys.path.append("/Gam_Tools")
from user_account_tools.helper_tools import user_script



# The Setup Class creates the needed Directory and then creates an empyt file that will be needed
class Setup:
    def __init__(self, account_type):
        # Create a directory with the account type the user chose
        subprocess.Popen(["mkdir", str(account_type)], stdout=subprocess.DEVNULL)
        subprocess.Popen(["mkdir", "logs"], stdout=subprocess.DEVNULL)
        self.account_type = account_type
        # Assign the new file and path to a variable
        n_file = f"{account_type}/{account_type}.txt"
        # Create the empty file
        subprocess.Popen(["touch", n_file], stdout=subprocess.DEVNULL)


# The Campus_OUs class gathers the campus OU's and puts them into a dictionary with numeric keys
class Campus_OUs:
    # We do not need the init method for this class so we move on
    def __init__(self):
        ...

    # The ou_dict method takes only the relevant Org Units for the desired account type and
    # Assigns them to a dictionary with numeric keys
    def ou_dict(self, account_type):
        self.account_type = account_type

        if str(self.account_type) == "staff":
            self.ou_type = "Employees"
        else:
            self.ou_type = "Students"

        self.org_unit_dict = {}

        # Query for the desired OU
        with open(f"needed_files/org_units", mode = "w") as write_file:
            data_file = subprocess.Popen(["gam","print","orgs"], stdout=write_file)
            data_file.wait()

        # Read the Org units file and sort out the ones based on the type of
        # account being created
        with open(f"needed_files/org_units", mode="r") as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=",")
            # Read the number of columns
            self.n_col = len(next(self.read_file))
            # Return the reader back to start of file
            self.csv_file_read.seek(0)
            # Keep track of line
            self.line_count = 0
            # Keep track of numeric value of the key
            self.dict_key_count = 0
            for row in self.read_file:
                if self.line_count == 0:
                    # Look through columns
                    for x in range(0, self.n_col):
                        # Set the column name to the header value of each column
                        self.col_name = str(row[x])
                        # Find the number of the column that has the header name of orgUnitPath
                        if str(self.col_name) == "orgUnitPath":
                            self.num = x
                            # Increase line count
                            self.line_count += 1
                else:
                    self.line_count += 1
                    if str(self.ou_type) in row[self.num]:
                        # Increase the key count so the numeric values start at 1 and not 0
                        self.dict_key_count += 1
                        # Add the numberic key and the value to the dictionary of Org Units
                        self.org_unit_dict.update(
                            {str(self.dict_key_count): row[self.num]}
                        )

        return self.org_unit_dict


# The Assign_OU class askes the user which Org Unit they want to assign the new user(s) to.
class Assign_OU:
    def __init__(self, ou):
        self.ou = ou

    def __str__(self):
        return self.ou

    @classmethod
    # Create the get class method to take the users input
    def get(cls, ou_dict):
        # Create a loop to help with invalid inputs
        while True:
            choice = input("Please select the desired Org Unit: ")
            # Check to see if the input matches any of the keys
            if str(choice) not in ou_dict:
                # If user input was not in the numeric keys, prompt them to enter a number
                # Between 1 and the length of the dictionary
                print(f"Invalid entry, please try again! (Enter 1-{len(ou_dict)})")
            else:
                ou = ou_dict.get(choice)
                return cls(ou)


# The Campus_groups class poll GAM for the campus groups, then assignes them as values to a numeric key
class Campus_groups:
    def __init__(self):
        ...

    # The groups_dict method in production will poll GAM for the campus groups
    # Put the stdout into a file, then read the file to create the desired dictionary
    with open(f"needed_files/groups", mode = "w") as write_file:
            data_file = subprocess.Popen(["gam","print","groups"], stdout=write_file)
            data_file.wait()

    def groups_dict(self):
        self.group_dict = {}
        # Open the group_data file for reading
        with open(f"needed_files/group", mode="r") as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=",")
            # Read the number of columns
            self.n_col = len(next(self.read_file))
            # Move the reader back to the start of the file
            self.csv_file_read.seek(0)
            # Keep track of the lines
            self.line_count = 0
            # Keep count for the numeric dictionary keys
            self.dict_key_count = 0
            for row in self.read_file:
                if self.line_count == 0:
                    # Loop through the header columns
                    for x in range(0, self.n_col):
                        # Assing col_name to each header column value
                        self.col_name = str(row[x])
                        # Look for the number of the column thats header value is Email
                        if str(self.col_name) == "Email":
                            self.num = x
                            self.line_count += 1
                else:
                    self.line_count += 1
                    self.dict_key_count += 1
                    # Write the keys and values to the dictionary
                    self.group_dict.update({str(self.dict_key_count): row[self.num]})

        # Append the NO GROUPS value to the dictionary
        self.group_dict.update({str(self.dict_key_count + 1): "NO GROUPS"})

        return self.group_dict


# The Assign_groups class askes the user what groups they user needs to be a part of if
class Assign_groups:
    def __init__(self, assigned_groups, account_type):
        self.assigned_groups = assigned_groups
        self.account_type = account_type
        self.groups = assigned_groups
        if "NO GROUPS" in str(self.groups):
            return
        # start the Add_to_group Class
        Add_to_group(self.groups, self.account_type)

    @classmethod
    # Create the get method so the user can input which groups are needed for the user
    def get(cls, campus_groups, account_type):
        assigned_groups = []

        # Take user input of the keys for which groups are needed.
        ## NOTE strip out whitespace incase user inputs spaces and use regex to check input
        group_wanted = input(
            f"""\nPlease enter the numbers of the groups
the user will need be a member of: (Comma seperated: ex. 1,2,3)\n"""
        )
        group_wanted = group_wanted.split(",")
        for i in range(0, len(group_wanted)):
            # Append each needed group to the assigned groups list
            assigned_groups.append(campus_groups.get(group_wanted[i]))

        return cls(assigned_groups, account_type)


class Add_to_group:
    def __init__(self, groups, account_type):
        self.groups = groups
        # Open up the needed file
        with open(f"{account_type}/{account_type}.txt") as self.file:
            self.reader = csv.reader(self.file, delimiter=":")
            # Loop through each row
            for row in self.reader:
                # Loop through each inde of the groups list
                for x in range(0, len(self.groups)):
                    try:
                        self.command = (
                            f"gam update group {self.groups[x]} add user {row[0]}"
                        )
                        # Added the user on current row to the needed groups
                        self.run_gam = subprocess.Popen(
                            [
                                "gam",
                                "update",
                                "group",
                                str(self.groups[x]),
                                "add",
                                "user",
                                str(row[0]),
                            ],
                            stdout=subprocess.PIPE,
                        )
                        print(self.command)
                        self.run_gam.wait()
                    except FileNotFoundError as e:
                        raise (e)


class Create_Account:
    def __init__(self, account_type, wanted_ou):
        self.account_type = account_type
        self.wanted_ou = str(wanted_ou)
        # Checking for ampersand in org unit name, this will break sed if not escaped first
        if "&" in self.wanted_ou:
            # If an ampersand is found in the org unit, escape it
            self.wanted_ou = self.wanted_ou.replace("&", "\&")
        # Set the paramaters wanted for the sed command
        self.sed_params = f"s,$,:{self.wanted_ou},"
        self.temp_file = f"{self.account_type}/temp_{self.account_type}.txt"
        self.awk_file = f"{self.account_type}/{self.account_type}.txt"
        subprocess.Popen(["touch", self.temp_file], stdout=subprocess.PIPE)
        # Open the file with vim to add the desired account lines
        self.edit_file = subprocess.Popen(["vim", self.temp_file])
        self.edit_file.wait()

        # Copy the temp file to the production file
        self.copy_file(self.temp_file, self.awk_file)

        with open(self.awk_file, mode="w") as self.file:
            # Inject the Org Unit to the end of each line in the account file
            self.inject_org = subprocess.Popen(
                ["sed", "-e", self.sed_params, self.temp_file], stdout=self.file
            )
            self.inject_org.wait()
            self.inject_org.communicate()

        # Start the gam method
        self.gam(self.account_type, wanted_ou, self.awk_file)

    # The copy_file method simply copies from the temp file to the production file
    def copy_file(self, temp_file, awk_file):
        cp = subprocess.Popen(["cp", temp_file, awk_file], stdout=subprocess.PIPE)
        cp.wait()

    # The gam method handles all gam commands that are needed to create the new accounts
    def gam(self, account_type, wanted_ou, awk_file):
        self.account_type = account_type
        self.wanted_ou = str(wanted_ou)
        self.awk_file = awk_file

        if str(self.account_type) == "student":
            # Set gal to false for students so they do not show up in the directory when creating an email
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org \'"$5"\' && sleep 2"}'
        elif str(self.account_type) == "staff":
            # Set gal to true for staff so they DO show up in the directory when creating an email
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org \'"$5"\' && sleep2"}'

        # Set dry run command for user to preview the command
        self.dry_run = subprocess.Popen(
            ["awk", "-F:", self.awk_line, self.awk_file], stdout=subprocess.PIPE
        )
        # Read the dry run command
        self.gam_command = str(self.dry_run.stdout.read().decode())
        print(self.gam_command)

        while True:
            yn = input(f"Does the above command look correct? y/n ").lower()
            if not re.search(r"^(y|n)$", yn):
                print(f"Invalid response please enter 'y' or 'n'")
            else:
                break

        if yn == "n":
            # Restart the create account class
            self.__init__(account_type, wanted_ou)
        else:
            try:
                # Stage the real awk command
                self.holder = subprocess.Popen(
                    ["awk", "-F:", self.awk_line, self.awk_file], stdout=subprocess.PIPE
                )
                # Execute the awk command
                self.run = subprocess.Popen(
                    ["sh"], stdin=self.holder.stdout, stdout=subprocess.PIPE
                )
                self.run.wait()
            except FileNotFoundError as e:
                raise (e)

        # Remove the temp file
        subprocess.Popen(["rm", self.temp_file], stdout=subprocess.PIPE)


# The log_file function writes a log file or created accounts in case needing to look at
# Past account creations
def log_file(account_type):
    account_type = str(account_type)
    filepath = f"{account_type}/{account_type}.txt"
    x = datetime.datetime.now()
    log_file_name = (
        f"logs/{account_type}-{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}"
    )
    create_log = subprocess.Popen(
        ["cp", filepath, log_file_name], stdout=subprocess.PIPE
    )
    create_log.wait()


# The dict_print function simply prints dictionaries in a nice format
def dict_print(data):
    print("\n")
    [print(key, ":", value) for key, value in data.items()]


def main():
    # Clear the screen
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    data_check()
    # Call the Account_type class from the user_script module
    account_type = user_script.Account_type.get()
    # Run the Setup class
    Setup(account_type)
    # Run the Campus_OUs class to get the OUs available in the campus and save the return to variable
    campus_OUs = Campus_OUs().ou_dict(account_type)
    # Call the dict_print function to print the desired dictionary
    dict_print(campus_OUs)
    # Run the Assign_OU class and assign the return to variable
    OU = Assign_OU(None).get(campus_OUs)
    # Run the Create_Account class to create the account
    Create_Account(account_type, OU)
    # Run the Campus_groups class to get available groups in the campus
    campus_groups = Campus_groups().groups_dict()
    dict_print(campus_groups)
    # Run the Assign groups class to assign the user to the desired groups
    Assign_groups.get(campus_groups, account_type)
    # Write the log file
    log_file(account_type)

    while True:
        # Check if user wants to perform more actions and if so, restart this tool
        restart = input(
            f"Account creations and group additions sucessfull. Would you like to create more accounts? y/n "
        ).lower()
        if not re.search(r"^(y|n)$", restart):
            print(f"Invalid response please enter 'y' or 'n'")
        else:
            break
    if str(restart) == "y":
        # Restart this tool
        main()
    else:
        sys.exit("Thank you!  -Jhart")


if __name__ == "__main__":
    main()
