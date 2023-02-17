import subprocess
from user_account_tools import create_account, move_user, escalate_grade_to_new_building
from helper_tools import misc, user_data
from device_tools import (
    find_units_low_on_space,
    inactive_units,
    find_device_info_by_uuid,
    find_device_data_by_org_unit,
)


# Create Tool class
class Tool:
    def __init__(self, tool):
        self.tool = tool

    def __str__(self):
        return self.tool

    @classmethod
    def get(cls, tool_dict):
        # Get user input on what tool they want to use
        dict_num = input("\nWhat tool would you like to utilize?\n")
        tool = tool_dict.get(dict_num)
        return cls(tool)


def main():
    # Define tool dictionary
    tool_dict = {
        "1": "create_account",
        "2": "find_device_info_by_uuid",
        "3": "find_units_low_on_space",
        "4": "find_inactive_units",
        "5": "find_device_data_by_org_unit",
        "6": "move_a_single_user_to_a_new_Org_Unit",
        "7": "get_user_data_from_an_Org_Unit",
        "8": "escalate_grade_to_new_building",
        "9": "Exit",
    }

    # Clear the terminal
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("\nWelcome to the MG GAM tools\n")
    misc.Setup()
    misc.Dict_Print(tool_dict)
    tool = Tool.get(tool_dict)
    # Change to case in the future since case switch exists Python >= 3.10
    if str(tool) == "create_account":
        create_account.main()
    elif str(tool) == "find_device_info_by_uuid":
        find_device_info_by_uuid.main()
    elif str(tool) == "find_units_low_on_space":
        find_units_low_on_space.main()
    elif str(tool) == "find_inactive_units":
        inactive_units.main()
    elif str(tool) == "find_device_data_by_org_unit":
        find_device_data_by_org_unit.main()
    elif str(tool) == "move_a_single_user_to_a_new_Org_Unit":
        move_user.main()
    elif str(tool) == "get_user_data_from_an_Org_Unit":
        user_data.main()
    elif str(tool) == "escalate_grade_to_new_building":
        escalate_grade_to_new_building.main()
    elif str(tool) == "Exit":
        misc.exit_message()


if __name__ == "__main__":
    main()
