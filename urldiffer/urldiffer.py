from __future__ import print_function
import pprint
from urlparse import urlparse, parse_qs
import ConfigParser


def get_ini_data():
    Config = ConfigParser.ConfigParser()
    Config.read("./differ.ini")
    path_items = Config.items( "comparisons" )
    for key, path in path_items:
        print(path)
    
def main():
    get_ini_data()

if __name__ == "__main__":
    main()
