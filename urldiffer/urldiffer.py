from __future__ import print_function
import pprint
from urlparse import urlparse, parse_qs
import ConfigParser
import collections
import csv
import tempfile
import os
from datetime import datetime
import copy


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


def get_csv_data():
    '''
    Read URL's from CSV. Returns a list of dictionaries

    The expected headings are : 

    SETTINGS|USAGE|URL
    '''
    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
    lst = []
    with open('differ.csv', "rb") as csvfile:
        for row in csv.DictReader(csvfile, dialect='piper'):
            print(row)
            lst.append(row)

    return lst

def makeTempDir():
    path2dir = tempfile.mkdtemp()
    return path2dir


def getTempPath(fName, dPath=None):
    if dPath==None:
        path2dir = makeTempDir()
    else:
        path2dir = dPath
    fullpath = os.path.join(path2dir,fName)
    return fullpath


def getiso():
    d=datetime.now()
    return d.strftime('%Y%m%dT%H%M%S')


def find_common(lst_dic_all_urls):
    '''
    Outputs a report on those elements which 
    are common to all urls
    '''
    #Load up the first one
    common_dic = parse_query(lst_dic_all_urls[0]['URL'])
    common_values_dic = copy.deepcopy(common_dic)

    lst_non_common_argname = []
    lst_common_argname_different_values = []
    #Iterate over each of our urls of interest
    for elem in lst_dic_all_urls:
        print("=======================================")
        this_elem_dic = parse_query(elem['URL'])
        #Iterate over each of the keys in the baseline dic
        for argname in common_dic:
            #If there's a baseline dic key not in the current
            #url then mark it for removal from the baseline dic
            print(argname)
            if argname not in elem['URL'] and argname not in lst_non_common_argname:
                lst_non_common_argname.append(argname)

            if (argname in common_values_dic) and (argname in this_elem_dic):
                if (collections.Counter(common_values_dic[argname]) == collections.Counter(this_elem_dic[argname])):
                    pass
                else:
                    if argname not in lst_common_argname_different_values:
                        lst_common_argname_different_values.append(argname)
            else:
                if (argname in this_elem_dic):
                    common_values_dic[argname] = this_elem_dic[argname]



    import pdb
    pdb.set_trace()
    for arg in lst_non_common_argname:
        del common_dic[arg]

    print(common_dic)

    output_path = getTempPath("differ.html")
    print(output_path)
    with open(output_path, 'wt') as f:
        f.write('contents go here')


def find_query_diff(baselineurl,
                    dic_of_urls_to_compare,
                    lst_excluded_categories,
                    lst_dic_all_urls):
    '''
    For each url in `lst_of_urls_to_compare` find those parts
    of the query which do not exist in the `baselineurl` and
    report on it.
    '''

    find_common(lst_dic_all_urls)

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
    lst_dic = get_csv_data()
    find_query_diff(dic_ini_data['baselineurl'],
                    dic_ini_data['diccompurls'],
                    dic_ini_data['excluded_categories'], 
                    lst_dic)

if __name__ == "__main__":
    main()
