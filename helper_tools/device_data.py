import subprocess

# Define Full_Device_Data Class
class Full_Device_Data:
    def __init__(self):
        # Set the needed path and file
        self.filename = "needed_files/full_list_devices.csv"
        # Create the file
        subprocess.Popen(["touch", self.filename], stdout=subprocess.PIPE)

        self.write_data(self.filename)

    def write_data(self, filename):
        print("Now going to collect all device data from GAM")
        self.filename = filename
        # Open the file for writing
        with open(self.filename, mode="w") as self.o_file:
            # Write all device info into open file
            self.write_out = subprocess.Popen(
                ["gam", "print", "cros", "full", "query", "status:provisioned"],
                stdout=self.o_file,
            )
            self.write_out.wait()


def main():
    Full_Device_Data()


if __name__ == "__main__":
    main()
