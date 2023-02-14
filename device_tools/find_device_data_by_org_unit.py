import subprocess
from helper_tools import (device_data, misc)

account_type = "Chromebooks"

class Choosen_OU:
    def __init__(self,ou):
        self.ou = ou
    
    def __str__(self):
        return self.ou

    @classmethod
    def get(cls, ou_dict):
        while True:
            choice = input("\nPlease select the desired Org Unit: ")
            if str(choice) not in ou_dict:
                print("Invalid entry, please try again! (Enter 1-" + str(len(ou_dict)) + ")")
            else:
                ou = ou_dict.get(choice)
                return cls(ou)


class Stage_CSV:
    def __init__(self,device_org_unit):
        self.ou = device_org_unit.split("/")
        self.ou = self.ou[len(self.ou)-1]
        print(self.ou)
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
    misc.Dict_Print(device_OUs)
    choosen_ou = Choosen_OU(None).get(device_OUs)
    print(choosen_ou)
    Stage_CSV(choosen_ou)



if __name__ == "__main__":
    main()