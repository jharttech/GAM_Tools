import subprocess
import re
from helper_tools import misc, user_data
        

class Escalate_OU:
    def __init__(self,old_ou,new_ou):
        self.old_ou = str(old_ou)
        self.new_ou = str(new_ou)

        self.escalation(self.old_ou,self.new_ou)

    def escalation(self,old_ou,new_ou):
        old_ou = str("'" + str(old_ou) + "'")
        escalate = subprocess.Popen(["gam","update","org",old_ou,"parent","/Students/" + new_ou,"inherit"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        escalate.communicate()
        escalate.wait()


def main():
    account_type = "student"
    org_units = misc.Campus_OUs().ou_dict(account_type)
    misc.Dict_Print(org_units)
    old_ou = misc.Assign_OU(None).get(org_units)
    print("\nNow going to ask you to select the new Parent Org Unit")
    parent_OUs = {
        "1":"MGHS",
        "2":"MGMS"
        }
    misc.Dict_Print(parent_OUs)
    new_ou = misc.Assign_OU(None).get(parent_OUs)
    Escalate_OU(old_ou,new_ou)
    misc.exit_message()

    
    





if __name__ == "__main__":
    main()