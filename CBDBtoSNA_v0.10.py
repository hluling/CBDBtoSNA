import sys
import argparse
import timeit
import datetime
from lxml import etree as et

def add_att_GEXF(atts_Elt, att_name, att_value):
    try:
        et.SubElement(atts_Elt,'attvalue',{'for':att_name,
                                           'value':att_value})
    except TypeError:
        pass

def add_att_GRAPHML(node_edge_Elt, att_name, att_value):
    try:
        data_Elt = et.SubElement(node_edge_Elt,'data',{'key':att_name})
        data_Elt.text = att_value
    except TypeError:
        pass

def add_edge_GEXF(edge_id,source,target,tie,edges_Elt):
    tie_type = tie.tag
    bibli = tie.xpath('Source')[0].text
    alter_name = tie.xpath('KinPersonName | AssocPersonName')[0].text
    tie_name = tie.xpath('KinRelName | AssocName')[0].text
   
    edge_Elt = et.SubElement(edges_Elt,'edge',{'id':'e'+str(edge_id),
                                               'source':'n'+source,
                                               'target':'n'+target})
    edge_atts_Elt = et.SubElement(edge_Elt,'attvalues')
    for att_name, att_value in zip(['e@label','e@bibl','e@edgeType'],[tie_name,bibli,tie_type]):
        add_att_GEXF(edge_atts_Elt,att_name,att_value)
    return edges_Elt

def add_edge_GRAPHML(edge_id,source,target,tie,edges_str):
    tie_type = tie.tag
    bibli = tie.xpath('Source')[0].text
    alter_name = tie.xpath('KinPersonName | AssocPersonName')[0].text
    tie_name = tie.xpath('KinRelName | AssocName')[0].text
   
    edge_Elt = et.Element('edge',{'id':'e'+str(edge_id),
                                               'source':'n'+source,
                                               'target':'n'+target})

    for att_name, att_value in zip(['e@label','e@bibl','e@edgeType'],[tie_name,bibli,tie_type]):
        add_att_GRAPHML(edge_Elt,att_name,att_value)
    edge_str = str(et.tostring(edge_Elt,encoding='unicode',pretty_print=True))
    edges_str += edge_str
    return (edges_str,edge_id)

def add_node_GEXF(person,nodes_Elt,nodes_set):
    person_info = person.xpath('BasicInfo')[0]
    node_id = person_info.xpath('PersonId')[0].text
    chname = person_info.xpath('ChName')[0].text
    year_b = person_info.xpath('YearBirth')[0].text
    year_d = person_info.xpath('YearDeath')[0].text
    gender = person_info.xpath('Gender')[0].text
    year_i = person_info.xpath('IndexYear')[0].text
    dynasty = person_info.xpath('Dynasty')[0].text
    if node_id in nodes_set:
        print('Adding node:', node_id)    
        node_Elt = et.SubElement(nodes_Elt,'node',{'id':'n'+person_info.xpath('PersonId')[0].text,
                                                   'label':person_info.xpath('EngName')[0].text})
        node_atts_Elt = et.SubElement(node_Elt,'attvalues')

        for att_name,att_value in zip(['n@chName','n@birthY','n@deathY','n@gender','n@indexYear','n@dynasty'],
                                      [chname,year_b,year_d,gender,year_i,dynasty]):
            add_att_GEXF(node_atts_Elt,att_name,att_value)
        nodes_set.remove(node_id)
    return (nodes_Elt,nodes_set)

def add_node_GRAPHML(person,nodes_str,nodes_set):
    person_info = person.xpath('BasicInfo')[0]
    node_id = person_info.xpath('PersonId')[0].text
    chname = person_info.xpath('ChName')[0].text
    year_b = person_info.xpath('YearBirth')[0].text
    year_d = person_info.xpath('YearDeath')[0].text
    gender = person_info.xpath('Gender')[0].text
    year_i = person_info.xpath('IndexYear')[0].text
    dynasty = person_info.xpath('Dynasty')[0].text
    engname = person_info.xpath('EngName')[0].text
    if node_id in nodes_set:
        print('Adding node:', node_id)    
        node_Elt = et.Element('node',{'id':'n'+person_info.xpath('PersonId')[0].text})
                                      #'label':person_info.xpath('EngName')[0].text})

        for att_name,att_value in zip(['n@chName','n@birthY','n@deathY','n@gender','n@indexYear','n@dynasty','n@label'],
                                      [chname,year_b,year_d,gender,year_i,dynasty,engname]):
            add_att_GRAPHML(node_Elt,att_name,att_value)
        
        node_str = str(et.tostring(node_Elt,encoding='unicode',pretty_print=True))
        nodes_str += node_str
        nodes_set.remove(node_id)
    return (nodes_str,nodes_set)

