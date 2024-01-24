import csv
from helper_tools import misc, device_data


# Define Stage_CSV Class for staging the data for writing a csv file
class Stage_CSV:
    def __init__(self):
        # Define a dictionary with the google defined headers
        self.g_headers = [
            "deviceId",
            "diskVolumeReports.0.volumeInfo.0.storageFree",
            "diskVolumeReports.0.volumeInfo.0.storageTotal",
            "orgUnitPath",
            "serialNumber",
        ]

        # Create empty dictionary
        self.header_to_num = {}
        # Create empty list
        self.lines = []
        # Define input file name
        self.i_filename = "full_list_devices.csv"
        # Define output file name
        self.o_filename = "disk_space_is_almost_full.csv"

    # Define the stage method
    def stage(self):
        # Open the input file to read the data from
        with open("needed_files/" + self.i_filename, mode="r") as self.csv_file_read:
            # Look for null bytes and remove them so the reader does not bail out
            self.csv_reader = csv.reader(
                (line.replace("\0", "") for line in self.csv_file_read),
                self.csv_file_read,
                delimiter=",",
            )
            # Read the number of columns in the csv
            self.n_col = len(next(self.csv_reader))
            # Rewind the reader to the beginning of the file
            self.csv_file_read.seek(0)
            self.line_count = 0

            # Read each row of the input csv file
            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        # Get the column header name and assign it to a variable
                        self.col_name = str(row[x])
                        # If the header name is in the google defined header dictionary add it to the header_to_num dictionary
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    self.line_count += 1
                else:
                    try:
                        # Write the desired data from the current row to a temporary list
                        self.temp_row = [
                            row[
                                self.header_to_num.get(
                                    "deviceId",
                                    "Error getting header number for deviceId",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "diskVolumeReports.0.volumeInfo.0.storageFree",
                                    "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageFree",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "diskVolumeReports.0.volumeInfo.0.storageTotal",
                                    "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageTotal",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "orgUnitPath",
                                    "Error geting header number for orgUnitPath",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "serialNumber", "Error getting header number"
                                )
                            ],
                        ]
                        # We do not want to wipe staff units so this logic keeps staff units from being added
                        if "Staff" in str(self.temp_row[3]):
                            continue
                        else:
                            # Some older units will not report their disk space properly due to the way the partitions were created, this logic keeps them from being added
                            if (str(self.temp_row[1]) or str(self.temp_row[2])) == "":
                                continue
                            # Create a percentage of disk space left and if it is less than or equal to 20 percent then add the device
                            elif (
                                int(self.temp_row[1]) / int(self.temp_row[2])
                            ) <= float(0.20):
                                self.temp_row.append(
                                    int(self.temp_row[1]) / int(self.temp_row[2])
                                )
                                self.lines.append(self.temp_row)
                            else:
                                continue
                    except:
                        print("Error getting needed fields for csv row")
                        misc.exit_message()
        # Check to see if there is any data to write
        if len(self.lines) > 2:
            return [self.lines, self.o_filename]
        else:
            print("\nError: no data to stage!\n")
            misc.exit_message()


def main():
    device_data.Full_Device_Data()
    stage_csv = Stage_CSV().stage()
    misc.Compose(stage_csv)
    print("The " + stage_csv[1] + " file has been created in the /needed_files directory.  Thank you!")


if __name__ == "__main__":
    main()
