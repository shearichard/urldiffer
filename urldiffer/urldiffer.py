from __future__ import print_function
import pprint
from urlparse import urlparse, parse_qs
import ConfigParser
import collections

def config_diag(parser):
    print()
    print("START DIAG")
    for section_name in parser.sections():
        print('Section:', section_name)
        print('  Options:', parser.options(section_name))
        for name, value in parser.items(section_name):
            print('  %s = %s' % (name, value))
        print()
    print("END DIAG")
    print()


def get_ini_data():
    '''
    Extract initailzation data from the .INI file
    '''
    parser = ConfigParser.ConfigParser()
    parser.read("./differ.ini")
    if False:
        config_diag(parser)
      
    path_items = parser.items( "comparisons" )
    dicout = {}
    for key, value in path_items:
        lst_val = value.split("|")
        dicout[lst_val[0]] = lst_val[1]
    baselineurl = parser.get('baseline', 'baseurl') 
    return {'baselineurl': baselineurl, 'diccompurls': dicout}

def parse_query(url):
    '''
    Take the query part of `url` and load the elements of it
    into a dictionary
    '''

    o_actual = urlparse(url)
    p_actual = parse_qs(o_actual.query)
    return p_actual

def find_query_diff(baselineurl, dic_of_urls_to_compare):
    '''
    For each url in `lst_of_urls_to_compare` find those parts
    of the query which do not exist in the `baselineurl` and 
    report on it.
    '''
    dic_urls_qry = {}
    for desc, url in dic_of_urls_to_compare.iteritems():
        dic_urls_qry[desc] = parse_query(url)

    baseline_urls_qry = parse_query(baselineurl)

    print("YYY")
    pprint.pprint(dic_urls_qry)
    pprint.pprint(baseline_urls_qry)

    print("XXX")
    for desc, dic_url_qry in dic_urls_qry.iteritems():
        print()
        for argname, argval in dic_url_qry.iteritems():
            if argname in baseline_urls_qry:
                if (collections.Counter(dic_url_qry[argname]) == collections.Counter(baseline_urls_qry[argname])):
                    pass
                else:
                    print(argname + " exists in both " + desc + " and baseline but values are different. Value in " + desc + " is " + str(dic_url_qry[argname]) + " . Value in baseline is " + str(baseline_urls_qry[argname]) + " .")
            else:
                print(argname + " exists in " + desc + " but not in baseline")

def main():
    dic_ini_data = get_ini_data()
    find_query_diff(dic_ini_data['baselineurl'],
                    dic_ini_data['diccompurls'])

if __name__ == "__main__":
    main()
