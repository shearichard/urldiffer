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

    do_composite_diff = parser.getboolean('processing', 'do_composite_diff')
    do_single_diff = parser.getboolean('processing', 'do_single_diff')

    baselineurl = parser.get('baseline', 'baseurl')

    return {'excluded_categories': lst_ex_cat, 
            'baselineurl': baselineurl, 
            'diccompurls': dicout,
            'do_composite_diff': do_composite_diff,
            'do_single_diff': do_single_diff
            }


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

    LINKTYPE|SETTINGS|USAGE|URL
    '''
    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
    lst = []
    with open('differ.csv', "rb") as csvfile:
        for row in csv.DictReader(csvfile, dialect='piper'):
            lst.append(row)

    return lst

def makeTempDir(label):
    dirprfx = "%s-%s-" % (getiso(), label)
    path2dir = tempfile.mkdtemp(prefix=dirprfx)
    return path2dir


def getTempPath(fName, dPath=None, label="UNKNOWN"):
    if dPath==None:
        path2dir = makeTempDir(label)
    else:
        path2dir = dPath
    fullpath = os.path.join(path2dir,fName)
    return fullpath


def getiso():
    d=datetime.now()
    return d.strftime('%Y%m%dT%H%M%S')


def dump_url(elem, f):
    f.write("1======================================\n")
    f.write("\n")
    f.write("\n")
    f.write(elem['USAGE'])
    f.write("\n")
    f.write(elem['LINKTYPE'])
    f.write("\n")
    f.write(elem['SETTINGS'])
    f.write("\n")
    f.write(elem['URL'])
    f.write("\n")
    f.write("\n")
    this_elem_dic = parse_query(elem['URL'])
    pprint.pprint(this_elem_dic, f)
    f.write("2======================================\n")


def output_urls_filtered(lst_dic_all_urls, 
                lst_inc_only_usage=None, 
                lst_inc_only_linktype=None, 
                lst_inc_only_settings=None):
    '''
    Outputs a report on those elements which 
    are common to all urls
    '''

    lst_non_common_argname = []
    lst_common_argname_different_values = []
    for elem in lst_dic_all_urls:
        if (((lst_inc_only_usage == None) or (elem['USAGE'] in lst_inc_only_usage))
            and ((lst_inc_only_linktype == None) or (elem['LINKTYPE'] in lst_inc_only_linktype))
            and ((lst_inc_only_settings == None) or (elem['SETTINGS'] in lst_inc_only_settings))):
            common_dic = parse_query(elem['URL'])
            common_values_dic = copy.deepcopy(common_dic)
            break
            
    output_path = getTempPath("differ.html")
    print(output_path)
    with open(output_path, 'wt') as f:
        for elem in lst_dic_all_urls:
            if (((lst_inc_only_usage == None) or (elem['USAGE'] in lst_inc_only_usage))
                and ((lst_inc_only_linktype == None) or (elem['LINKTYPE'] in lst_inc_only_linktype))
                and ((lst_inc_only_settings == None) or (elem['SETTINGS'] in lst_inc_only_settings))):
                dump_url(elem, f)
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

        f.write("3= lst_non_common_argname =====================================\n")
        pprint.pprint(lst_non_common_argname, f)
        f.write("4= lst_common_argname_different_values =====================================\n")
        pprint.pprint(lst_common_argname_different_values, f)
        f.write("5======================================\n")


    output_path = getTempPath("differ.txt", label="ARGUSAGE")
    print(output_path)
    lst_args = []
    dic_args = {}
    import pdb
    pdb.set_trace()
    with open(output_path, 'wt') as f:
        f.write("lst_inc_only_usage\n")
        pprint.pprint(lst_inc_only_usage, f)
        f.write("lst_inc_only_linktype\n")
        pprint.pprint(lst_inc_only_linktype, f)
        f.write("lst_inc_only_settings\n")
        pprint.pprint(lst_inc_only_settings, f)
        f.write("\n\n")
        for elem in lst_dic_all_urls:
            if (((lst_inc_only_usage == None) or (elem['USAGE'] in lst_inc_only_usage))
                and ((lst_inc_only_linktype == None) or (elem['LINKTYPE'] in lst_inc_only_linktype))
                and ((lst_inc_only_settings == None) or (elem['SETTINGS'] in lst_inc_only_settings))):
                this_elem_dic = parse_query(elem['URL'])
                for argname in this_elem_dic:
                    if argname not in lst_args:
                        lst_args.append(argname)
                    if argname in dic_args:
                        dic_args[argname]['count'] += 1
                        dic_args[argname]['where'].append(elem['SETTINGS'])
                        dic_args[argname]['values'].append(this_elem_dic[argname]) 
                    else:
                        dic_args[argname] = {'count':1, 'where': [elem['SETTINGS']], 'values': [this_elem_dic[argname]]} 

        f.write("\n\n")
        pprint.pprint(dic_args, f)
        f.write("\n\n")
        for k in dic_args:
            if dic_args[k]['count'] == 4:
                f.write("%s -> %s\n" % ( str(k) , dic_args[k]['count']))
                f.write("\n")
        f.write("\n\n\n\n")
        for k in dic_args:
            if dic_args[k]['count'] != 4:
                f.write("%s -> %s\n" % ( str(k) , dic_args[k]['count']))
                pprint.pprint(dic_args[k]['where'], f)
                f.write("\n")


def find_common(lst_dic_all_urls, 
                lst_inc_only_usage=None, 
                lst_inc_only_linktype=None, 
                lst_inc_only_settings=None):
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
        if (((lst_inc_only_usage == None) or (elem['USAGE'] in lst_inc_only_usage))
            and ((lst_inc_only_linktype == None) or (elem['LINKTYPE'] in lst_inc_only_linktype))
            and ((lst_inc_only_settings == None) or (elem['SETTINGS'] in lst_inc_only_settings))):
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
    output_urls_filtered(lst_dic_all_urls, ['FIN'], ['RED'], None)
    find_common(lst_dic_all_urls, ['FIN'], ['RED'], None)

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

def do_simple_diff():
    parser = ConfigParser.ConfigParser()
    parser.read("./differ.ini")

    url1 = parser.get('simplediff', 'u1')
    url1_desc = parser.get('simplediff', 'u1_desc')
    url2 = parser.get('simplediff', 'u2')
    url2_desc = parser.get('simplediff', 'u2_desc')
    dic_url1 = parse_query(url1)
    dic_url2 = parse_query(url2)

    import pdb
    pdb.set_trace()
    print("*" * 40)
    print("URL1: %s" % url1_desc)
    print(url1)
    print(" ")
    pprint.pprint(dic_url1)
    print("*" * 40)
    print("*" * 40)
    print("URL2: %s" % url2_desc)
    print(url2)
    print(" ")
    pprint.pprint(dic_url2)
    print("*" * 40)
    print(" ")
    print(" ")

    lstout = []
    lst_common_argname_different_values = []
    for argname, argval in dic_url1.iteritems():
        if argname in dic_url2:
            if (collections.Counter(dic_url1[argname]) == collections.Counter(dic_url1[argname])):
                pass
            else:
                #lstout.append(argname + " exists in both but values are different. Value in " + desc + " is " + str(dic_url_qry[argname]) + " . Value in baseline is " + str(baseline_urls_qry[argname]) + " .")
                lstout.append(argname + " exists in both but values are different.")
        else:
            lstout.append(argname + " exists in %s but not in %s" % (url1_desc, url2_desc))

    for argname, argval in dic_url2.iteritems():
        if argname in dic_url1:
            pass
        else:
            lstout.append(argname + " exists in %s but not in %s" % (url2_desc, url1_desc))

    for argname, argval in dic_url1.iteritems():
        if (argname in dic_url1) and (argname in dic_url2):
            if (collections.Counter(dic_url1[argname]) == collections.Counter(dic_url2[argname])):
                pass
            else:
                if argname not in lst_common_argname_different_values:
                    lst_common_argname_different_values.append(argname)
    for argname, argval in dic_url2.iteritems():
        if (argname in dic_url1) and (argname in dic_url2):
            if (collections.Counter(dic_url1[argname]) == collections.Counter(dic_url2[argname])):
                pass
            else:
                if argname not in lst_common_argname_different_values:
                    lst_common_argname_different_values.append(argname)

    lstout.sort()
    if lstout:
        for msg in lstout:
            print(msg)
    else:
        print("The two urls are identical")

    print("Common argnames with different values")
    if lst_common_argname_different_values:
        for a in lst_common_argname_different_values:
            print(a)


def main():

    dic_ini_data = get_ini_data()
    lst_dic = get_csv_data()

    if dic_ini_data['do_composite_diff']:
        find_query_diff(dic_ini_data['baselineurl'],
                        dic_ini_data['diccompurls'],
                        dic_ini_data['excluded_categories'], 
                        lst_dic)

    if dic_ini_data['do_single_diff']:
        do_simple_diff()

if __name__ == "__main__":
    main()
