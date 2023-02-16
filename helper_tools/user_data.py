import sys
import csv
import re
import subprocess
import user_account_tools.create_account
from helper_tools import misc


# The Account_type class simply asks the user whether the user wants to use
# Staff data or student data and returns the user input as a string.
class Account_type:
    def __init__(self, account):
        # Define dictionary of types of accounts we use on campus
        self.dict = {"1": "student", "2": "staff", "3": "exit"}
        self.a_type = self.dict.get(account)

        if self.a_type == "exit":
            print("You have chosen to exit.")
            misc.exit_message()

    def __str__(self):
        return self.a_type

    @classmethod
    def get(cls):
        while True:
            account = input(
                "Would you like to work with: \n1 : student\n2 : staff\n3 : exit\n"
            )
            # Use regex to sanitize user input for validation
            if not re.search(r"^([1-3])$", account):
                print("Please enter 1, 2, or 3")
            else:
                return cls(account)


# Define Get_User_Data class to gather the wanted user data from the desired org unit
class Get_User_Data:
    def __init__(self, account_type, org_units, selected_ou):
        self.account_type = account_type
        self.org_units = org_units
        self.selected_ou = selected_ou
        self.selected_ou_name = self.selected_ou.split("/")
        self.selected_ou_name = self.selected_ou_name[len(self.selected_ou_name) - 1]
        self.gather_data(self.selected_ou)

    # Define gather_data method
    def gather_data(self, selected_ou):
        if str(self.account_type) == "student":
            # Open file for writing
            with open("needed_files/list_student_data.csv", mode="w") as needed_file:
                # Run GAM command to get desired user data from desired org unit
                gather = subprocess.Popen(
                    [
                        "gam",
                        "print",
                        "users",
                        "allfields",
                        "query",
                        "orgUnitPath=" + str(selected_ou),
                    ],
                    stdout=needed_file,
                )
                # Wait for the subprocess to finish as it could take some time
                gather.wait()
        elif str(self.account_type) == "staff":
            # Open file for writing
            with open("needed_files/list_staff_data.csv", mode="w") as needed_file:
                # Run GAM command to get deisred user data from desired org unit
                gather = subprocess.Popen(
                    [
                        "gam",
                        "print",
                        "users",
                        "allfields",
                        "query",
                        "orgUnitPath=" + str(selected_ou),
                    ],
                    stdout=needed_file,
                )
                # wait for subprocess to finish as it could take some time
                gather.wait()

    def __str__(self):
        return self.selected_ou_name

    @classmethod
    def get(cls, account_type, org_units):
        while True:
            wanted_ou = input("Please enter which Org Unit you want user data from: ")
            # Validate user input and if invalid ask again
            if str(wanted_ou) not in org_units:
                print(
                    "Invalid entry, please try again! (Enter 1-"
                    + str(len(org_units))
                    + ")"
                )
            else:
                # Convert user option number to the actuall org unit name
                selected_ou = str(org_units.get(str(wanted_ou)))
                break
        return cls(account_type, org_units, selected_ou)


# The Stage_csv class ultimately returns a list of values for
# The data to be composed into a file, the name of the output file, and the type of account
# Data that is being worked with
class Stage_csv:
    # Set inital class variables
    def __init__(self, account_type, selected_ou):
        self.g_headers = [
            "primaryEmail",
            "name.givenName",
            "name.familyName",
            "orgUnitPath",
        ]
        self.header_to_num = {}
        self.lines = []
        self.account_type = str(account_type)
        self.result = []

        # Set input file, output file, and notes variables based on the type of data being worked with
        if self.account_type == "staff":
            self.i_filename = "list_staff_data.csv"
            self.o_filename = str(selected_ou) + "_staff_data.csv"
            self.notes = "EMPLOYEE"
        elif self.account_type == "student":
            self.i_filename = "list_student_data.csv"
            self.o_filename = str(selected_ou) + "_student_data.csv"
            self.notes = "Initial Import"
        else:
            raise ValueError("Invalid account type!")

    # stage class method handles the reading of the input file and sorting the data into
    # a list of rows to be written to a file later
    def stage(
        self,
    ):
        # Open file for reading
        with open("needed_files/" + self.i_filename, mode="r") as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            self.line_count = 0
            self.header_row = [
                "Email",
                "First Name",
                "Last Name",
                "Location",
                "Notes",
                "Username",
            ]

            self.lines.append(self.header_row)

            # Loop over each row in the input file
            for row in self.csv_reader:
                # If it is the first row then gather the column names and put them in a
                # Dictionary that stores the column name as the key and the column number as the value
                if (self.line_count == 0) or ("primaryEmail" in row):
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    # Keep count of each row
                    self.line_count += 1
                else:
                    if "primaryEmail" not in row:
                        try:
                            # Break the email from the primaryEmail column using the @ to split as
                            # the username should not include the domain
                            self.username = row[
                                self.header_to_num.get(
                                    "primaryEmail",
                                    "Error getting header number for primaryEmail",
                                )
                            ].split("@")
                            # Drop the domain off to create a username
                            self.username = self.username[0]
                        except:
                            sys.exit(
                                "Error with primaryEmail field, please check the 'needed_files/"
                                + self.i_filename
                                + "'"
                            )
                        try:
                            # Get each value from each desired column using the column name as the key,
                            # And returning the value, which is a num, as an index for the row.
                            self.temp_row = [
                                row[
                                    self.header_to_num.get(
                                        "primaryEmail",
                                        "Error getting header number for primaryEmail",
                                    )
                                ],
                                row[
                                    self.header_to_num.get(
                                        "name.givenName",
                                        "Error getting header number for givenName",
                                    )
                                ],
                                row[
                                    self.header_to_num.get(
                                        "name.familyName",
                                        "Error getting header number for familyName",
                                    )
                                ],
                                row[
                                    self.header_to_num.get(
                                        "orgUnitPath",
                                        "Error getting header number for orgUnitPath",
                                    )
                                ],
                                self.notes,
                                self.username,
                            ]
                            self.lines.append(self.temp_row)
                        except:
                            sys.exit("Error getting needed fields for csv row")

            if len(self.lines) > 2:
                return [self.lines, self.o_filename, self.account_type]
            else:
                sys.exit(
                    "Error: no " + self.account_type + " data to add. Exiting now..."
                )


# Main function in case this script is called independently of the main create_account.py program
def main():
    account_type = Account_type.get()
    campus_OUs = misc.Campus_OUs().ou_dict(account_type)
    misc.Dict_Print(campus_OUs)
    selected_ou = misc.Assign_OU(None).get(campus_OUs)
    staged = Stage_csv(account_type, selected_ou).stage()
    misc.Compose(staged)
    misc.move_file(staged)


# Check to see if script was called directly
if __name__ == "__main__":
    main()
