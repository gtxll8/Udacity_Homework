__author__ = 'gcalinescu'
import os
def rename_files():

    #(1) get teh file names from a folder
    target_path = os.getcwd()
    file_list = os.listdir(target_path + "\prank")
    #print=(file_list)
    print("Current working directory is: "+target_path)
    os.chdir(target_path+"\prank")
    #(2) for each file rename filename
    for file_name in file_list:
        print("Old name - "+file_name)
        print("New Name - "+file_name.translate(None, "0123456789"))
        os.rename(file_name, file_name.translate(None, "0123456789"))
    os.chdir(target_path)



def create_message():

    #(1) define the secret message
    secret_message = "HELLO THERE"

    #(2) clear directory prank of any old files
    target_path = os.getcwd()
    os.chdir(target_path+"\prank")
    for files_to_remove in os.listdir(target_path + "\prank"):
        print(files_to_remove)
        os.remove(files_to_remove)


create_message()

#rename_files()