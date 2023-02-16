import subprocess
from helper_tools import (misc, user_data)


#class Gather_All_User_Data:
    #def __init__(self):



def main():
    account_type = user_data.Account_type.get()
    campus_OUs = misc.Campus_OUs().ou_dict(account_type)
    misc.Dict_Print(campus_OUs)
    OU = misc.Assign_OU(None).get(campus_OUs)
    print(str(OU))


if __name__ == "_main__":
    main()