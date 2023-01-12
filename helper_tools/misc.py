import csv

# The Compose class simply composes a file that can then be moved or reused for further
# Data manipulation
class Compose:
    def __init__(self, staged_data):
        self.o_filename = staged_data[1]
        self.lines = staged_data[0]
        with open(f"needed_files/{self.o_filename}", mode="w") as self.csv_file:
            for i in range(0, len(self.lines)):
                self.full = csv.writer(self.csv_file, delimiter=",")
                self.full.writerow(self.lines[i])


class Dict_Print:
    def __init__(self,data):
        self.data = data
        self.data_list = list(map(int,self.data))
        self.data_list = sorted(self.data_list)
        print("\n")
        for i in range(0,len(self.data)):
            print(str(self.data_list[i]) +  " : " + self.data.get(str(self.data_list[i])))


def exit_message():
    print("Terminating Program at this time.  Thank you! --JHart")