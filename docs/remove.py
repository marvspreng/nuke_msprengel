import os
import sys
import nuke




#set works path
path = "Z:\com\Mengxb\logo"









def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.startswith("."):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))

if __name__ == "__main__":

    del_files(path)