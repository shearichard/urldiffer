# urldiffer
A number of command line utilities to help analyse the difference between a set of URL's

The .INI used by urldiffer.py looks like this :

    [baseline]
    baseurl = https://wiki.python.org/moin/ConfigParserExamples/
    [comparisons]
    url1 = TFF|FIN|/query/?0_description=~&0_closed=0&0_owner=137&0_financial_colour=red&1_closed=0&1_data_entry_user=137&1_financial_colour=red&order=id&col=id&col=description&col=owner&col=data_entry_user&col=financial_colour&col=budget&col=actual&col=forecast&col=financial_variance&col=financial_explanation&as_of=as_of 
    url2 = TFF|INHERENTRISK|/query/?0_description=~&0_closed=u0&0_owner=137&0_risk_colour=red&1_closed=u0&1_data_entry_user=137&1_risk_colour=red&order=id&include_underlying=1&col=id&col=description&col=owner&col=data_entry_user&col=risk_colour&col=risk_description&col=risk_recommendation&col=risk_residual_colour&as_of=as_of
    url3 = TFF|MITIGATEDRISK|/query/?0_description=~&0_closed=u0&0_owner=137&0_risk_residual_colour=red&1_closed=u0&1_data_entry_user=137&1_risk_residual_colour=red&order=id&include_underlying=1&col=id&col=description&col=owner&col=data_entry_user&col=risk_colour&col=risk_description&col=risk_recommendation&col=risk_residual_colour&as_of=as_of
    url4 =TTF|FIN|https://design.opal3.com/query/?0_description=~&0_closed=u0&0_owner=137&0_financial_colour=red&1_closed=u0&1_data_entry_user=137&1_financial_colour=red&order=id&include_underlying=1&col=id&col=description&col=owner&col=data_entry_user&col=financial_colour&col=budget&col=actual&col=forecast&col=financial_variance&col=financial_explanation&as_of=as_of
    url5 =TTF|INHERENTRISK|https://design.opal3.com/query/?0_description=~&0_closed=u0&0_owner=137&0_risk_colour=red&1_closed=u0&1_data_entry_user=137&1_risk_colour=red&order=id&include_underlying=1&col=id&col=description&col=owner&col=data_entry_user&col=risk_colour&col=risk_description&col=risk_recommendation&col=risk_residual_colour&as_of=as_of
    url6 =TTF|MITIGATEDRISK|https://design.opal3.com/query/?0_description=~&0_closed=u0&0_owner=137&0_risk_residual_colour=red&1_closed=u0&1_data_entry_user=137&1_risk_residual_colour=red&order=id&include_underlying=1&col=id&col=description&col=owner&col=data_entry_user&col=risk_colour&col=risk_description&col=risk_recommendation&col=risk_residual_colour&as_of=as_of
    [excludecategories]
    cat1=INHERENTRISK
    cat2=MITIGATEDRISK

