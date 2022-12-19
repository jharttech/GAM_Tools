import csv
import subprocess
import datetime


class Full_Device_Data:
    def __init__(self):
        self.filename = "needed_files/full_devices.csv"
        subprocess.Popen(["touch",self.filename], stdout=subprocess.PIPE)

        self.write_data(self.filename)

    def write_data(self,filename):
        print("Now going to collect all device data from GAM")
        self.filename = filename
        with open(self.filename, mode='w') as self.o_file:
            self.write_out = subprocess.Popen(["gam","print","cros","full","query","status:provisioned"], stdout=self.o_file)
            self.write_out.wait()

class Wanted_Devices_Data:
    def __init__(self):
        self.header_list = [
            'deviceId',
            'autoUpdateExpiration',
            'serialNumber',
            'macAddress',
            'model',
            'orgUnitPath',
            #REMAINING SPACE ON DEVICE
        ]
        self.header_to_num = {}
        self.lines = []
        self.temp_row = []
        self.num = None
                

def main():
    Full_Device_Data()


if __name__ == "__main__":
    main()
