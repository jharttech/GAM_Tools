import subprocess
from scripts import create_account


class Tool:
    def __init__(self, tool):
        self.tool = tool
        
    def __str__(self):
        return f"{self.tool}"
        
    @classmethod
    def get(cls, tool_dict):
        dict_num = input("\nWhat tool would you like to utilize?\n")
        tool = tool_dict.get(dict_num)
        return cls(tool)


def main():
    tool_dict = {
        "1":"create_account",
        "2":"find_device_by_uuid",
        "2":"Exit"
    }
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    create_account.dict_print(tool_dict)
    tool = Tool.get(tool_dict)
    # Change to case in the future since case switch exists Python >= 3.10
    if str(tool) == "create_account":
        create_account.main()
    elif str(tool) == "find_device_by_uuid":
        #PICK UP HERE
        ...


if __name__ == "__main__":
    main()