def add_outside_node_GEXF(name,ID,nodes_Elt): # Add nodes that are not one of the Persons in CBDB.
    if name is None:
        node_Elt = et.SubElement(nodes_Elt,'node',{'id':'n'+ID,
                                               'label':'Unknown'})
    else:
        node_Elt = et.SubElement(nodes_Elt,'node',{'id':'n'+ID,
                                                   'label':name})

def add_outside_node_GRAPHML(name,ID,nodes_str): # Add nodes that are not one of the Persons in CBDB.
    if name is None:
        node_Elt = et.Element('node',{'id':'n'+ID})
                                      #'label':'Unknown'})
        add_att_GRAPHML(node_Elt,'n@label','Unknown')
    else:
        node_Elt = et.Element('node',{'id':'n'+ID})
                                      #'label':name})
        add_att_GRAPHML(node_Elt,'n@label',name)
    node_str = str(et.tostring(node_Elt,encoding='unicode',pretty_print=True))
    nodes_str += node_str
    return nodes_str

def process_person_GEXF(person,edge_id,edges_Elt,nodes_set):
    ego_id = person.xpath('BasicInfo/PersonId')[0].text
    print('Processing person:',ego_id)
    nodes_set.add(ego_id)
    all_ties = person.xpath('PersonKinshipInfo/Kinship | PersonSocialAssociation/Association')
    if len(all_ties) > 0:
        for tie in all_ties:
            alter_id = tie.xpath('KinPersonId | AssocPersonId')[0].text
            if alter_id == '0' or alter_id == '9999':
                continue
            else:
                add_edge_GEXF(edge_id,ego_id,alter_id,tie,edges_Elt)
                edge_id += 1
                nodes_set.add(alter_id)
    return edge_id

def process_person_GRAPHML(person,edge_id,edges_str,nodes_set):
    ego_id = person.xpath('BasicInfo/PersonId')[0].text
    print('Processing person:',ego_id)
    nodes_set.add(ego_id)
    all_ties = person.xpath('PersonKinshipInfo/Kinship | PersonSocialAssociation/Association')
    if len(all_ties) > 0:
        for tie in all_ties:
            alter_id = tie.xpath('KinPersonId | AssocPersonId')[0].text
            if alter_id == '0' or alter_id == '9999':
                continue
            else:
                edges_str,edge_id=add_edge_GRAPHML(edge_id,ego_id,alter_id,tie,edges_str)
                edge_id += 1
                nodes_set.add(alter_id)
    return (edges_str,edge_id)

def process_person_pid_GEXF(person,edge_id,edges_Elt,nodes_set,targets_set,degree):
    ego_id = person.xpath('BasicInfo/PersonId')[0].text
    print('Processing person:',ego_id)
    nodes_set.add(ego_id)
    all_ties = person.xpath('PersonKinshipInfo/Kinship | PersonSocialAssociation/Association')
    if len(all_ties) > 0:
        for tie in all_ties:
            alter_id = tie.xpath('KinPersonId | AssocPersonId')[0].text
            if alter_id == '0' or alter_id == '9999':
                continue
            else:
                add_edge_GEXF(edge_id,ego_id,alter_id,tie,edges_Elt)
                edge_id += 1
                nodes_set.add(alter_id)
                if degree > 1:
                    targets_set.add(alter_id)
    return edge_id

