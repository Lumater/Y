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
print("Checking files...")
if os.path.isfile(r'Y.py'):
    print("Well it looks like your all set!")
else:
    print("Oh no! It looks like your missing Y.py!")
    print("Please download the missing file at: https://github.com/Lumater/Y/blob/master/Y.py")
#--------------------------------------
#remove, this is only for testing purposes for now
input()
#--------------------------------------
