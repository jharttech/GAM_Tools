import sys
import csv
import re
import subprocess


# The Account_type class simply asks the user whether the user wants to use
# Staff data or student data and returns the user input as a string.
class Account_type:
    def __init__(self, account):
        self.dict = {"1": "student", "2": "staff", "3": "exit"}

        self.a_type = self.dict.get(account)
        if self.a_type == "exit":
            sys.exit("You have chosen to exit.")

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
                print(f"Please enter 1, 2, or 3")
            else:
                return cls(account)


# The Stage_csv class ultimately returns a list of values for
# The data to be composed into a file, the name of the output file, and the type of account
# Data that is being worked with
class Stage_csv:
    # Set inital class variables
    def __init__(self, account_type):
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
            print(f"made it to staff account type")
            self.i_filename = "full_staff.csv"
            self.o_filename = "fullStaff.csv"
            self.notes = "EMPLOYEE"
        elif self.account_type == "student":
            print(f"Made it to student account type")
            self.i_filename = "full_student.csv"
            self.o_filename = "fullStudent.csv"
            self.notes = "Initial Import"
        else:
            raise ValueError("Invalid account type!")

    # stage class method handles the reading of the input file and sorting the data into
    # a list of rows to be written to a file later
    def stage(
        self,
    ):
        with open(f"needed_file/{self.i_filename}", mode="r") as self.csv_file:
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
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    # Keep count of each row
                    self.line_count += 1
                else:
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
                            f"Error with primaryEmail field, please check the 'needed_file/{self.i_filename}'"
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
                        sys.exit(f"Error getting needed fields for csv row")

            if len(self.lines) > 2:
                return [self.lines, self.o_filename, self.account_type]
            else:
                sys.exit(f"Error: no {self.account_type} data to add. Exiting now...")


# The Compose class simply composes a file that can then be moved or reused for further
# Data manipulation
class Compose:
    def __init__(self, staged_data):
        self.o_filename = staged_data[1]
        self.lines = staged_data[0]
        with open(f"needed_file/{self.o_filename}", mode="w") as self.csv_file:
            for i in range(0, len(self.lines)):
                self.full = csv.writer(self.csv_file, delimiter=",")
                self.full.writerow(self.lines[i])


# The Building_names class creates a list of building names and returns the list
class Building_names:
    def __init__(self, staged_data):
        self.building_list = []
        self.temp_building = []
        self.o_filename = staged_data[1]
        self.num = None

        # self.buildings(self,staged_data[2],staged_data[1])

    def buildings(self):
        with open(f"needed_file/{self.o_filename}", mode="r") as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=",")
            self.line_count = 0
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        if (column_name := str(row[x])) == "Location":
                            self.num = x
                            self.line_count += 1
                else:
                    self.temp_building = row[self.num].split("/")
                    if (
                        self.temp_building[len(self.temp_building) - 1]
                        not in self.building_list
                    ):
                        self.building_list.append(
                            self.temp_building[len(self.temp_building) - 1]
                        )
        return self.building_list


# The Building class show the user a list of building names and asks which building the
# User would like data from.
class Building:
    def __init__(self, building):
        self.building = building

    def __str__(self):
        return self.building

    @classmethod
    def get(cls, building_list):
        buildings = building_list
        # Add the ALL option the the list of buildings in case the user wants data from
        # all buildings
        buildings.append("ALL")
        while True:
            for l in range(len(buildings)):
                print(buildings[l])
            building = input(
                f"Please enter the building of data wanted: "
            )
            if building not in buildings:
                print("Invalid Building")
            else:
                return cls(building)


# The Sort_students class is used if the user wants to sort students based on a particular
# Building.  Then creates a csv of the data for that building.
class Sort_students:
    def __init__(self, building, i_filename):
        self.building = building
        self.i_filename = i_filename

    def sort(self):
        # Open the needed csv in read mode
        with open(f"{self.i_filename}", mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader(self.csv_file_read, delimiter=",")
            self.line_count = 0
            self.lines = []
            # Get the number of columns in the csv
            self.n_cols = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            for row in self.csv_reader:
                # Keep count of the rows
                if self.line_count == 0:
                    for x in range(0, self.n_cols):
                        # Keep track of what column has the header of Location
                        if (column_name := str(row[x])) == "Location":
                            self.num = x
                    # Append the header row to the lines list
                    self.lines.append(row)
                    self.line_count += 1
                # If the row is not the header and its building is the desired building then
                # Start logic block
                elif (self.line_count != 0) and (row[self.num].__contains__(str(self.building))):
                    self.temp_building = row[self.num].split("/")
                    self.temp_building = self.temp_building[len(self.temp_building) - 1]
                    # Make sure the row does coincide with the desired building
                    if str(self.temp_building) == str(self.building):
                        self.lines.append(row)
                else:
                    continue
        # Write the data to the desired location and file
        with open(f"student/{self.building}.csv", mode="w") as self.csv_file_write:
            for i in range(0, len(self.lines)):
                self.o_file = csv.writer(self.csv_file_write, delimiter=",")
                self.o_file.writerow(self.lines[i])


# The move_file function moves the created files to where they need to go
def move_file(staged_data):
    filename = f"needed_file/{staged_data[1]}"
    destination = f"{staged_data[2]}/{staged_data[1]}"

    # Nested function to reduce reduntant code
    def moved():
        # Move the wanted file to its final destination
        subprocess.Popen(["mv", filename, destination], stdout=subprocess.PIPE)
        return f"All {staged_data[2]} has been compiled into ..ChromebookCheckoutTool/{destination}"

    if staged_data[2] == "staff":
        # Move the staff data file to its destination
        print(moved())
    elif staged_data[2] == "student":
        # Call the Building_names class to get a list of possible buildings
        building_names = Building_names(staged_data).buildings()
        # Pass the list of possible buildings to the Building class get method to allow the
        # User to state which building they want
        building = Building.get(building_names)
        if str(building) != "ALL":
            # If the user did not chose ALL buildings, then sort the student data based on
            # Users desired building
            Sort_students(building, filename).sort()
            print(
                f"All {staged_data[2]} in {building} has been compiled into ..ChromebookCheckoutTool/{staged_data[2]}/{building}.csv"
            )
        else:
            # If user wanted student data from ALL buildings then do not sort the data, instead
            # Write the file of all the student data and move it to its destination.
            print(moved())
    else:
        sys.exit(
            f"No Data to work with or move, please check original data source needed_file/{staged_data[1]}"
        )


# Main function in case this script is called independently of the main create_account.py program
def main():
    account_type = Account_type.get()
    staged = Stage_csv(account_type).stage()
    Compose(staged)
    move_file(staged)


# Check to see if script was called directly
if __name__ == "__main__":
    main()
