import subprocess
import re
import csv
import datetime
from helper_tools import user_data, misc


# The Campus_groups class poll GAM for the campus groups, then assignes them as values to a numeric key
class Campus_groups:
    def __init__(self):
        ...

    # The groups_dict method in production will poll GAM for the campus groups
    # Put the stdout into a file, then read the file to create the desired dictionary
    def groups_dict(self):
        self.group_dict = {}
        # Open the group_data file for reading
        with open("needed_files/groups", mode="w") as write_file:
            data_file = subprocess.Popen(["gam", "print", "groups"], stdout=write_file)
            data_file.wait()

        with open("needed_files/groups", mode="r") as self.csv_file_read:
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
        assign = False

        # Take user input of the keys for which groups are needed.
        ## NOTE strip out whitespace incase user inputs spaces and use regex to check input
        while assign == False:
            group_wanted = input(
                """\nPlease enter the numbers of the groups
    the user will need be a member of: (Comma seperated: ex. 1,2,3)\n"""
            )
            group_wanted = group_wanted.replace(" ", "")
            group_wanted = group_wanted.split(",")
            for i in range(0, len(group_wanted)):
                if group_wanted[0] != "":
                    if str(group_wanted[i]) not in campus_groups:
                        print(
                            "Invalid entry, please try again! (Enter 1-"
                            + str(len(campus_groups))
                            + ")"
                        )
                        break
                    else:
                        # Append each needed group to the assigned groups list
                        assigned_groups.append(campus_groups.get(group_wanted[i]))
                elif group_wanted[0] == "":
                    assigned_groups.append("NO GROUPS")
                    break
                else:
                    break
            if len(assigned_groups) == len(group_wanted):
                break

        return cls(assigned_groups, account_type)


class Add_to_group:
    def __init__(self, groups, account_type):
        self.groups = groups
        # Open up the needed file
        with open(str(account_type) + "/" + str(account_type) + ".txt") as self.file:
            self.reader = csv.reader(self.file, delimiter=":")
            # Loop through each row
            for row in self.reader:
                # Loop through each inde of the groups list
                for x in range(0, len(self.groups)):
                    try:
                        self.command = (
                            "gam update group " + self.groups[x] + " add user " + row[0]
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
        self.sed_params = "s,$,:" + self.wanted_ou + ","
        self.temp_file = (
            str(self.account_type) + "/" + "temp_" + str(self.account_type) + ".txt"
        )
        self.awk_file = str(self.account_type) + "/" + str(self.account_type) + ".txt"
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
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org \'"$5"\' && sleep 2"}'

        # Set dry run command for user to preview the command
        self.dry_run = subprocess.Popen(
            ["awk", "-F:", self.awk_line, self.awk_file], stdout=subprocess.PIPE
        )
        # Read the dry run command
        self.gam_command = str(self.dry_run.stdout.read().decode())
        print(self.gam_command)

        while True:
            yn = input("Does the above command look correct? y/n ").lower()
            if not re.search(r"^(y|n)$", yn):
                print("Invalid response please enter 'y' or 'n'")
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
    filepath = account_type + "/" + account_type + ".txt"
    x = datetime.datetime.now()
    log_file_name = (
        "logs/"
        + account_type
        + "-accounts"
        + "-"
        + str(x.year)
        + str(x.month)
        + str(x.day)
        + str(x.hour)
        + str(x.minute)
        + str(x.second)
    )
    create_log = subprocess.Popen(
        ["cp", filepath, log_file_name], stdout=subprocess.PIPE
    )
    create_log.wait()


def main():
    # Clear the screen
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    # Call the Account_type class from the user_script module
    account_type = user_data.Account_type.get()
    # Run the Campus_OUs class to get the OUs available in the campus and save the return to variable
    campus_OUs = misc.Campus_OUs().ou_dict(account_type)
    # Call the dict_print function to print the desired dictionary
    misc.Dict_Print(campus_OUs)
    # Run the Assign_OU class and assign the return to variable
    OU = misc.Assign_OU(None).get(campus_OUs)
    # Run the Create_Account class to create the account
    Create_Account(account_type, OU)
    # Run the Campus_groups class to get available groups in the campus
    campus_groups = Campus_groups().groups_dict()
    misc.Dict_Print(campus_groups)
    # Run the Assign groups class to assign the user to the desired groups
    Assign_groups.get(campus_groups, account_type)
    # Write the log file
    log_file(account_type)

    while True:
        # Check if user wants to perform more actions and if so, restart this tool
        restart = input(
            "Account creations and group additions sucessfull. Would you like to create more accounts? y/n "
        ).lower()
        if not re.search(r"^(y|n)$", restart):
            print("Invalid response please enter 'y' or 'n'")
        else:
            break
    if str(restart) == "y":
        # Restart this tool
        main()
    else:
        misc.exit_message()


if __name__ == "__main__":
    main()
