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

    cat_items = parser.items("excludecategories")
    lst_ex_cat = []
    for key, value in cat_items:
        lst_ex_cat.append(value)

    path_items = parser.items("comparisons")
    dicout = {}
    for key, value in path_items:
        lst_val = value.split("|")
        if lst_val[0] not in dicout:
            dicout[lst_val[0]] = {}
        dicout[lst_val[0]][lst_val[1]] = lst_val[2]

    baselineurl = parser.get('baseline', 'baseurl')
    return {'excluded_categories': lst_ex_cat, 'baselineurl': baselineurl, 'diccompurls': dicout}


def parse_query(url):
    '''
    Take the query part of `url` and load the elements of it
    into a dictionary
    '''

    o_actual = urlparse(url)
    p_actual = parse_qs(o_actual.query)
    return p_actual


def find_query_diff(baselineurl,
                    dic_of_urls_to_compare,
                    lst_excluded_categories):
    '''
    For each url in `lst_of_urls_to_compare` find those parts
    of the query which do not exist in the `baselineurl` and
    report on it.
    '''
    dic_urls_qry = {}
    for settings, urldic in dic_of_urls_to_compare.iteritems():
        if settings not in dic_urls_qry:
            dic_urls_qry[settings] = {}

        for desc, url in urldic.iteritems():
            if desc not in lst_excluded_categories:
                if desc not in dic_urls_qry[settings]:
                    dic_urls_qry[settings][desc] = {}
                dic_urls_qry[settings][desc] = parse_query(url)

    baseline_urls_qry = parse_query(baselineurl)

    print("YYY")
    pprint.pprint(dic_urls_qry)
    pprint.pprint(baseline_urls_qry)

    print("XXX")
    import pdb
    pdb.set_trace()
    for settings, dicurl in dic_urls_qry.iteritems():
        print()
        print("- " + settings)
        for desc, dic_url_qry in dicurl.iteritems():
            print()
            print("-- " + desc)
            lstout = []
            for argname, argval in dic_url_qry.iteritems():
                if argname in baseline_urls_qry:
                    if (collections.Counter(dic_url_qry[argname]) == collections.Counter(baseline_urls_qry[argname])):
                        pass
                    else:
                        lstout.append(argname + " exists in both " + desc + " and baseline but values are different. Value in " + desc + " is " + str(dic_url_qry[argname]) + " . Value in baseline is " + str(baseline_urls_qry[argname]) + " .")
                else:
                    lstout.append(argname + " exists in " + desc + " but not in baseline")

            for argname, argval in baseline_urls_qry.iteritems():
                if argname in dic_url_qry:
                    pass
                else:
                    lstout.append(argname + " exists in baseline but not in " + desc)

            lstout.sort()
            for msg in lstout:
                print(msg)


def main():
    dic_ini_data = get_ini_data()
    find_query_diff(dic_ini_data['baselineurl'],
                    dic_ini_data['diccompurls'],
                    dic_ini_data['excluded_categories'])

if __name__ == "__main__":
    main()
