__author__ = 'g'
import os
import urllib

def read_text():
    path = os.getcwd
    quotes = open(path+"movie_quotes")
    print path
    contents_of_file = quotes.read()
    print (contents_of_file)
    quotes.close()