def process_person_pid_GRAPHML(person,edge_id,edges_str,nodes_set,targets_set,degree):
    ego_id = person.xpath('BasicInfo/PersonId')[0].text
    print('Processing person:',ego_id)
    nodes_set.add(ego_id)
    all_ties = person.xpath('PersonKinshipInfo/Kinship | PersonSocialAssociation/Association')
    if len(all_ties) > 0:
        for tie in all_ties:
            alter_id = tie.xpath('KinPersonId | AssocPersonId')[0].text
            if alter_id == '0' or alter_id == '9999':
                continue
            else:
                edges_str,edge_id = add_edge_GRAPHML(edge_id,ego_id,alter_id,tie,edges_str)
                edge_id += 1
                nodes_set.add(alter_id)
                if degree > 1:
                    targets_set.add(alter_id)
    return edges_str,edge_id

def get_years(person, bid):
    xpth = 'BasicInfo/' + bid
    year = person.xpath(xpth)[0].text
    if year == None or year == '0':
            year = None
    else:
        year = int(year)
    return year

def get_gender(person):
    xpth = 'BasicInfo/Gender'
    gender = person.xpath(xpth)[0].text
    return gender

def get_pid(person):
    xpth = 'BasicInfo/PersonId'
    pid = person.xpath(xpth)[0].text
    return pid

def filter_by_years(start_y,end_y,year_b,year_d,year_i):
    if year_b is not None:
        if year_b > end_y:
            decision = 'out'
        elif start_y <= year_b <= end_y:
            decision = 'in'
        else:
            if year_d is not None:
                if year_d < start_y:
                    decision = 'out'
                else:
                    decision = 'in'
            else:
                if year_i is not None:
                    if year_i < start_y:
                        decision = 'out'
                    else:
                        decision = 'in'
                else:
                    decision = 'out'
    else:
        if year_d is not None:
            if year_d < start_y:
                decision = 'out'
            elif start_y <= year_d <= end_y:
                decision = 'in'
            else:
                if year_i is not None:
                    if year_i > end_y:
                        decision = 'out'
                    else:
                        decision = 'in'
        else:
            if year_i is not None:
                if start_y <= year_i <= end_y:
                    decision = 'in'
                else:
                    decision = 'out'
            else:
                decision = 'out'

    return decision

def filter_by_year(start_y,end_y,year_b,year_d,year_i):
    if start_y is None:
        year = end_y
        if year_b is not None:
            if year_b <= year:
                decision = 'in'
        elif year_d is not None:
            if year_d <= year:
                decision = 'in'
            else:
                if year_i is not None:
                    if year_i <= year:
                        decision = 'in'
        elif year_i is not None:
            if year_i <= year:
                decision = 'in'
    else:
        year = start_y
        if year_d is not None:
            if year_d >= year:
                decision = 'in'
        elif year_b is not None:
            if year_b >= year:
                decision = 'in'
            else:
                if year_i is not None:
                    if year_i >= year:
                        decision = 'in'
        elif year_i is not None:
            if year_i >= year:
                decision = 'in'
    try:
        decision
    except UnboundLocalError:
        decision = 'out'
    return decision

