import sys
import subprocess
import re
from helper_tools import misc



class Wanted_Device_Info:
    def __init__(self,device_id,wanted_data):
       self.g_headers = {
        "1" : "serialNumber",
        "2" : "orgUnitPath",
        "3" : "osVersion",
        "4" : "macAddress",
        "5" : "autoUpdateExpiration",
        "6" : "email"
       }

       self.return_data_list(device_id,wanted_data)

    def return_data_list(self,device_id,wanted_data):
       self.device_id = device_id
       self.wanted_data = wanted_data

       return([self.device_id,self.wanted_data])

       
    @classmethod
    def get(cls):
        user_choice_dict = {
            "1" : "Serial Number",
            "2" : "Org Unit",
            "3" : "OS Version",
            "4" : "MAC Address",
            "5" : "Auto Update Expiration Date",
            "6" : "Recent Users",
            "7" : "ALL",
            "8" : "EXIT"
        }

        while True:
            device_id = input("Please enter the UUID (Directory API ID): ")
            if not re.search(r"^(?:\w{8})-(?:\w{4})-(?:\w{4})-(?:\w{4})-(?:\w{12})$", device_id):
                print("Not a valid Directory API ID!!")
            else:
                break
        
        misc.Dict_Print(user_choice_dict)

        while True:
            wanted_data_key = input("What information about the unit would you like? ")
            if str(wanted_data_key) not in user_choice_dict:
                print("Invalid entry, please try again! (Enter 1-" + str(len(user_choice_dict)) + ")")
            else:
                wanted_data = user_choice_dict.get(wanted_data_key)
                break
        return cls(device_id,wanted_data)

def show_data(data):
    device_id = data[0]
    device_data = data[1]
    print(device_id + device_data)

def main():
    data = Wanted_Device_Info.get()
    print(data)



if __name__ == "__main__":
    main()