import subprocess
import csv
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
        #print(self.ou)
        self.i_filename = "needed_files/full_list_devices.csv"
        self.o_filename = "cart_device_data/" + str(self.ou)
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
        self.notes = "Initial Import"
        self.category = "Chromebook"

    def stage(self):
        with open(self.i_filename,mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader((line.replace("\0","") for line in self.csv_file_read),self.csv_file_read, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            self.line_count = 0

            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0,self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_number.update({self.col_name: x})
                    self.header_row = ['deviceId','autoUpdateExpiration','Serial Number','macAddress','Model Name','notes','Location','Manufacturer','Category','Asset Tag']
                    self.lines.append(self.header_row)
                    self.line_count += 1
                else:
                    try:
                        if len(self.header_to_number.get('serialNumber')) > 14:
                            temp_asset_tag = list(self.header_to_number.get('serialNumber'))
                            while len(temp_asset_tag) > 14:
                                temp_asset_tag.remove(temp_asset_tag[0])
                            self.asset_tag = ''.join(temp_asset_tag)
                        self.temp_row = [
                            row[
                                self.header_to_number.get("deviceId","Error getting header number for deviceId")
                            ],
                            row[
                                self.header_to_number.get("autoUpdateExpiration","Error getting header number for autoUpdateExpiration")
                            ],
                            row[
                                self.header_to_number.get("serialNumber","Error getting header number for serialNumber")
                            ],
                            row[
                                self.header_to_number.get("macAddress","Error getting header number for macAddress")
                            ],
                            row[
                                self.header_to_number.get("model","Error getting header number for model")
                            ],
                            self.notes,
                            row[
                                self.header_to_number.get("orgUnitPath","Error getting header number for orgUnitPath")
                            ],
                            row[
                                self.header_to_number.get("model","Error getting header number for model")
                            ],
                            self.category,
                            self.asset_tag
                        ]
                        self.lines.append(self.temp_row)
                        self.line_count += 1
                    except:
                        print("Error getting needed fields for csv row")
                        misc.exit_message()
            if len(self.lines) > 2:
                return [self.lines, self.o_filename]
            else:
                print("\nError: No data to stage!!")
                misc.exit_message()


def main():
    device_OUs = misc.Campus_OUs().ou_dict(account_type)
    misc.Dict_Print(device_OUs)
    choosen_ou = Choosen_OU(None).get(device_OUs)
    #print("Choosen" + str(choosen_ou))
    stage_csv = Stage_CSV(str(choosen_ou)).stage()
    misc.Compose(stage_csv)



if __name__ == "__main__":
    main()