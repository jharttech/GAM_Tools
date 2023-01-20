import sys
import subprocess
import re
from helper_tools import misc


# Create Wanted Device Class
class Wanted_Device_Info:
    def __init__(self, device_id, wanted_data):
        # Define google specific headers dictionary
        self.g_headers = {
            "Serial Number": "serialNumber",
            "Org Unit": "orgUnitPath",
            "OS Version": "osVersion",
            "MAC Address": "macAddress",
            "Auto Update Expiration Date": "autoUpdateExpiration",
            "Recent Users": "email",
        }
        self.device_id = device_id
        self.wanted_data = wanted_data

        # Call get_device_data method with desired parameters
        self.get_device_data(self.device_id, self.wanted_data, self.g_headers)

    # Define the get_device_data method
    def get_device_data(self, device_id, wanted_data, g_headers):
        # Gather device data from GAM
        gather = subprocess.Popen(
            ["gam", "info", "cros", device_id], stdout=subprocess.PIPE
        )
        # Wait until the subprocess is complete before proceeding
        gather.wait()

        if str(wanted_data) != "ALL":
            # Grep out desired data from the GAM data gathered above
            data = subprocess.Popen(
                ["grep", g_headers.get(wanted_data)],
                stdin=gather.stdout,
                stdout=subprocess.PIPE,
            )
            # Read the result of the grep subprocess above
            self.result = str(data.stdout.read().decode().strip())
        elif str(wanted_data) == "ALL":
            self.result = str(gather.stdout.read().decode().strip())

        print(self.result)

    @classmethod
    def get(cls):
        # Define the possible data the user wants in a dictionary
        user_choice_dict = {
            "1": "Serial Number",
            "2": "Org Unit",
            "3": "OS Version",
            "4": "MAC Address",
            "5": "Auto Update Expiration Date",
            "6": "Recent Users",
            "7": "ALL",
            "8": "EXIT",
        }

        while True:
            # Ask user for the UUID of the device they want to gather data from
            device_id = input("Please enter the UUID (Directory API ID): ")
            # Use regex to validate the user input, if not valid then ask the question again
            if not re.search(
                r"^(?:\w{8})-(?:\w{4})-(?:\w{4})-(?:\w{4})-(?:\w{12})$", device_id
            ):
                print("Not a valid Directory API ID!!")
            else:
                break
        
        # Print the user_choice_dict dictionary to screen
        misc.Dict_Print(user_choice_dict)

        while True:
            # Ask the user what information they want about the desired device
            wanted_data_key = input("What information about the unit would you like? ")
            # Validate the user input is an option in the dictionary, if not ask again.
            if str(wanted_data_key) not in user_choice_dict:
                print(
                    "Invalid entry, please try again! (Enter 1-"
                    + str(len(user_choice_dict))
                    + ")"
                )
            elif str(wanted_data_key) == "8":
                # Call the exit message
                misc.exit_message()
            else:
                wanted_data = user_choice_dict.get(wanted_data_key)
                break
        return cls(device_id, wanted_data)


def main():
    Wanted_Device_Info.get()


if __name__ == "__main__":
    main()