def parse_person_GEXF(xml,edge_id,edges_Elt,nodes_set,targets_set,tartarts_set,start_y,end_y,gender,pid_l,degree):
    if pid_l is not None:
        pid_left = len(pid_l)
    context = et.iterparse(xml, events=('end',), tag='Person')
    for event, element in context:
        year_b = get_years(element,'YearBirth')
        year_d = get_years(element,'YearDeath')
        year_i = get_years(element,'IndexYear')
        gender_p = get_gender(element)
        pid = get_pid(element)

        if pid_l is not None:
            if pid in pid_l:
                edge_id = process_person_pid_GEXF(element,edge_id,edges_Elt,nodes_set,targets_set,degree)
                pid_left -= 1

        else:
            
            if gender is not None and start_y is None and end_y is None: # May delete this condition later, 11/26/2018, LH.
                if gender_p == str(gender):
                    edge_id = process_person_GEXF(element,edge_id,edges_Elt,nodes_set)
            if gender is not None and start_y is not None and end_y is not None:
                decision = filter_by_years(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    if gender_p == str(gender):
                        edge_id = process_person_GEXF(element,edge_id,edges_Elt,nodes_set)
                    else:
                        continue
            if gender is None and start_y is not None and end_y is not None:
                
                decision = filter_by_years(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    edge_id = process_person_GEXF(element,edge_id,edges_Elt,nodes_set)

            if gender is None and ((start_y is not None and end_y is None) or (start_y is None and end_y is not None)):
                decision = filter_by_year(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    edge_id = process_person_GEXF(element,edge_id,edges_Elt,nodes_set)

            if gender is not None and ((start_y is not None and end_y is None) or (start_y is None and end_y is not None)):
                decision = filter_by_year(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    if gender_p == str(gender):
                        edge_id = process_person_GEXF(element,edge_id,edges_Elt,nodes_set)
                    else:
                        continue

        element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if pid_l is not None:
            if pid_left == 0:
                break
    del context
    return edge_id

def parse_person_GRAPHML(xml,edge_id,edges_str,nodes_set,targets_set,tartarts_set,start_y,end_y,gender,pid_l,degree):
    if pid_l is not None:
        pid_left = len(pid_l)
    context = et.iterparse(xml, events=('end',), tag='Person')
    for event, element in context:
        year_b = get_years(element,'YearBirth')
        year_d = get_years(element,'YearDeath')
        year_i = get_years(element,'IndexYear')
        gender_p = get_gender(element)
        pid = get_pid(element)

        if pid_l is not None:
            if pid in pid_l:
                edges_str,edge_id = process_person_pid_GRAPHML(element,edge_id,edges_str,nodes_set,targets_set,degree)
                pid_left -= 1

        else:
            
            if gender is not None and start_y is None and end_y is None: # May delete this condition later, 11/26/2018, LH.
                if gender_p == str(gender):
                    edges_str,edge_id = process_person_GRAPHML(element,edge_id,edges_str,nodes_set)
            if gender is not None and start_y is not None and end_y is not None:
                decision = filter_by_years(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    if gender_p == str(gender):
                        edges_str,edge_id = process_person_GRAPHML(element,edge_id,edges_str,nodes_set)
                    else:
                        continue
            if gender is None and start_y is not None and end_y is not None:
                
                decision = filter_by_years(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    edges_str,edge_id = process_person_GRAPHML(element,edge_id,edges_str,nodes_set)

            if gender is None and ((start_y is not None and end_y is None) or (start_y is None and end_y is not None)):
                decision = filter_by_year(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    edges_str,edge_id = process_person_GRAPHML(element,edge_id,edges_str,nodes_set)

            if gender is not None and ((start_y is not None and end_y is None) or (start_y is None and end_y is not None)):
                decision = filter_by_year(start_y,end_y,year_b,year_d,year_i)
                if decision == 'out':
                    continue
                else:
                    if gender_p == str(gender):
                        edges_str,edge_id = process_person_GRAPHML(element,edge_id,edges_str,nodes_set)
                    else:
                        continue

        element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if pid_l is not None:
            if pid_left == 0:
                break
    del context
    return (edges_str,edge_id)

def create_fn_year(start_y,end_y):
    if start_y is None:
        str_start_y = ''
        if end_y < 0:
            str_end_y = str(abs(end_y)) + 'BCE'
        else:
            str_end_y = str(end_y) + 'CE'
        str_end_y = '_TO_' + str_end_y
    else:
        str_end_y = ''
        if start_y < 0:
            str_start_y = str(abs(start_y)) + 'BCE'
        else:
            str_start_y = str(start_y) + 'CE'
        str_start_y = '_FROM_' + str_start_y
    return str_start_y,str_end_y

def create_fn_years(start_y,end_y):
    if start_y < 0:
            str_start_y = '_' + str(abs(start_y)) + 'BCE'
    else:
        str_start_y = '_' + str(start_y) + 'CE'
    if end_y < 0:
        str_end_y = '_' + str(abs(end_y)) + 'BCE'
    else:
        str_end_y = '_' + str(end_y) + 'CE'
    return str_start_y,str_end_y


def toGEXF(xml,start_y,end_y,gender,pid_l,degree):
    # Initialization:
    nodes_Elt = et.Element('nodes')
    edges_Elt = et.Element('edges')
    nodes_set = set()
    targets_set = set() # If degree is 2, selected person's targets are put in this set.
    tartarts_set = set() # If degree is 3, selected person's targets' targets are put in this set.
    empty_set = set()
    edge_id = 0

    # Select persons by (1) year, with or without gender, or (2) person IDs, with or without degree. Then, add edges.
    edge_id = parse_person_GEXF(xml,edge_id,edges_Elt,nodes_set,targets_set,tartarts_set,start_y,end_y,gender,pid_l,degree)

    # If person IDs are used, and degree is set to 2, add more nodes and edges.
    if degree == 2:
        next_degree = 1
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in targets_set:
                edge_id = process_person_pid_GEXF(element,edge_id,edges_Elt,nodes_set,empty_set,next_degree)
                targets_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(targets_set) == 0:
                break
        del context

    # If person IDs are used, and degree is set to 3, add more nodes and edges, and more nodes and edges.
    if degree == 3:
        next_degree = 2
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in targets_set:
                edge_id = process_person_pid_GEXF(element,edge_id,edges_Elt,nodes_set,tartarts_set,next_degree)
                targets_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(targets_set) == 0:
                break
        del context

        next_degree = 1
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in tartarts_set:
                edge_id = process_person_pid_GEXF(element,edge_id,edges_Elt,nodes_set,empty_set,next_degree)
                tartarts_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(tartarts_set) == 0:
                break
        del context
            

    # Add nodes inside CBDB.
    context = et.iterparse(xml, events=('end',), tag='Person')
    for event, element in context:
        nodes_Elt,nodes_set = add_node_GEXF(element,nodes_Elt,nodes_set)
        element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if len(nodes_set) == 0:
            break
    del context

    # Add nodes outside CBDB if there's any.
    if len(nodes_set) != 0:
        context = et.iterparse(xml, events=('end',), tag=('KinPersonId','AssocPersonId'))
        outsiders = set()
        for event, element in context:
            alter_id = element.text
            if alter_id in nodes_set:
                try:
                    matched_name = element.xpath('following-sibling::*[1]')[0].text
                except IndexError:
                    matched_name = 'Unknown'
                if alter_id not in outsiders:
                    print('Adding outside node:',alter_id)
                    add_outside_node_GEXF(matched_name,alter_id,nodes_Elt)
                    outsiders.add(alter_id)
                    nodes_set.remove(alter_id)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(nodes_set) == 0:
                break
        del context

    # Create a GEXF filename.
    if pid_l is not None:
        str_pid = '_'.join(pid_l)
        str_degree = '_' + 'Degree' + str(degree)
        filename = 'CBDBtoGEXF' + '_' + str_pid + str_degree + '.gexf'
    else:
        if None in [start_y,end_y]:
            str_start_y,str_end_y = create_fn_year(start_y,end_y)
        else:
            str_start_y,str_end_y = create_fn_years(start_y,end_y)
            
        if gender is None:
            str_gd = ''
        elif gender == 0:
            str_gd = '_Male'
        else:
            str_gd = '_Female' 
        
        filename = 'CBDBtoGEXF' + str_start_y + str_end_y + str_gd + '.gexf'

    # GEXF formalities:
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    meta = '''<?xml version="1.0" encoding="UTF-8"?> 
    <gexf xmlns="http://www.gexf.net/1.2draft"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.gexf.net/1.2draft
                            http://www.gexf.net/1.2draft/gexf.xsd"
        version="1.2">
    <meta lastmodifieddate={!r}>
        <creator>CBDB XML-API output: Simon Wiles, Transformed to GEXF: LH and MB</creator>
        <description>This network contains kinship and social relations of the selected CBDB persons.</description>
    </meta>
    <graph defaultedgetype="undirected" mode="static">
        <attributes class="node">
            <attribute id="n@chName" title="chName" type="string"/>
            <attribute id="n@birthY" title="birthY" type="integer"/>
            <attribute id="n@deathY" title="deathY" type="integer"/>
            <attribute id="n@gender" title="gender" type="integer"/>
            <attribute id="n@indexYear" title="index" type="integer"/>
            <attribute id="n@dynasty" title="dynasty" type="string"/>
        </attributes>
        <attributes class="edge">
            <attribute id="e@label" title="label" type="string"/>
            <attribute id="e@bibl" title="source" type="string"/>
            <attribute id="e@edgeType" title="edgeType" type="string"/>
        </attributes>\n'''.format(today)

    # Concatenate string objects for GEXF.
    page = meta + str(et.tostring(nodes_Elt,encoding='unicode',pretty_print=True) + et.tostring(edges_Elt,encoding='unicode',pretty_print=True)) + '</graph></gexf>'
    
    # Write to file.
    with open(filename,'w') as f:
        f.write(page)
    print('Done writing file in GEXF.')

def toGRAPHML(xml,start_y,end_y,gender,pid_l,degree):
    # Initialization:
    nodes_str = ""
    edges_str = ""
    nodes_set = set()
    targets_set = set() # If degree is 2, selected person's targets are put in this set.
    tartarts_set = set() # If degree is 3, selected person's targets' targets are put in this set.
    empty_set = set()
    edge_id = 0

    # Select persons by (1) year, with or without gender, or (2) person IDs, with or without degree. Then, add edges.
    edges_str,edge_id = parse_person_GRAPHML(xml,edge_id,edges_str,nodes_set,targets_set,tartarts_set,start_y,end_y,gender,pid_l,degree)

    # If person IDs are used, and degree is set to 2, add more nodes and edges.
    if degree == 2:
        next_degree = 1
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in targets_set:
                edges_str,edge_id = process_person_pid_GRAPHML(element,edge_id,edges_str,nodes_set,empty_set,next_degree)
                targets_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(targets_set) == 0:
                break
        del context

    # If person IDs are used, and degree is set to 3, add more nodes and edges, and more nodes and edges.
    if degree == 3:
        next_degree = 2
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in targets_set:
                edges_str,edge_id = process_person_pid_GRAPHML(element,edge_id,edges_str,nodes_set,tartarts_set,next_degree)
                targets_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(targets_set) == 0:
                break
        del context

        next_degree = 1
        context = et.iterparse(xml, events=('end',), tag='Person')
        for event, element in context:
            pid = get_pid(element)
            if pid in tartarts_set:
                edges_str,edge_id = process_person_pid_GRAPHML(element,edge_id,edges_str,nodes_set,empty_set,next_degree)
                tartarts_set.remove(pid)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(tartarts_set) == 0:
                break
        del context
            

    # Add nodes inside CBDB.
    context = et.iterparse(xml, events=('end',), tag='Person')
    for event, element in context:
        nodes_str,nodes_set = add_node_GRAPHML(element,nodes_str,nodes_set)
        element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if len(nodes_set) == 0:
            break
    del context

    # Add nodes outside CBDB if there's any.
    if len(nodes_set) != 0:
        context = et.iterparse(xml, events=('end',), tag=('KinPersonId','AssocPersonId'))
        outsiders = set()
        for event, element in context:
            alter_id = element.text
            if alter_id in nodes_set:
                try:
                    matched_name = element.xpath('following-sibling::*[1]')[0].text
                except IndexError:
                    matched_name = 'Unknown'
                if alter_id not in outsiders:
                    print('Adding outside node:',alter_id)
                    nodes_str = add_outside_node_GRAPHML(matched_name,alter_id,nodes_str)
                    outsiders.add(alter_id)
                    nodes_set.remove(alter_id)
            element.clear()
            for ancestor in element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
            if len(nodes_set) == 0:
                break
        del context

    # Create a GraphML filename.
    if pid_l is not None:
        str_pid = '_'.join(pid_l)
        str_degree = '_' + 'Degree' + str(degree)
        filename = 'CBDBtoGraphML' + '_' + str_pid + str_degree + '.graphml'
    else:
        if None in [start_y,end_y]:
            str_start_y,str_end_y = create_fn_year(start_y,end_y)
        else:
            str_start_y,str_end_y = create_fn_years(start_y,end_y)
            
        if gender is None:
            str_gd = ''
        elif gender == 0:
            str_gd = '_Male'
        else:
            str_gd = '_Female' 
        
        filename = 'CBDBtoGraphML' + str_start_y + str_end_y + str_gd + '.graphml'

    # GraphML formalities:
    meta = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- CBDB XML-API output: Simon Wiles, Transformed to Graph: LH and MB
This network contains kinship and social relations of the selected CBDB persons.-->
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
    <graph id="G" edgedefault="undirected">
        <key id="n@chName" for="node" attr.name="chName" attr.type="string"/>
        <key id="n@birthY" for="node" attr.name="birthY" attr.type="int"/>
        <key id="n@deathY" for="node" attr.name="deathY" attr.type="int"/>
        <key id="n@gender" for="node" attr.name="gender" attr.type="int"/>
        <key id="n@indexYear" for="node" attr.name="index" attr.type="int"/>
        <key id="n@dynasty" for="node" attr.name="dynasty" attr.type="string"/>
        <key id="n@label" for="node" attr.name="label" attr.type="string"/>
        <key id="e@label" for="edge" attr.name="label" attr.type="string"/>
        <key id="e@bibl" for="edge" attr.name="source" attr.type="string"/>
        <key id="e@edgeType" for="edge" attr.name="edgeType" attr.type="string"/>\n'''

    # Concatenate string objects for GraphML.
    page = meta + nodes_str + edges_str + '</graph></graphml>'
    
    # Write to file.
    with open(filename,'w') as f:
        f.write(page)
    print('Done writing file in GraphML.')

if __name__=='__main__':
    start_time = timeit.default_timer()

    parser = argparse.ArgumentParser()
    
    # Positional (required) arguments: 
    parser.add_argument("xmlInput", help="The CBDB XML input file",type=str)
    parser.add_argument("outputFormat", help="Output file format: 'GEXF' or 'GraphML', NOT case sensitive",type=str)

    # Optional arguments:
    parser.add_argument("-f","--fromY",
                        help="The start of a year range; prepend '-' for BCE",
                        type=int)
    parser.add_argument("-t","--toY",
                        help="The end of a year range; prepend '-' for BCE",
                        type=int)
    parser.add_argument("-g","--gender",
                        help="1 for male, 2 for female;c ISO/IEC 5218",
                        type=int)
    parser.add_argument("-pid","--personID",
                        nargs='+',
                        help="One or more person IDs, no more than ten. Separate by a space. Don't prepend leading zeros. If this parameter is used, no other parameters can be used.",
                        type=str)
    parser.add_argument("-d","--degree",
                        help="Degree of stretch, if person ID is used. Maximum: 2 in the current version.",
                        type=int,
                        default=1)
    
    args = parser.parse_args()
    
    xml = args.xmlInput
    opformat = args.outputFormat

    start_y = args.fromY
    end_y = args.toY
    gender = args.gender
    pid_l = args.personID
    degree = args.degree

    # Recode gender:
    if gender is not None:
        if gender == 1:
            gender = 0
        else:
            gender = 1
    
    # Validate user inputs:
    if xml.endswith('.xml') == False:
        sys.exit("Please enter the correct .xml file extension.")

    if all(x is None for x in [pid_l,start_y,end_y,gender]) == True:
        sys.exit("Please enter one or more parameter options. See the README file.")
    
    if None not in [start_y,end_y]:
        if start_y > end_y:
            sys.exit("'From' year should NOT be greater than 'to' year. Enter the parameters again.")
    
    if start_y == 0 or end_y == 0:
        sys.exit('No Year Zero. Enter the parameters again.')

    if gender is not None and (all(x is None for x in [pid_l,start_y,end_y]) == True): # If only gender is used, the size of the GEXF file might become too large.
        sys.exit('Specify at least one end of year range or use person ID. Enter the parameters again.')

    if pid_l is not None and (any(x is not None for x in [start_y,end_y,gender]) == True):
        sys.exit('If person ID is used for query, the year and the gender parameters cannot be used. Enter person ID only, with or without the degree parameter.')

    if pid_l is not None:
        if len(pid_l) > 10:
            sys.exit('No more than 10 person IDs are allowed.')

    if degree > 3:
        sys.exit('Maximum degree is 3.')

    if opformat.lower() == 'gexf':
        toGEXF(xml,start_y,end_y,gender,pid_l,degree)
        elapsed = timeit.default_timer() - start_time
        print('Execution time: %s seconds' % (elapsed))
    elif opformat.lower() == 'graphml':
        toGRAPHML(xml,start_y,end_y,gender,pid_l,degree)
        elapsed = timeit.default_timer() - start_time
        print('Execution time: %s seconds' % (elapsed))
    else:
        sys.exit("Please input one of the correct output formats: 'GEXF' or 'GraphML' (NOT case sensitive).")
    