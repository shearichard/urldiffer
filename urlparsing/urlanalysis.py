from __future__ import print_function
import pprint
from urlparse import urlparse, parse_qs
import collections

ACTUALDESC = "NF TRUE/FALSE/TRUE AS CURRENTLY GENERATED"
ACTUAL = "/query/?0_description=~&0_owner=137&0_closed=0&0_performance_colour=red&order=id&as_of=as_of&1_closed=0&1_data_entry_user=137&1_performance_colour=red&col=id&col=description&col=owner&col=data_entry_user&col=performance_colour&col=value&col=performance_explanation&1_future_colour=red&col=future_colour&col=future_recommendation"

'''
DESIREDDESC = "NF TRUE/FALSE/TRUE"
DESIRED = "/query/?0_description=~&0_closed=0&0_owner=137&0_future_colour=red&0_has_performance=1&1_closed=0&1_data_entry_user=137&1_future_colour=red&1_has_performance=1&order=id&col=id&col=description&col=owner&col=data_entry_user&col=performance_colour&col=value&col=performance_explanation&col=future_colour&col=future_recommendation&as_of=as_of"
'''
DESIREDDESC = "NF TRUE/FALSE/TRUE AS PER SPEC"
DESIRED = "/query/?0_description=~&0_closed=0&0_owner=137&0_future_colour=red&0_has_performance=1&1_closed=0&1_data_entry_user=137&1_future_colour=red&1_has_performance=1&order=id&col=id&col=description&col=owner&col=data_entry_user&col=performance_colour&col=value&col=performance_explanation&col=future_colour&col=future_recommendation&as_of=as_of"

def find_diff(p_actual, p_desired):
    for k, v in p_actual.iteritems():
        if k in p_desired:
            if (collections.Counter(p_actual[k]) == collections.Counter(p_desired[k])):
                pass
            else:
                print(k + " exists in both but values are different")
        else:
            print(k + " exists in p_actual but not in p_desired")

    for k, v in p_desired.iteritems():
        if k in p_actual:
            if (collections.Counter(p_actual[k]) == collections.Counter(p_desired[k])):
                pass
            else:
                print(k + " exists in both but values are different")
        else:
            print(k + " exists in p_desired but not in p_actual")

def main():
    print("ACTUAL ============================" + ACTUALDESC) 
    o_actual = urlparse(ACTUAL)
    p_actual = parse_qs(o_actual.query)
    pprint.pprint(p_actual)
    print("===================================")
    print("DESIRED ===========================" + DESIREDDESC)
    o_desired = urlparse(DESIRED)
    p_desired = parse_qs(o_desired.query)
    pprint.pprint(p_desired)
    print("===================================")
    find_diff(p_actual, p_desired)

if __name__ == "__main__":
    main()
