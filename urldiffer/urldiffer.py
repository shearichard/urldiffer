from __future__ import print_function
import pprint
from urlparse import urlparse, parse_qs
import ConfigParser



def config_diag(parser):
    print("START DIAG")
    for section_name in parser.sections():
        print('Section:', section_name)
        print('  Options:', parser.options(section_name))
        for name, value in parser.items(section_name):
            print('  %s = %s' % (name, value))
        print()
    print("END DIAG")

def get_ini_data():
    parser = ConfigParser.ConfigParser()
    parser.read("./differ.ini")
    config_diag(parser)
      
    path_items = parser.items( "comparisons" )
    lstout = []
    for key, path in path_items:
        lstout.append(path)
    baselineurl = parser.get('baseline', 'baseurl') 
    return {'baselineurl': baselineurl, 'lstcompurls': lstout}

    
def main():
    get_ini_data()

if __name__ == "__main__":
    main()
