import csv
import subprocess

# The Compose class simply composes a file that can then be moved or reused for further
# Data manipulation
class Compose:
    def __init__(self, staged_data):
        # Set output filename
        self.o_filename = staged_data[1]
        self.lines = staged_data[0]
        # Open file for writing
        with open("needed_files/" + self.o_filename, mode="w") as self.csv_file:
            for i in range(0, len(self.lines)):
                self.full = csv.writer(self.csv_file, delimiter=",")
                self.full.writerow(self.lines[i])


# Define the Dict_Print class to print dictionary keys and values in numerical order.  This is not natively done in python3.4
class Dict_Print:
    def __init__(self, data):
        self.data = data
        self.data_list = list(map(int, self.data))
        self.data_list = sorted(self.data_list)
        print("\n")
        for i in range(0, len(self.data)):
            print(
                str(self.data_list[i]) + " : " + self.data.get(str(self.data_list[i]))
            )


# Define the Setup class so when the tool starts it makes sure all needed directories and files exist
class Setup:
    def __init__(self):
        self.account_types = ["staff", "student", "cart_device_data"]
        # Create a directory with the account type the user chose
        for i in range(0, len(self.account_types)):
            subprocess.Popen(
                ["mkdir", self.account_types[i]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Assign the new file and path to a variable
            # n_file = f"{account_type}/{account_type}.txt"
            self.n_file = (
                str(self.account_types[i]) + "/" + str(self.account_types[i]) + ".txt"
            )
            # Create the empty file
            subprocess.Popen(["touch", self.n_file], stdout=subprocess.DEVNULL)
        subprocess.Popen(
            ["mkdir", "logs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        with open("needed_files/org_units", mode="w") as write_file:
            data_file = subprocess.Popen(["gam", "print", "orgs"], stdout=write_file)
            data_file.wait()

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
        elif str(self.account_type) == "student":
            self.ou_type = "Students"
        elif str(self.account_type) == "Chromebooks":
            self.ou_type = "Chromebooks"

        self.org_unit_dict = {}

        with open("needed_files/org_units", mode="r") as self.csv_file_read:
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


# Defind the exit_message function to be called any time the program is asked or wants to close.
def exit_message():
    print("Terminating Program at this time.  Thank you! --JHart")
