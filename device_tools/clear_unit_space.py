import sys
import subprocess
import csv

#sys.path.append("/GAM_Tools")
from helper_tools import csv_compose, device_data


class Stage_CSV:
    def __init__(self):
        self.g_headers = [
            "deviceId",
            "diskVolumeReports.0.volumeInfo.0.storageFree",
            "diskVolumeReports.0.volumeInfo.0.storageTotal",
            "orgUnitPath",
            "serialNumber"
        ]

        self.header_to_num = {}
        self.lines = []
        self.i_filename = "full_devices.csv"
        self.o_filename = "disk_is_full.csv"

    def stage(self):
        with open("needed_files/" + self.i_filename, mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader((line.replace('\0','') for line in self.csv_file_read), self.csv_file_read, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            self.line_count = 0

            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0,self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    self.line_count += 1
                else:
                    try:
                        self.temp_row = [
                            row[
                                self.header_to_num.get("deviceId", "Error getting header number for deviceId")
                            ],
                            row[
                                self.header_to_num.get("diskVolumeReports.0.volumeInfo.0.storageFree", "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageFree")
                            ],
                            row[
                                self.header_to_num.get("diskVolumeReports.0.volumeInfo.0.storageTotal", "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageTotal")
                            ],
                            row[
                                self.header_to_num.get("orgUnitPath", "Error geting header number for orgUnitPath")
                            ],
                            row[
                                self.header_to_num.get("serialNumber", "Error getting header number")
                            ]
                        ]
                        if ("Staff" in str(self.temp_row[3])):
                            print("STAFF")
                            continue
                        else:
                            if (str(self.temp_row[1]) or str(self.temp_row[2])) == '':
                                continue
                            elif (int(self.temp_row[1]) / int(self.temp_row[2])) <= float(.20):
                                self.temp_row.append(int(self.temp_row[1]) / int(self.temp_row[2]))
                                self.lines.append(self.temp_row)
                                print(self.temp_row)
                                #return self.result
                            else:
                                continue
                    except:
                        sys.exit("Error getting needed fields for csv row")
        if len(self.lines) > 2:
            return [self.lines, self.o_filename]
        else:
            sys.exit("Error: no data to stage!")


def main():
    device_data.Full_Device_Data()
    stage_csv = Stage_CSV().stage()
    csv_compose.Compose(stage_csv)
    


if __name__ == "__main__":
    main()
