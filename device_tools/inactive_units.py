import sys
import subprocess
import csv
from datetime import date
from helper_tools import csv_compose


d = date.isoformat(date.today()).split("-")
d = (int(d[0]) - 2)


class Stage_CSV:
    def __init__(self):
        self.x = 0
        self.g_headers = [
            "deviceId",
            "orgUnitPath",
            "serialNumber"
        ]

        self.header_to_num = {}
        self.lines = []
        self.i_filename = "full_devices.csv"
        self.o_filename = "non_active_units.csv"
        self.temp_row =[]

    def stage(self):
        with open(f"../needed_files/{self.i_filename}", mode = "r") as self.csv_file_read:
            self.csv_reader = csv.reader((line.replace('\0','') for line in self.csv_file_read), self.csv_file_read, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            self.line_count = 0
            self.date_count = 0

            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0,self.n_col):
                        self.col_name = str(row[x])
                        if (self.col_name in self.g_headers) or ((str(self.col_name).__contains__("activeTimeRanges")) and (str(self.col_name).__contains__("date"))):
                            if (str(self.col_name).__contains__("activeTimeRanges")) and (str(self.col_name).__contains__("date")):
                                self.g_headers.append(self.col_name)
                            self.header_to_num.update({self.col_name: x})
                    self.line_count += 1
                else:
                    try:
                        #self.active_dates.sort()
                        self.active_dates = []
                        self.temp_row = []
                        for i in self.g_headers:
                            if i.__contains__("activeTimeRanges"):
                                self.active_dates.append(
                                    row[
                                        self.header_to_num.get(i, f"Error getting header number for {i}")
                                    ]
                                )
                            else:
                                self.temp_row.append(
                                    row[
                                        self.header_to_num.get(i, f"Error getting header number for {i}")
                                    ]
                                )
                        self.active_dates.sort()
                        self.last_active = self.active_dates[len(self.active_dates) - 1].split("-")
                        self.last_active = self.last_active[0]
                        if self.last_active != "" and int(self.last_active) <= d:
                            self.temp_row.append(self.active_dates[len(self.active_dates)-1])
                            self.lines.append(self.temp_row)
                        elif self.last_active == "":
                            #WRITE TO LOG
                            ...
                    except:
                        sys.exit(f"Error getting needed fields for csv row")

            #print(self.lines)
        if len(self.lines) >= 1:
            return [self.lines, self.o_filename]
        else:
            sys.exit(f"Error: no data to stage!")
                        


def main():
    print("start")
    staged_csv = Stage_CSV().stage()
    csv_compose.Compose(staged_csv)


if __name__ == "__main__":
    main()