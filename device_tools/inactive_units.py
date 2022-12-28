import sys
import subprocess
import csv
from datetime import date
from helper_tools import csv_compose


# Get the current date in ISO format then split it on the hyphens
d = date.isoformat(date.today()).split("-")
# Take 2 years off of the current year, will probably prompt for amount of years in in
# future revision
d = int(d[0]) - 2


# Define Stage_CSV class to setup the csv data
class Stage_CSV:
    def __init__(self):
        # Set up the desired google headers
        self.g_headers = ["deviceId", "orgUnitPath", "serialNumber"]
        # Create empty dictionary
        self.header_to_num = {}
        # Create empty list for the coming lines
        self.lines = []
        # Set the input file
        self.i_filename = "full_devices.csv"
        # Set the output file
        self.o_filename = "non_active_units.csv"

    # Define the stage method
    def stage(self):
        # Open the input file for reading
        with open(f"needed_files/{self.i_filename}", mode="r") as self.csv_file_read:
            # Create a reader, replace any null bytes found in each line so the program does not error
            self.csv_reader = csv.reader(
                (line.replace("\0", "") for line in self.csv_file_read),
                self.csv_file_read,
                delimiter=",",
            )
            # Count the number of columns in the csv input file
            self.n_col = len(next(self.csv_reader))
            # Seek the reader back to the beginning of the file
            self.csv_file_read.seek(0)
            # Start line count at 0
            self.line_count = 0
            # Start the counting of dates to 0
            self.date_count = 0

            # Loop through each row
            for row in self.csv_reader:
                # Only run this logic block if we are reading the first line of the input file
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        # Set the col_name variable to the name of each column
                        self.col_name = str(row[x])
                        # Check to see if the column name is in the assigned google headers above,
                        # or if the column name is an active time date, if either then step into next if statement
                        # This has to be done due to google keeping multiple active time dates
                        if (self.col_name in self.g_headers) or (
                            (str(self.col_name).__contains__("activeTimeRanges"))
                            and (str(self.col_name).__contains__("date"))
                        ):
                            # Since one of the above it true, then we check to see if it is an active date header,
                            # if so then we append it to the google headers dictionary
                            if (
                                str(self.col_name).__contains__("activeTimeRanges")
                            ) and (str(self.col_name).__contains__("date")):
                                self.g_headers.append(self.col_name)
                            # Now wer update the header_to_num dictionary with the column name and a sequential digit
                            self.header_to_num.update({self.col_name: x})
                    # Increase count so next part of program will run
                    self.line_count += 1
                else:
                    try:
                        # Create an empty list to hold the found active dates for each unit
                        self.active_dates = []
                        # Recreate the temp_row list each iteration of this logic block
                        self.temp_row = []
                        # Loop through the google headers dictionary
                        for i in self.g_headers:
                            # If the column is an active date, then get the information and append the information to the active_dates list
                            if i.__contains__("activeTimeRanges"):
                                self.active_dates.append(
                                    row[
                                        self.header_to_num.get(
                                            i, f"Error getting header number for {i}"
                                        )
                                    ]
                                )
                            # If the column is not an active date, then get the information and append it to the temp_row list
                            else:
                                self.temp_row.append(
                                    row[
                                        self.header_to_num.get(
                                            i, f"Error getting header number for {i}"
                                        )
                                    ]
                                )
                        # Sort the active dates from oldest to most recent
                        self.active_dates.sort()
                        # Get the most recent date and then split it on the hyphens
                        self.last_active = self.active_dates[
                            len(self.active_dates) - 1
                        ].split("-")
                        # Set the last_active variable to the year only
                        self.last_active = self.last_active[0]
                        # Check to see if the last_active year is less than or equal to the desired year assigned to d,
                        # If so then append the full date to the temp_row list
                        if self.last_active != "" and int(self.last_active) <= d:
                            self.temp_row.append(
                                self.active_dates[len(self.active_dates) - 1]
                            )
                            # Append the temp_row to the lines list
                            self.lines.append(self.temp_row)
                    except:
                        sys.exit(f"Error getting needed fields for csv row")

        # If there is 1 or more lines then return the lines
        if len(self.lines) >= 1:
            return [self.lines, self.o_filename]
        else:
            sys.exit(f"Error: no data to stage!")


# Define the main function
def main():
    staged_csv = Stage_CSV().stage()
    csv_compose.Compose(staged_csv)


if __name__ == "__main__":
    main()
