import subprocess
from user_account_tools import create_account
from device_tools import find_units_low_on_space, inactive_units


class Tool:
    def __init__(self, tool):
        self.tool = tool
        
    def __str__(self):
        return self.tool
        
    @classmethod
    def get(cls, tool_dict):
        dict_num = input("\nWhat tool would you like to utilize?\n")
        tool = tool_dict.get(dict_num)
        return cls(tool)


def main():
    tool_dict = {
        "1":"create_account",
        "2":"find_device_info_by_uuid",
        "3":"find_units_low_on_space",
        "4":"find_inactive_units",
        "5":"Exit"
    }
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    create_account.dict_print(tool_dict)
    tool = Tool.get(tool_dict)
    # Change to case in the future since case switch exists Python >= 3.10
    if str(tool) == "create_account":
        create_account.main()
    elif str(tool) == "find_device_info_by_uuid":
        #FIXME
        ...
    elif str(tool) == "find_units_low_on_space":
        find_units_low_on_space.main()
    elif str(tool) == "find_inactive_units":
        inactive_units.main()
        


if __name__ == "__main__":
    main()
