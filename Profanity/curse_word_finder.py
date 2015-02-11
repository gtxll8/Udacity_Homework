__author__ = 'g'
import os
import urllib

def read_text():
    path = os.getcwd()
    quotes = open(path+"/movie_quotes")
    contents_of_file = quotes.read()
    print (contents_of_file)
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(text_to_check):
    connection = urllib.urlopen("http://www.wdyl.com/profanity?q="+text_to_check)
    output = connection.read()
    connection.close()
    if "true" in output:
        print("Profanity Alert !")
    elif "false" in output:
        print("No profanities !")
    else:
        print("Could not connect !")



read_text()