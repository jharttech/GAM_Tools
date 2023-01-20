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
        self.account_types = ["staff", "student"]
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
                f"{str(self.account_types[i])}/{str(self.account_types[i])}.txt"
            )
            # Create the empty file
            subprocess.Popen(["touch", self.n_file], stdout=subprocess.DEVNULL)
        subprocess.Popen(
            ["mkdir", "logs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


# Defind the exit_message function to be called any time the program is asked or wants to close.
def exit_message():
    print("Terminating Program at this time.  Thank you! --JHart")
