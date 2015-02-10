__author__ = 'gcalinescu'
import os
import time
import shutil
from random import randint

def unscramble_message():
    #(1) get teh file names from a folder
    target_path = os.getcwd()
    #(!) For windows use backslash like 'this '\prank'
    file_list = os.listdir(target_path + "/prank")
    #print=(file_list)
    print("Current working directory is: "+target_path)
    os.chdir(target_path+'/prank')
    #(2) for each file rename filename
    for file_name in file_list:
        print("Old name - "+file_name)
        print("New Name - "+file_name.translate(None, "0123456789"))
        os.rename(file_name, file_name.translate(None, "0123456789"))
    os.chdir(target_path)

def create_message():
    #(1) define the secret message
    secret_message = "HELLO THERE TO EVERYONE AT UDACITY"
    #(2) clear directory prank of any old files
    target_path = os.getcwd()
    os.chdir(target_path+"/prank")
    for files_to_remove in os.listdir(target_path + "/prank"):
        print(files_to_remove)
        os.remove(files_to_remove)
    #(3) get the list of files from alphabet directory + sort
    alphabet_files = os.listdir(target_path+"/alphabet")
    alphabet_files.sort()
    file_name_letter = alphabet_files[1]
    print(file_name_letter)
    #(4) translate secret message to numbers, using 'ord()'
    # exception is 'space' trap the '-64' and replace it with 'madrid.jpg'
    # also create an index so you can add an extra letter to the file name
    # so it orders alphabetically. LastLY add a random number in front oF the
    # file name
    alphabet_folder = target_path+"/alphabet/"
    prank_folder = target_path+"/prank/"
    index_counter = 1
    for letter in secret_message:
        # rnd number + increment alpha to scramble the files order, for
        # messages only up to 48 characters
        if index_counter <= 24:
            prefix_addition = str(randint(10,  39)) + (chr(96 + index_counter))
        else:
            prefix_addition = str(randint(10,  39)) + (chr(121)) + (chr(96 + (index_counter - 24)))

        #get the letter number
        letter_number = ord(letter.lower()) - 96
        if letter_number == -64:
            letter_file_name = 'madrid.jpg'
            shutil.copyfile(alphabet_folder+letter_file_name, prank_folder+prefix_addition+letter_file_name)
        else:
            letter_file_name = alphabet_files[letter_number - 1]
            shutil.copyfile(alphabet_folder+letter_file_name, prank_folder+prefix_addition+letter_file_name)
        index_counter += 1
    os.chdir(target_path)
    print(index_counter)

create_message()

time.sleep(10)

unscramble_message()