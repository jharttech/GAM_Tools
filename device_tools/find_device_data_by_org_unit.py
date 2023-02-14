import subprocess
from helper_tools import (device_data, misc)

account_type = "Chromebooks"

class Stage_CSV:
    def __init__(self,device_org_unit):
        self.i_filename = "needed_files/full_list_devices.csv"
        self.o_filename = "cart_device_data/" + device_org_unit
        self.g_headers = [
            "deviceId",
            "autoUpdateExpiration",
            "serialNumber",
            "macAddress",
            "model",
            "orgUnitPath"
            ]
        self.header_to_number = {}
        self.lines = []
        self.temp_row = []
        self.num = None

        self.write_data(self.i_filename)

    def stage(self,i_filename):
        ...


def main():
    device_OUs = misc.Campus_OUs().ou_dict(account_type)
    misc.Dict_print(device_OUs)



if __name__ == "__main__":
    main()