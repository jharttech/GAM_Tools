import subprocess
import re
from helper_tools import misc, user_data


class Grade_To_Escalate():
    def __init__(self,building,grad_year):
        self.building = building
        self.grad_year = grad_year

    def get_building(self):
        return self.building
    
    def get_grad_year(self):
        return self.grad_year

    @classmethod
    def get(cls):
        options = {
            "1":"MS to HS",
            "2":"ES to MS"
        }
        misc.Dict_Print(options)
        while True:
            building = input("\nWhich building would you like to escalate? ")
            if building not in options:
                print("\nInvalid option, please select again!")
            else:
                building = options.get(building)
                break
        
        while True:
            grad_year = input("\nPlease enter the graduation year desired to escalate: ")
            if not re.search(r"^[1-9]{2}$", grad_year):
                print("\nInvalid year, please use the 'YY' format.")
            else:
                break

        grad_year = ("^"+grad_year)
        
        return cls(building,grad_year)


class Escalate:
    def __init__(self,building, grad_year):
        self.awk_command = '{print $1}'
        self.building = str(building).split(" ")
        self.old_building = self.building[0]
        self.new_building = self.building[2]
        print("Old: " + self.old_building)
        print("New: " + self.new_building)

        
    
        


def main():
    account_type = user_data.Account_type.get()
    info = Grade_To_Escalate(None,None).get()
    building = info.get_building()
    grad_year = info.get_grad_year()
    Escalate(building,grad_year)



if __name__ == "__main__":
    main()