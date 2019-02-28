#--------------------------------------
#File Integrety Checker (FIC)

#TO DO!
# 1). Create a basic GUI
# 2). Have the computer download the missing files if needed
#--------------------------------------
import os
import getpass
#--------------------------------------
computeruser = getpass.getuser()
#--------------------------------------
if os.path.isfile(r'Y.py'):
    print("your all set!")
else:
    print("An Error Occured!")
    #make the computer download the missing files
#--------------------------------------
