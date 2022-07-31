from argparse import Namespace
import argparse
from fileinput import close
import ntpath
from email import header
from json.tool import main
from pickle import TRUE
from sys import addaudithook
from SPARQLWrapper import SPARQLWrapper, JSON

import pandas as pd
import xml.etree.ElementTree as ET
import urllib.parse
import urllib

import requests
import subprocess

import re  #import for regex to filter out Q identifier


#global dict containing abbreviations for countries and full forms
#this is used to filter the sparql queries later on
country_dict = {'BE':'Belgium', 'BG':'Bulgaria', 'CZ':'Czech Republic', 'DK':'Denmark', 'ES': 'Spain', 'FR':'France', 'GB':'United Kingdom', 'HR':'Croatia', 'HU':'Hungary', 'IS':'Iceland', 'IT':'Italy', 'LT':'Lithuania', 'LV':'Latvia', 'NL':'Netherlands', 'PL':'Poland', 'SI':'Slovenia', 'TR':'Turkey'}

ct_person_query1 = 0
ct_person_query2 = 0
ct_person_query3 = 0
ct_person_query4 = 0
ct_person_query5 = 0
ct_person_query6 = 0
ct_person_query7 = 0
ct_person_query8 = 0
ct_person_query9 = 0
ct_person_notfound = 0

ct_org_query1 = 0
ct_org_query2 = 0
ct_org_query3 = 0
ct_org_query4 = 0
ct_org_query5 = 0
ct_org_notfound = 0





#function to get the Wikidata identifier (e.g. Q1234) of a person
#based on the name of the person
#@param personName: name of person for which you need the wiki identifier
#return personwikiidentifier: identifier of the person on Wikidata (if available)
#if not available return Error
def findPersoninWiki(personName, language_xml, person, tree, party_tag_dict, namespace, nowikiid_filename, filepnowikiid, birthdateFound, country_id):
    
    #retrieve country name of corpus
    country_code = country_dict[country_id]
    full_party_name = ""
    personName = personName.replace("'", " ")
    
    
   
    #query with birthdate and country
    if birthdateFound != None:

        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        personQuery = str()
        personQuery = "SELECT DISTINCT ?item ?dob {"
        personQuery = personQuery + "SERVICE wikibase:mwapi {"
        personQuery = personQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
        personQuery = personQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
        personQuery = personQuery + "bd:serviceParam wikibase:limit 10 ."
        personQuery = personQuery + "bd:serviceParam mwapi:search '" + personName + "'."
        personQuery = personQuery + "bd:serviceParam mwapi:language '" + language_xml + "'."
        personQuery = personQuery + "?item wikibase:apiOutputItem mwapi:item."
        personQuery = personQuery + "?num wikibase:apiOrdinal true."
        personQuery = personQuery + "}"
        personQuery = personQuery + "?item (wdt:P279|wdt:P31) wd:Q5;"
        personQuery = personQuery + "wdt:P569 ?dob;"
        personQuery = personQuery + "wdt:P27 ?country."
        personQuery = personQuery + "?country rdfs:label ?label."
        personQuery = personQuery + "FILTER(LANG(?label) = 'en')."
        personQuery = personQuery + "FILTER(CONTAINS(?label, '" + country_code +"'))." 
        personQuery = personQuery + "FILTER('"+ birthdateFound +"'^^xsd:dateTime = ?dob)"
        personQuery = personQuery + "}"
        personQuery = personQuery + "ORDER BY ?searchTerm ?num "
        
        #set query
        sparql.setQuery(personQuery)
        
        #return format to JSON
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        resultsstr = str()

        #check to see if json is empty (i.e if the sparql query returned a result or not)
        try:
            resultsstr = results_df[['item.value']].to_string(index=False, header=False)
            indexslash = int()
            indexslash = resultsstr.rfind('/')
            
            #save wikidata identifier of person 
            personwikiidentifier = str()
            #access everything after index of last slash found in uri
            personwikiidentifier = resultsstr[indexslash + 1: ]
            global ct_person_query1
            ct_person_query1 += 1
            return str(personwikiidentifier)
        
        #query with birthdate and name
        except:
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
            personQuery = str()
            personQuery = "SELECT DISTINCT ?item ?dob {"
            personQuery = personQuery + "SERVICE wikibase:mwapi {"
            personQuery = personQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
            personQuery = personQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
            personQuery = personQuery + "bd:serviceParam wikibase:limit 10 ."
            personQuery = personQuery + "bd:serviceParam mwapi:search '" + personName + "'."
            personQuery = personQuery + "bd:serviceParam mwapi:language '" +language_xml+ "'."
            personQuery = personQuery + "?item wikibase:apiOutputItem mwapi:item."
            personQuery = personQuery + "?num wikibase:apiOrdinal true."
            personQuery = personQuery + "}"
            personQuery = personQuery + "?item (wdt:P279|wdt:P31) wd:Q5;"
            personQuery = personQuery + "wdt:P569 ?dob;"
            personQuery = personQuery + "FILTER('"+ birthdateFound +"'^^xsd:dateTime = ?dob)"
            personQuery = personQuery + "}"
            personQuery = personQuery + "ORDER BY ?searchTerm ?num "

            #set query
            sparql.setQuery(personQuery)
            
            #return format to JSON
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            results_df = pd.json_normalize(results['results']['bindings'])
            resultsstr = str()

            #check to see if json is empty (i.e if the sparql query returned a result or not)
            try:
                resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                indexslash = int()
                indexslash = resultsstr.rfind('/')
                
                #save wikidata identifier of person 
                personwikiidentifier = str()
                #access everything after index of last slash found in uri
                personwikiidentifier = resultsstr[indexslash + 1: ]
                global ct_person_query2
                ct_person_query2 += 1
                return str(personwikiidentifier)
            
            except:
                pass
        

    #query using only country and name of person, no birth date
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    personQuery = str()
    personQuery = "SELECT DISTINCT ?item ?dob {"
    personQuery = personQuery + "SERVICE wikibase:mwapi {"
    personQuery = personQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
    personQuery = personQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
    personQuery = personQuery + "bd:serviceParam wikibase:limit 1 ."
    personQuery = personQuery + "bd:serviceParam mwapi:search '" + personName + "'."
    personQuery = personQuery + "bd:serviceParam mwapi:language '" +language_xml+ "'."
    personQuery = personQuery + "?item wikibase:apiOutputItem mwapi:item."
    personQuery = personQuery + "?num wikibase:apiOrdinal true."
    personQuery = personQuery + "}"
    personQuery = personQuery + "?item (wdt:P279|wdt:P31) wd:Q5;"
    personQuery = personQuery + "wdt:P27 ?country."
    personQuery = personQuery + "?country rdfs:label ?label."
    personQuery = personQuery + "FILTER(LANG(?label) = 'en')."
    personQuery = personQuery + "FILTER(CONTAINS(?label, '" + country_code +"'))." 
    personQuery = personQuery + "}"
    personQuery = personQuery + "ORDER BY ?searchTerm ?num "
    
    #set query
    sparql.setQuery(personQuery)
    
    #return format to JSON
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    resultsstr = str()

    #check to see if json is empty (i.e if the sparql query returned a result or not)
    try:
        resultsstr = results_df[['item.value']].to_string(index=False, header=False)
        indexslash = int()
        indexslash = resultsstr.rfind('/')
        
        #save wikidata identifier of person 
        personwikiidentifier = str()
        #access everything after index of last slash found in uri
        personwikiidentifier = resultsstr[indexslash + 1: ]
        global ct_person_query3
        ct_person_query3 += 1
        return str(personwikiidentifier)   
        
    except:    
        #query using only the name
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        personQuery = str()
        personQuery = "SELECT DISTINCT ?item {"
        personQuery = personQuery + "SERVICE wikibase:mwapi {"
        personQuery = personQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
        personQuery = personQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
        personQuery = personQuery + "bd:serviceParam wikibase:limit 1 ."
        personQuery = personQuery + "bd:serviceParam mwapi:search '" + personName + "'."
        personQuery = personQuery + "bd:serviceParam mwapi:language '" +language_xml+ "'."
        personQuery = personQuery + "?item wikibase:apiOutputItem mwapi:item."
        personQuery = personQuery + "?num wikibase:apiOrdinal true."
        personQuery = personQuery + "}"
        personQuery = personQuery + "?item (wdt:P279|wdt:P31) wd:Q5."
        personQuery = personQuery + "}"
        personQuery = personQuery + "ORDER BY ?searchTerm ?num "
        #set query
        sparql.setQuery(personQuery)
        
        #return format to JSON
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        resultsstr = str()


        #check to see if json is empty (i.e if the sparql query returned a result or not)
        try:
            resultsstr = results_df[['item.value']].to_string(index=False, header=False)
            #find index of last slash in return uri
            #because that is where identifier is placed in return uri
            indexslash = int()
            indexslash = resultsstr.rfind('/')
            
            #save wikidata identifier of person 
            personwikiidentifier = str()
            #access everything after index of last slash found in uri
            personwikiidentifier = resultsstr[indexslash + 1: ]
            global ct_person_query4
            ct_person_query4 += 1
            return str(personwikiidentifier)

        #if person not found in wikidata in first query using the full name including middle names
        #try second query with only one first name and one last name
        #some people might have Wikidata pages only with one forename and one last name
        except:
            split_persname = []
            personName = personName.strip()
            split_persname = personName.split(' ')
            #do a query only with first and last name to make sure there is no wikidata page already
            #maybe without middle names etc
            #new name, birth date, country
            if birthdateFound != None:
                if len(split_persname) > 2:
                    new_name = split_persname[0] + " " + split_persname[len(split_persname) -1]
                    personName = personName.replace("'", " ")
                    sparql_2 = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                    personQuery_2 = str()

                    personQuery_2 = "SELECT DISTINCT ?item {"
                    personQuery_2 = personQuery_2 + "SERVICE wikibase:mwapi {"
                    personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:api 'EntitySearch'."
                    personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
                    personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:limit 10 ."
                    personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:search '" + new_name + "'."
                    personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:language '" +language_xml+ "'."
                    personQuery_2 = personQuery_2 + "?item wikibase:apiOutputItem mwapi:item."
                    personQuery_2 = personQuery_2 + "?num wikibase:apiOrdinal true."
                    personQuery_2 = personQuery_2 + "}"
                    personQuery_2 = personQuery_2 + "?item (wdt:P279|wdt:P31) wd:Q5;"
                    personQuery_2 = personQuery_2 + "wdt:P569 ?dob;"
                    personQuery_2 = personQuery_2 + "wdt:P27 ?country."
                    personQuery_2 = personQuery_2 + "?country rdfs:label ?label."
                    personQuery_2 = personQuery_2 + "FILTER(LANG(?label) = 'en')."
                    personQuery_2 = personQuery_2 + "FILTER(CONTAINS(?label, '" + country_code +"'))." 
                    personQuery_2 = personQuery_2 + "FILTER('"+ birthdateFound +"'^^xsd:dateTime = ?dob)"
                    personQuery_2 = personQuery_2 + "}"
                    personQuery_2 = personQuery_2 + "ORDER BY ?searchTerm ?num "
                
                    #set query
                    sparql_2.setQuery(personQuery_2)
                    
                    #return format to JSON
                    sparql_2.setReturnFormat(JSON)
                    results = sparql_2.query().convert()
                    results_df = pd.json_normalize(results['results']['bindings'])
                    resultsstr = str()
            
                #check to see if json is empty (i.e if the sparql query returned a result or not)
                try:
                    
                    resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                    #find index of last slash in return uri
                    #because that is where identifier is placed in return uri
                    indexslash = int()
                    indexslash = resultsstr.rfind('/')
                
                    #save wikidata identifier of person 
                    personwikiidentifier = str()
                    #access everything after index of last slash found in uri
                    personwikiidentifier = resultsstr[indexslash + 1: ]
                    global ct_person_query5
                    ct_person_query5 += 1
                    return str(personwikiidentifier)

                except:
                    split_persname = []
                    personName = personName.strip()
                    split_persname = personName.split(' ')
                    #do a query only with first and last name to make sure there is no wikidata page already
                    #maybe without middle names etc
                    #query for abb name and bd
                    if len(split_persname) > 2:
                        new_name = split_persname[0] + " " + split_persname[len(split_persname) -1]
                        personName = personName.replace("'", " ")
                        sparql_2 = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                        personQuery_2 = str()
                        personQuery_2 = "SELECT DISTINCT ?item {"
                        personQuery_2 = personQuery_2 + "SERVICE wikibase:mwapi {"
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:api 'EntitySearch'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:limit 10 ."
                        personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:search '" + new_name + "'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:language '" +language_xml+ "'."
                        personQuery_2 = personQuery_2 + "?item wikibase:apiOutputItem mwapi:item."
                        personQuery_2 = personQuery_2 + "?num wikibase:apiOrdinal true."
                        personQuery_2 = personQuery_2 + "}"
                        personQuery_2 = personQuery_2 + "?item (wdt:P279|wdt:P31) wd:Q5;"
                        personQuery_2 = personQuery_2 + "wdt:P569 ?dob." 
                        personQuery_2 = personQuery_2 + "FILTER('"+ birthdateFound +"'^^xsd:dateTime = ?dob)"
                        personQuery_2 = personQuery_2 + "}"
                        personQuery_2 = personQuery_2 + "ORDER BY ?searchTerm ?num "
                        
                        #set query
                        sparql_2.setQuery(personQuery_2)
                        
                        #return format to JSON
                        sparql_2.setReturnFormat(JSON)
                        results = sparql_2.query().convert()
                        results_df = pd.json_normalize(results['results']['bindings'])
                        resultsstr = str()
                    
                        #check to see if json is empty (i.e if the sparql query returned a result or not)
                        try:
                            
                            resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                            #find index of last slash in return uri
                            #because that is where identifier is placed in return uri
                            indexslash = int()
                            indexslash = resultsstr.rfind('/')
                        
                            #save wikidata identifier of person 
                            personwikiidentifier = str()
                            #access everything after index of last slash found in uri
                            personwikiidentifier = resultsstr[indexslash + 1: ]
                            global ct_person_query6 
                            ct_person_query6 += 1
                            return str(personwikiidentifier)
                        except:
                            pass
                    
                
            
            #only query for abb name
            if len(split_persname) > 2:
                new_name = split_persname[0] + " " + split_persname[len(split_persname) -1]
                personName = personName.replace("'", " ")
                sparql_2 = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                personQuery_2 = str()
                personQuery_2 = "SELECT DISTINCT ?item {"
                personQuery_2 = personQuery_2 + "SERVICE wikibase:mwapi {"
                personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:api 'EntitySearch'."
                personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
                personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:limit 1 ."
                personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:search '" + new_name + "'."
                personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:language '" +language_xml+ "'."
                personQuery_2 = personQuery_2 + "?item wikibase:apiOutputItem mwapi:item."
                personQuery_2 = personQuery_2 + "?num wikibase:apiOrdinal true."
                personQuery_2 = personQuery_2 + "}"
                personQuery_2 = personQuery_2 + "?item (wdt:P279|wdt:P31) wd:Q5;"
                personQuery_2 = personQuery_2 + "wdt:P27 ?country."
                personQuery_2 = personQuery_2 + "?country rdfs:label ?label."
                personQuery_2 = personQuery_2 + "FILTER(LANG(?label) = 'en')."
                personQuery_2 = personQuery_2 + "FILTER(CONTAINS(?label, '" + country_code +"'))." 
                personQuery_2 = personQuery_2 + "}"
                personQuery_2 = personQuery_2 + "ORDER BY ?searchTerm ?num "
                
                #set query
                sparql_2.setQuery(personQuery_2)
                
                #return format to JSON
                sparql_2.setReturnFormat(JSON)
                results = sparql_2.query().convert()
                results_df = pd.json_normalize(results['results']['bindings'])
                resultsstr = str()
            
                #check to see if json is empty (i.e if the sparql query returned a result or not)
                try:
                    
                    resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                    #find index of last slash in return uri
                    #because that is where identifier is placed in return uri
                    indexslash = int()
                    indexslash = resultsstr.rfind('/')
                
                    #save wikidata identifier of person 
                    personwikiidentifier = str()
                    #access everything after index of last slash found in uri
                    personwikiidentifier = resultsstr[indexslash + 1: ]
                    global ct_person_query7
                    ct_person_query7 += 1
                    return str(personwikiidentifier)
    
                except:
                    if len(split_persname) > 2:
                        new_name = split_persname[0] + " " + split_persname[len(split_persname) -1]
                        personName = personName.replace("'", " ")
                        sparql_2 = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                        personQuery_2 = str()
                        personQuery_2 = "SELECT DISTINCT ?item {"
                        personQuery_2 = personQuery_2 + "SERVICE wikibase:mwapi {"
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:api 'EntitySearch'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam wikibase:limit 1 ."
                        personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:search '" + new_name + "'."
                        personQuery_2 = personQuery_2 + "bd:serviceParam mwapi:language '" +language_xml+ "'."
                        personQuery_2 = personQuery_2 + "?item wikibase:apiOutputItem mwapi:item."
                        personQuery_2 = personQuery_2 + "?num wikibase:apiOrdinal true."
                        personQuery_2 = personQuery_2 + "}"
                        personQuery_2 = personQuery_2 + "?item (wdt:P279|wdt:P31) wd:Q5."
                        personQuery_2 = personQuery_2 + "}"
                        personQuery_2 = personQuery_2 + "ORDER BY ?searchTerm ?num "
                        
                        #set query
                        sparql_2.setQuery(personQuery_2)
                        
                        #return format to JSON
                        sparql_2.setReturnFormat(JSON)
                        results = sparql_2.query().convert()
                        results_df = pd.json_normalize(results['results']['bindings'])
                        resultsstr = str()
                    
                        #check to see if json is empty (i.e if the sparql query returned a result or not)
                        try:
                            
                            resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                            #find index of last slash in return uri
                            #because that is where identifier is placed in return uri
                            indexslash = int()
                            indexslash = resultsstr.rfind('/')
                        
                            #save wikidata identifier of person 
                            personwikiidentifier = str()
                            #access everything after index of last slash found in uri
                            personwikiidentifier = resultsstr[indexslash + 1: ]
                            global ct_person_query8
                            ct_person_query8 += 1
                            return str(personwikiidentifier)


                        except:
                            #this query always for English language 
                            params = dict (
                                        action='wbsearchentities',
                                        format='json',
                                        language= 'en',
                                        uselang= 'en',
                                        type='item',
                                        search= personName
                                        )

                            response = requests.get('https://www.wikidata.org/w/api.php?', params).json() 
                    

                            try:
                                
                                response_out = response.get('search')[0]['id']
                                personwikiidentifier = response_out
                                global ct_person_query9
                                ct_person_query9 += 1
                                return str(personwikiidentifier)


                            except:
                                #if this second query also did not bring a result write info from corpus to a file
                                #write name, sex, gender, birthdate and affiliation to file
                                #also retrieve the affiliation/ party name the person is affiliated with so it can be added to Wikidata page which is created later on
                                print("Not found:      " + personName)
                                global ct_person_notfound
                                ct_person_notfound += 1
                                if person.find(namespace + 'affiliation') != None:
                                    
                                    full_party_name = list()
                                    for aff in person.findall(namespace + 'affiliation'):
                                        
                                        if aff.attrib['role'] == 'member':
                                            
                                            try:
                                                ref_string = aff.attrib['ref']
                                                ref_string = ref_string.replace('#', '')
                                                full_party_name.append(party_tag_dict[ref_string])
                                                
                                            except:
                                                full_party_name = None
                                                
                                
                                else:
                                    full_party_name = None



                            
                                write_file_noid(person,full_party_name, language_xml, namespace, nowikiid_filename, filepnowikiid)


#function to write information about a person from corpus to a file, if there is nothing found on Wikidata
#@param person: person node
#@param full_party_name: full name of party the person is affiliated with (retrieved from original corpus via code #party.Bf)
def write_file_noid(person, full_party_name, language_xml, namespace, nowikiid_filename, filepnowikiid):
    
    no_id = {}
    filepath = nowikiid_filename
    
    for tag in person.iter():

        if tag.tag == namespace + 'sex':
            
            gender_attribute = tag.attrib['value']
            gender_text = tag.text
            no_id['gender'] = gender_attribute

        elif tag.tag == namespace + 'birth':
            birth_attribute = tag.attrib['when']
            birth_text = tag.text
            no_id['birth'] = birth_attribute
            
        elif tag.tag == namespace + 'persName':
            forenames = []
            for forename in tag:
                if forename.tag == namespace + 'forename':
            
                    forenames.append(forename.text)
                    no_id['forename'] = forenames
        else:
            tag_text = tag.text
        
                
        if (tag.tag!= namespace + 'sex') and (tag.tag != namespace + 'birth') and (tag.tag != namespace + 'forename') and (tag.tag != namespace + 'persName') and (tag.tag != namespace + 'person'):
            tag_text = tag.text
            tag = str(tag.tag)
            new_tag = tag.replace(namespace, '')
            no_id[new_tag] = tag_text

    if full_party_name != None:
        no_id['affiliation'] = full_party_name
    else:
        pass
    for key, value in no_id.items():
        if isinstance(value, list):
            for val in value:
                
                filepnowikiid.write(str(key) + ',' + str(val) + ';')

        else:    
            if key != 'forename':
                
                filepnowikiid.write(str(key) + ',' + str(value) +  ';')
    
    filepnowikiid.write('\n')


#function similar to findPersoninWiki but with specification of 'political party' otherwise many 'dead'/empty pages
#are turning up, instead of the populated ones
def findPartyinWiki(partyName, country_id):
    country_code = country_dict[country_id]
    #search for party with country
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    partyQuery = str()
    partyQuery = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    partyQuery = partyQuery + "SELECT DISTINCT ?item {"
    partyQuery = partyQuery + "SERVICE wikibase:mwapi {"
    partyQuery = partyQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
    partyQuery = partyQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
    partyQuery = partyQuery + "bd:serviceParam wikibase:limit 10 ."
    partyQuery = partyQuery + "bd:serviceParam mwapi:search '''" + partyName + "'''."
    partyQuery = partyQuery + "bd:serviceParam mwapi:language 'en'."
    partyQuery = partyQuery + "?item wikibase:apiOutputItem mwapi:item."
    partyQuery = partyQuery + "?num wikibase:apiOrdinal true."
    partyQuery = partyQuery + "}"
    partyQuery = partyQuery + "?item (wdt:P279|wdt:P31) wd:Q7278. "
    partyQuery = partyQuery + "?item  wdt:P17 ?country. "
    partyQuery = partyQuery + "?country rdfs:label ?label. "
    partyQuery = partyQuery + "FILTER(LANG(?label) = 'en'). "
    partyQuery = partyQuery + "FILTER(CONTAINS(?label, '''"+ country_code +"''')). "
    partyQuery = partyQuery + "}"
    partyQuery = partyQuery + "ORDER BY ?searchTerm ?num "
    
    sparql.setQuery(partyQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    resultsstr = str()
    #check to see if json is empty (i.e if the sparql query returned a result or not)
    try:
        resultsstr = results_df[['item.value']].to_string(index=False, header=False)
        #find index of last slash in return uri
        #because that is where identifier is placed in return uri
        indexslash = int()
        indexslash = resultsstr.rfind('/')
    
        #save wikidata identifier of person 
        partywikiidentifier = str()
        #access everything after index of last slash found in uri
        partywikiidentifier = resultsstr[indexslash + 1: ]
        global ct_org_query1
        ct_org_query1 += 1
        return str(partywikiidentifier)

    #search for political organisation with country code filter
    except:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        partyQuery = str()
        partyQuery = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        partyQuery = partyQuery + "SELECT DISTINCT ?item {"
        partyQuery = partyQuery + "SERVICE wikibase:mwapi {"
        partyQuery = partyQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
        partyQuery = partyQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
        partyQuery = partyQuery + "bd:serviceParam wikibase:limit 10 ."
        partyQuery = partyQuery + "bd:serviceParam mwapi:search '''" + partyName + "'''."
        partyQuery = partyQuery + "bd:serviceParam mwapi:language 'en'."
        partyQuery = partyQuery + "?item wikibase:apiOutputItem mwapi:item."
        partyQuery = partyQuery + "?num wikibase:apiOrdinal true."
        partyQuery = partyQuery + "}"
        partyQuery = partyQuery + "?item (wdt:P279|wdt:P31) wd:Q7210356. "
        partyQuery = partyQuery + "?item  wdt:P17 ?country. "
        partyQuery = partyQuery + "?country rdfs:label ?label. "
        partyQuery = partyQuery + "FILTER(LANG(?label) = 'en'). "
        partyQuery = partyQuery + "FILTER(CONTAINS(?label, '''"+ country_code +"''')). "
        partyQuery = partyQuery + "}"
        partyQuery = partyQuery + "ORDER BY ?searchTerm ?num "
        
        sparql.setQuery(partyQuery)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        resultsstr = str()
        #check to see if json is empty (i.e if the sparql query returned a result or not)
        try:
            resultsstr = results_df[['item.value']].to_string(index=False, header=False)
            #find index of last slash in return uri
            #because that is where identifier is placed in return uri
            indexslash = int()
            indexslash = resultsstr.rfind('/')
        
            #save wikidata identifier of person 
            partywikiidentifier = str()
            #access everything after index of last slash found in uri
            partywikiidentifier = resultsstr[indexslash + 1: ]
            global ct_org_query2
            ct_org_query2 += 1
            return str(partywikiidentifier)
        
    
        except:
            #search for political party
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
            partyQuery = str()
            partyQuery = "SELECT DISTINCT ?item {"
            partyQuery = partyQuery + "SERVICE wikibase:mwapi {"
            partyQuery = partyQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
            partyQuery = partyQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
            partyQuery = partyQuery + "bd:serviceParam wikibase:limit 1 ."
            partyQuery = partyQuery + "bd:serviceParam mwapi:search '''" + partyName + "'''."
            partyQuery = partyQuery + "bd:serviceParam mwapi:language 'en'."
            partyQuery = partyQuery + "?item wikibase:apiOutputItem mwapi:item."
            partyQuery = partyQuery + "?num wikibase:apiOrdinal true."
            partyQuery = partyQuery + "}"
            partyQuery = partyQuery + "?item (wdt:P279|wdt:P31) wd:Q7278"
            partyQuery = partyQuery + "}"
            partyQuery = partyQuery + "ORDER BY ?searchTerm ?num "

            sparql.setQuery(partyQuery)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            results_df = pd.json_normalize(results['results']['bindings'])
            resultsstr = str()

            #check to see if json is empty (i.e if the sparql query returned a result or not)
            try:
                resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                #find index of last slash in return uri
                #because that is where identifier is placed in return uri
                indexslash = int()
                indexslash = resultsstr.rfind('/')
            
                #save wikidata identifier of person 
                partywikiidentifier = str()
                #access everything after index of last slash found in uri
                partywikiidentifier = resultsstr[indexslash + 1: ]
                global ct_org_query3
                ct_org_query3 += 1
                return str(partywikiidentifier)

            #person not found in wikidata
            
            except:
                #search for political organisation
                sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                partyQuery = str()
                partyQuery = "SELECT DISTINCT ?item {"
                partyQuery = partyQuery + "SERVICE wikibase:mwapi {"
                partyQuery = partyQuery + "bd:serviceParam wikibase:api 'EntitySearch'."
                partyQuery = partyQuery + "bd:serviceParam wikibase:endpoint 'www.wikidata.org'."
                partyQuery = partyQuery + "bd:serviceParam wikibase:limit 1 ."
                partyQuery = partyQuery + "bd:serviceParam mwapi:search '''" + partyName + "'''."
                partyQuery = partyQuery + "bd:serviceParam mwapi:language 'en'."
                partyQuery = partyQuery + "?item wikibase:apiOutputItem mwapi:item."
                partyQuery = partyQuery + "?num wikibase:apiOrdinal true."
                partyQuery = partyQuery + "}"
                partyQuery = partyQuery + "?item (wdt:P279|wdt:P31) wd:Q7210356"
                partyQuery = partyQuery + "}"
                partyQuery = partyQuery + "ORDER BY ?searchTerm ?num "

                sparql.setQuery(partyQuery)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                results_df = pd.json_normalize(results['results']['bindings'])
                resultsstr = str()

                try:
                    resultsstr = results_df[['item.value']].to_string(index=False, header=False)
                    #find index of last slash in return uri
                    #because that is where identifier is placed in return uri
                    indexslash = int()
                    indexslash = resultsstr.rfind('/')
                
                    #save wikidata identifier of person 
                    partywikiidentifier = str()
                    #access everything after index of last slash found in uri
                    partywikiidentifier = resultsstr[indexslash + 1: ]
                    global ct_org_query4
                    ct_org_query4 += 1
                    return str(partywikiidentifier)

            
                #if all queries above fail try this as last measure
                except:
                    
                    params = dict (
                                    action='wbsearchentities',
                                    format='json',
                                    language= 'en',
                                    uselang= 'en',
                                    type='item',
                                    search= partyName
                                    )

                    response = requests.get('https://www.wikidata.org/w/api.php?', params).json() 
                    

                    try:
                        
                        response_out = response.get('search')[0]['id']
                        partywikiidentifier = response_out
                        global ct_org_query5
                        ct_org_query5 += 1
                        return str(partywikiidentifier)

                    except:
                        global ct_org_notfound
                        ct_org_notfound += 1
                        print('party/group not found')

            



#function to get meta-information about a person
#using the wikidata identifier 
# @param identifier: Wikidata identifier of a person (acquired via findPersoninWiki)
# @param language_xml: language identifier (of the xml) to return metadata in (e.g. tr = turkish...)
# return metadict: dictionairy containing the meta-info from wiki
# keys are title of meta-info, value:meta-info value in lists   
def getwikimetainfo(identifier, language_xml):

    if identifier != None:
    
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        metaquery = str()
        metaquery = "SELECT ?birthLabel ?placeLabel ?deathLabel ?deathplaceLabel ?genderLabel ?educationLabel ?employLabel ?imageLabel ?twitterLabel ?facebookLabel ?instagramLabel ?websiteLabel ?viafLabel"
        metaquery = metaquery + " WHERE{"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P569   ?birth.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P19    ?place.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P570   ?death.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P20    ?deathplace.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P21    ?gender.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P69    ?education.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P106   ?employ.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P18    ?image.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P2002  ?twitter.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P2013  ?facebook.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P2003  ?instagram.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P856   ?website.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P214   ?viaf.}"
        metaquery = metaquery + " SERVICE wikibase:label{bd:serviceParam wikibase:language '" + language_xml + "' .}"
        metaquery = metaquery + " }"
        
        
        sparql.setQuery(metaquery)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        
        #second query to get content in english (en)
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        metaquery_en = str()
        metaquery_en = "SELECT ?placeLabel ?deathplaceLabel ?genderLabel ?educationLabel ?employLabel"
        metaquery_en = metaquery_en + " WHERE{"
        metaquery_en = metaquery_en + " OPTIONAL{ wd:" + identifier + " wdt:P19    ?place.}"
        metaquery_en = metaquery_en + " OPTIONAL{ wd:" + identifier + " wdt:P20    ?deathplace.}"
        metaquery_en = metaquery_en + " OPTIONAL{ wd:" + identifier + " wdt:P21    ?gender.}"
        metaquery_en = metaquery_en + " OPTIONAL{ wd:" + identifier + " wdt:P69    ?education.}"
        metaquery_en = metaquery_en + " OPTIONAL{ wd:" + identifier + " wdt:P106   ?employ.}"
        metaquery_en = metaquery_en + " SERVICE wikibase:label{bd:serviceParam wikibase:language 'en' .}"
        metaquery_en = metaquery_en + " }"


        sparql.setQuery(metaquery_en)
        sparql.setReturnFormat(JSON)
        results_en = sparql.query().convert()
        results_df_en = pd.json_normalize(results_en['results']['bindings'])


        
        #create metadict
        metadict = {}   

        #check if values are available in the metadict
        #if yes add to meta dict
        #else do nothing/pass
        metadict['wikidata'] = 'https://www.wikidata.org/wiki/' + str(identifier)
        try:
            birthplace= list()
            birthplace = results_df['placeLabel.value']
            metadict["birthplace"] = list(set(birthplace))
        except:
            pass

        try:
            birthplace_en= list()
            birthplace_en = results_df_en['placeLabel.value']
            metadict["birthplace_en"] = list(set(birthplace_en))
        except:
            pass

        try:
            birthdate = list()
            birthdate = results_df['birthLabel.value']
            metadict["birthdate"] = list(set(birthdate))
        except:
            pass
        
        try:
            deathdate = list()
            deathdate = results_df['deathLabel.value']
            metadict["deathdate"] = list(set(deathdate))
        except:
            pass

        
        try:
            deathplace = list()
            deathplace = results_df['deathplaceLabel.value']
            metadict["deathplace"] = list(set(deathplace))
        except:
            pass

        try:
            gender = list()
            gender = results_df['genderLabel.value']
            metadict["gender"] = list(set(gender))
        except:
            pass

        try:
            gender_en = list()
            gender_en = results_df_en['genderLabel.value']
            metadict["gender_en"] = list(set(gender_en))
        except:
            pass
        

        try:
            deathplace_en= list()
            deathplace_en = results_df_en['deathplaceLabel.value']
            metadict["deathplace_en"] = list(set(deathplace_en))
        except:
            pass



        try:
            occupation = list()
            occupation = results_df['employLabel.value']
            temp_list = list()
            tempstr = results_df['employLabel.value'].to_string(index=False, header=False)
            temp_list = tempstr.split('\n')
            temp_list = list(set(temp_list))
            metadict["occupation"] = temp_list
        except:
            pass

        try:
            temp_list = list()
            tempstr = results_df_en['employLabel.value'].to_string(index=False, header=False)
            temp_list = tempstr.split('\n')
            temp_list = list(set(temp_list))
            metadict["occupation_en"] = temp_list
        except:
            pass

        
        try:
            temp_list = list()
            education = list()
            return_education_list = ()
            education = results_df['educationLabel.value']
            tempstr = results_df['educationLabel.value'].to_string(index=False, header=False)
            temp_list = tempstr.split('\n')
            temp_list = list(set(temp_list))
            metadict["education"] = temp_list

        except:
            pass

        try:
            education_en = list()
            education_en = results_df_en['educationLabel.value']
            temp_list = list()
            tempstr = results_df_en['educationLabel.value'].to_string(index=False, header=False)
            temp_list = tempstr.split('\n')
            temp_list = list(set(temp_list))
            metadict["education_en"] = temp_list
        except:
            pass

        try:
            image = list()
            image = results_df['imageLabel.value']
            metadict["image"] = list(set(image))
        except:
            pass

        
        try:
            twitter = list()
            twitter = results_df['twitterLabel.value']
            metadict["twitter"] = list(set("https://twitter.com/"+ twitter))
        except:
            pass
        
        
        try:
            facebook = list()
            facebook = results_df['facebookLabel.value']
            metadict["facebook"] = list(set("https://www.facebook.com/" + facebook))
        except:
            pass

        try:
            instagram = list()
            instagram = results_df['instagramLabel.value']
            metadict["instagram"] = list(set("https://www.instagram.com/" + instagram))
        except:
            pass

        try:
            website = list()
            website = results_df['websiteLabel.value']
            metadict["website"] = list(set(website))
        except:
            pass

        try:
            viaf = list()
            viaf = results_df['viafLabel.value']
            metadict["viaf"] = list(set(viaf))
        except:
            pass
        
        
        return metadict


#function to split strings that are delivered in list (like ['politician, 'solicitor'])
#specifically to edit values of metadict
#so they can be put into different xml tags for building of xml file
#edits values -> cut off Hochkommas and square brackets
#also edits singular values coming in!
#returns a list 
#@param str_to_split: list with content to split and edit
#@return string_list: list of  edited string(s)
def my_split_string(str_to_split):
    string_list = []
    str_to_split = str(str_to_split)
    
    #remove brackets
    if '[' in str_to_split:
        str_to_split = str_to_split[1:-1]
    str_to_split = str_to_split.replace(',', '%|%')
    #check if str contains comma (if yes its multiple values in input else single)
    if "," in str_to_split:
        string_list = str_to_split.split(', ')
    #single value case
    else:
        #brackets already removed, remove Hochkomma
        str_to_split = str_to_split.replace("'", "")
        #append to return list
        str_to_split = str_to_split.replace('%|%', ',')
        string_list.append(str_to_split)
        
    

    return string_list



##############death
def handle_tag_death(person, namespace, indexgender, metainfo):
    try:
        #retrieve info on persons birthdate from metadict
        birth_str = str(metainfo['deathdate'])
        #if 'http' not in birth_str:
        #get birthdate string in required format (cut off everything after T)
        birth_str = my_split_string(birth_str)
        birthdate_list = []
        for bd in person.findall(namespace + 'death'):
            birthdate_list.append(bd)

        if len(birthdate_list) == 0:
        #if more than one birthdate available
            if len(birth_str) > 1:
                
                for bi in birth_str:
                    if 'http' not in bi:
                    #build new 'birth' element in xml
                        birth = ET.Element(namespace + 'death')
                        #get rid of T in birthdate
                        bi = bi.split('T')
                        #set date as attribute of tag 'birth'
                        birth.set('when', str(bi[0]))
                        #insert birth-element into xml at index one after sex-index
                        person.insert(indexgender  , birth)
                        #check to see if birthplace is available for person
                        try:

                            #if yes add new subelement to birth: placeName
                            if str(metainfo['deathplace']) != str(metainfo['deathplace_en']):
                                deathplace = metainfo['deathplace']
                                #if ('http' not in deathplace) and ('http' not in str(metainfo['deathplace_en'])):
                                birthplace = ET.SubElement(birth, 'placeName')
                                #retrieve birthplace from metadict
                                bplace = str(metainfo['deathplace'])
                                #remove brackets and Hochkomma ? warum nicht split string??
                                bplace = bplace[1:-1]
                                bplace = bplace[1:-1]
                                #add birthplace text
                                birthplace.text = str(bplace)

                                #birthplace element in en
                                metainfo['deathplace_en']
                                birthplace_en = ET.SubElement(birth, 'placeName')
                                #retrieve birthplace from metadict
                                bplace_en = str(metainfo['deathplace_en'])
                                #remove brackets and Hochkomma ? warum nicht split string??
                                bplace_en = bplace_en[1:-1]
                                bplace_en = bplace_en[1:-1]
                                #add birthplace text
                                birthplace_en.text = str(bplace_en)
                            
                            else:
                                metainfo['deathplace_en']
                                birthplace_en = ET.SubElement(birth, 'placeName')
                                #retrieve birthplace from metadict
                                bplace_en = str(metainfo['deathplace_en'])
                                #remove brackets and Hochkomma ? warum nicht split string??
                                bplace_en = bplace_en[1:-1]
                                bplace_en = bplace_en[1:-1]
                                #add birthplace text
                                birthplace_en.text = str(bplace_en)

                        #if not pass
                        except:
                            pass
                    #unknown value
                    else:
                        pass
            #if only one birthdate is available            
            else:
                
                #new birth element
                if 'http' not in birth_str[0]:
                    birth = ET.Element(namespace + 'death')
                    #remove T from date
                    birth_str = birth_str[0].split('T')
                    #set attribute of birth to birthdate
                    birth.set('when', str(birth_str[0]))
                    #insert birth element into xml structure
                    person.insert(indexgender  , birth)
                    #check to see if birthplace available
                    try:
                        if str(metainfo['deathplace']) != str(metainfo['deathplace_en']):
                            deathplace = metainfo['deathplace']
                            birthplace = ET.SubElement(birth,'placeName')
                            bplace = str(metainfo['deathplace'])
                            bplace = bplace[1:-1]
                            bplace = bplace[1:-1]
                            birthplace.text = str(bplace)

                            #add birthplace in en
                            metainfo['deathplace_en']
                            birthplace_en = ET.SubElement(birth,'placeName')
                            bplace_en = str(metainfo['deathplace_en'])
                            bplace_en = bplace_en[1:-1]
                            bplace_en = bplace_en[1:-1]
                            birthplace_en.text = str(bplace_en)
                        else:
                            metainfo['deathplace_en']
                            birthplace_en = ET.SubElement(birth,'placeName')
                            bplace_en = str(metainfo['deathplace_en'])
                            bplace_en = bplace_en[1:-1]
                            bplace_en = bplace_en[1:-1]
                            birthplace_en.text = str(bplace_en)
                    except:
                        pass
                #unknown value
                else:
                    pass


        if len(birthdate_list) > 0:
            
            bplace = str(metainfo['deathplace'])
            birthplace_list = []
            for birth in person.findall(namespace + 'death'):
                for bp in birth.findall(namespace + 'placeName'):
                    birthplace_list.append(bp.text)

            if (len(bplace) != 0) and (len(birthplace_list) == 0):
                if str(metainfo['deathplace']) != str(metainfo['deathplace_en']):
                    bplace = str(metainfo['deathplace'])
                    if 'http' not in bplace:
                        birthplace = ET.SubElement(birth,'placeName')
                        bplace = str(metainfo['deathplace'])
                        bplace = bplace[1:-1]
                        bplace = bplace[1:-1]
                        birthplace.text = str(bplace)

                        #add birthplace in en
                        birthplace_en = ET.SubElement(birth,'placeName')
                        bplace_en = str(metainfo['deathplace_en'])
                        bplace_en = bplace_en[1:-1]
                        bplace_en = bplace_en[1:-1]
                        birthplace_en.text = str(bplace_en)
                    else:
                        pass
                    
                else:

                    
                    bplace_en = str(metainfo['deathplace_en'])
                    if 'http' not in bplace_en:
                        birthplace_en = ET.SubElement(birth,'placeName')
                        bplace_en = bplace_en[1:-1]
                        bplace_en = bplace_en[1:-1]
                        birthplace_en.text = str(bplace_en)
                    else:
                        pass


    except:
        pass



#################################


def handle_tag_birth(person, namespace, indexgender, metainfo):
    try:
        #retrieve info on persons birthdate from metadict
        birth_str = str(metainfo['birthdate'])
        #if 'http' not in birth_str:
        #get birthdate string in required format (cut off everything after T)
        birth_str = my_split_string(birth_str)
        birthdate_list = []
        for bd in person.findall(namespace + 'birth'):
            birthdate_list.append(bd)
        if len(birthdate_list) == 0:
        #if more than one birthdate available
            if len(birth_str) > 1:
                
                for bi in birth_str:
                    #build new 'birth' element in xml
                    birth = ET.Element(namespace + 'birth')
                    #get rid of T in birthdate
                    
                    if 'http' not in birth_str[0]:
                        bi = bi.split('T')
                    #set date as attribute of tag 'birth'
                        birth.set('when', str(bi[0]))
                    #insert birth-element into xml at index one after sex-index
                        person.insert(indexgender  , birth)
                    #check to see if birthplace is available for person
                        try:
                            #if yes add new subelement to birth: placeName
                            if str(metainfo['birthplace']) != str(metainfo['birthplace_en']):
                                metainfo['birthplace']
                                birthplace = ET.SubElement(birth, 'placeName')
                                #retrieve birthplace from metadict
                                bplace = str(metainfo['birthplace'])
                                #remove brackets and Hochkomma ? warum nicht split string??
                                bplace = bplace[1:-1]
                                bplace = bplace[1:-1]
                                #add birthplace text
                                birthplace.text = str(bplace)

                                #birthplace element in en
                                if 'http' not in metainfo['birthplace_en']:
                                    birthplace_en = ET.SubElement(birth, 'placeName')
                                    #retrieve birthplace from metadict
                                    bplace_en = str(metainfo['birthplace_en'])
                                    #remove brackets and Hochkomma ? warum nicht split string??
                                    bplace_en = bplace_en[1:-1]
                                    bplace_en = bplace_en[1:-1]
                                    #add birthplace text
                                    birthplace_en.text = str(bplace_en)
                                else:
                                    pass
                            
                            else:
                                if 'http' not in metainfo['birthplace_en']:
                                    birthplace_en = ET.SubElement(birth, 'placeName')
                                    #retrieve birthplace from metadict
                                    bplace_en = str(metainfo['birthplace_en'])
                                    #remove brackets and Hochkomma ? warum nicht split string??
                                    bplace_en = bplace_en[1:-1]
                                    bplace_en = bplace_en[1:-1]
                                    #add birthplace text
                                    birthplace_en.text = str(bplace_en)
                                else:
                                    pass

                        #if not pass
                        except:
                            pass
                    #else when birthdate has unknown wiki value (link)
                    else:
                        pass
            #if only one birthdate is available            
            else:
                #new birth element
                
                #remove T from date
                
                if 'http' not in birth_str[0]:
                    birth = ET.Element(namespace + 'birth')
                    birth_str = birth_str[0].split('T')
                    #set attribute of birth to birthdate
                    birth.set('when', str(birth_str[0]))
                    #insert birth element into xml structure
                    person.insert(indexgender  , birth)
                    #check to see if birthplace available
                    try:
                        if str(metainfo['birthplace']) != str(metainfo['birthplace_en']):
                            if 'http' not in metainfo['birthplace']:
                                birthplace = ET.SubElement(birth,'placeName')
                                bplace = str(metainfo['birthplace'])
                                bplace = bplace[1:-1]
                                bplace = bplace[1:-1]
                                birthplace.text = str(bplace)

                            #add birthplace in en
                            if 'http' not in metainfo['birthplace_en']:
                                birthplace_en = ET.SubElement(birth,'placeName')
                                bplace_en = str(metainfo['birthplace_en'])
                                bplace_en = bplace_en[1:-1]
                                bplace_en = bplace_en[1:-1]
                                birthplace_en.text = str(bplace_en)
                        else:
                            if 'http' not in metainfo['birthplace_en']:
                                birthplace_en = ET.SubElement(birth,'placeName')
                                bplace_en = str(metainfo['birthplace_en'])
                                bplace_en = bplace_en[1:-1]
                                bplace_en = bplace_en[1:-1]
                                birthplace_en.text = str(bplace_en)
                    except:
                        pass
                #unknown value 
                else:
                    pass


        if len(birthdate_list) > 0:
            
            bplace = str(metainfo['birthplace'])
            bplace_en = str(metainfo['birthplace_en'])
            birthplace_list = []

            for birth in person.findall(namespace + 'birth'):
                for bp in birth.findall(namespace + 'placeName'):
                    birthplace_list.append(bp.text)

            if (len(bplace) != 0) and (len(birthplace_list) == 0):
                if str(metainfo['birthplace']) != str(metainfo['birthplace_en']):
                    if 'http' not in bplace:
                        birthplace = ET.SubElement(birth,'placeName')
                        bplace = str(metainfo['birthplace'])
                        bplace = bplace[1:-1]
                        bplace = bplace[1:-1]
                        birthplace.text = str(bplace)

                    #add birthplace in en
                    if 'http' not in bplace_en:
                        birthplace_en = ET.SubElement(birth,'placeName')
                        bplace_en = str(metainfo['birthplace_en'])
                        bplace_en = bplace_en[1:-1]
                        bplace_en = bplace_en[1:-1]
                        birthplace_en.text = str(bplace_en)
                    
                else:
                    if 'http' not in bplace_en:
                        birthplace_en = ET.SubElement(birth,'placeName')
                        bplace_en = str(metainfo['birthplace_en'])
                        bplace_en = bplace_en[1:-1]
                        bplace_en = bplace_en[1:-1]
                        birthplace_en.text = str(bplace_en)


    except:
        pass

#function to check if a returned value from wikidata is a Q identifier instead of a label value e.g. Q1234
#this is then removed and not added to final xml structure
def regex_for_qid(string):
    return re.search('^Q\d', string)



def handle_tag_occupation(person, namespace,  current_index, metainfo, language_xml):
    try:
        countoccupation = list()
        for occup in person.findall(namespace + 'occupation'):
            countoccupation.append(occup)
        addtooccindex = len(countoccupation)
        #get value(s) for occupation and format
        occ_from_dict_before = metainfo['occupation']
        occ_from_dict_en_before = metainfo['occupation_en']
        occupationMatch = False
        
        occ_from_dict = list()
        occ_from_dict_en = list()
        
        for item in occ_from_dict_before:
            stripped_item = item.strip()
            stripped_item = stripped_item.replace('"', '')
            occ_from_dict.append(stripped_item)
        
        for item in occ_from_dict_en_before:
            stripped_item = item.strip()
            stripped_item = stripped_item.replace('"', '')
            occ_from_dict_en.append(stripped_item)
        
            
        for occ in occ_from_dict:
            if regex_for_qid(occ) == None:
                occ = occ.replace("'", "")
                countoccelement = list()
                for occup in person.findall(namespace + 'occupation'):
                    countoccelement.append(occup.text)
                for coccu in countoccelement:
                    if str(occ) == coccu:
                        occupationMatch = True

                if occupationMatch == False: 
                    if regex_for_qid(occ) == None:
                        #add occupation element
                        occupation = ET.Element(namespace + 'occupation')
                        occupation.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)
                        #set text to item 
                        occupation.text = str(occ)
                        #add at index
                        person.insert( current_index + addtooccindex , occupation)
                occupationMatch = False


        for occ_en in occ_from_dict_en:
            if regex_for_qid(occ_en) == None:
                countoccelement = list()
                for occup in person.findall(namespace + 'occupation'):
                    countoccelement.append(occup.text)
                for coccu in countoccelement:
                    if str(occ_en) == coccu:
                        occupationMatch = True

                if occupationMatch == False: 
                    #add occupation element
                    occupation_en = ET.Element(namespace + 'occupation')
                    occupation_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    #set text to item 
                    occupation_en.text = str(occ_en)
                    #add at index
                    person.insert(current_index + addtooccindex , occupation_en)
                occupationMatch = False
         

    except:
        pass


def handle_tag_education(person, namespace, current_index, metainfo, language_xml):
    try:
        #get education content from meta dict and format it 
        edu_from_dict_before = metainfo['education']
        edu_from_dict_en_before = metainfo['education_en']
        educationMatch = False
        edu_from_dict = list()
        edu_from_dict_en = list()
        
        for item in edu_from_dict_before:
            stripped_item = item.strip()
            stripped_item = stripped_item.replace('"', '')
            edu_from_dict.append(stripped_item)
        
        for item in edu_from_dict_en_before:
            stripped_item = item.strip()
            stripped_item = stripped_item.replace('"', '')
            edu_from_dict_en.append(stripped_item)


        #if more than one value for education
        if len(edu_from_dict) > 1:
            for edu in edu_from_dict:
                if regex_for_qid(edu) == None:
                    counteduelement = list()
                    for educ in person.findall(namespace + 'education'):
                        counteduelement.append(educ.text)
                    for cedu in counteduelement:
                        if str(edu) == cedu:
                            educationMatch = True
                    if educationMatch == False: 
                        #add new education element 
                        education = ET.Element(namespace + 'education')
                        education.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml )
                        #set text content of tag
                        education.text = str(edu)
                        person.insert(current_index, education)
                    educationMatch = False

            for edu_en in edu_from_dict_en:
                if regex_for_qid(edu_en) == None:
                    counteduelement = list()
                    for educ_en in person.findall(namespace + 'education'):
                        counteduelement.append(educ_en.text)
                    for cedu in counteduelement:
                        if str(edu_en) == cedu:
                            educationMatch = True
                    if educationMatch == False: 
                        #add new education element 
                        education_en = ET.Element(namespace + 'education')
                        #set text content of tag
                        education_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                        education_en.text = str(edu_en)
                        person.insert(current_index, education_en)
                    educationMatch = False
        #if only one education value in metadict
        else:
            if str(metainfo['education']) != str(metainfo['education_en']):
                counteduelement = list()
                for educ in person.findall(namespace + 'education'):  
                    counteduelement.append(educ.text)
                for cedu in counteduelement:
                    if str(edu_from_dict[0]) == cedu:
                        educationMatch = True   
                    #new education element
                edu_txt = str(edu_from_dict[0])
                    
                if regex_for_qid(edu_txt) == None:
                    edu_txt = edu_txt
                        
                else:
                    edu_txt = ""
                    pass



                education = ET.Element(namespace + 'education')
                education.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)
                #set text
                if edu_txt != "":
                    education.text = str(edu_txt)
                #insert
                    person.insert(current_index, education)


                edu_en_txt =  str(edu_from_dict_en[0])
                    
                if regex_for_qid(edu_en_txt) == None:
                        edu_en_txt = edu_en_txt
                        
                else:
                    edu_en_txt = ""
                    pass


                education_en = ET.Element(namespace + 'education')
                education_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                #set text
                if edu_en_txt != "":
                    education_en.text = str(edu_en_txt)
                #insert
                    person.insert(current_index, education_en)

                #empty for next person in iteration above 
                educationMatch = False
            
            #edu and edu_en are the same, then only add english version as tag, else duplicates
            else:
                counteduelement = list()
                for educ in person.findall(namespace + 'education'):  
                    counteduelement.append(educ.text)
                for cedu in counteduelement:
                    if str(edu_from_dict[0]) == cedu:
                        educationMatch = True  
                    #new education element
                edu_txt = str(edu_from_dict[0])
                    
                if regex_for_qid(edu_txt) == None:
                        edu_txt = edu_txt
                        
                else:
                    edu_txt = ""
                    pass



                education = ET.Element(namespace + 'education')
                education.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)
                #set text
                if edu_txt != "":
                    edu_txt = edu_txt.replace('"', '')
                    education.text = str(edu_txt)
                #insert
                    person.insert(current_index, education)

    except:
        pass

def handle_tag_gender(person, namespace, current_index, metainfo, language_xml, missing_gender_dict):
    try:    
        gender_from_dict_en = my_split_string(str(metainfo['gender_en']))
        gender_from_dict = my_split_string(str(metainfo['gender']))
        if len(missing_gender_dict) != 0:
            if gender_from_dict_en[0] == 'male':
                gender = ET.Element(namespace + 'sex')
                gender.set('value', 'M')
                try: 
                    male_txt = missing_gender_dict['M']
                    gender.text = male_txt
                except:
                    pass
                person.insert(current_index, gender)



            if gender_from_dict_en[0] == 'female':
                gender = ET.Element(namespace + 'sex')
                gender.set('value', 'F')
                try: 
                    female_txt = missing_gender_dict['F']
                    gender.text = female_txt
                except:
                    pass
                person.insert(current_index, gender)

            

            if (gender_from_dict_en[0] != 'female') and (gender_from_dict_en[0] != 'male'):
                gender = ET.Element(namespace + 'sex')
                gender.set('value', 'U')
                person.insert(current_index, gender)

    
    except:
        pass



def handle_tag_idno(person, namespace, current_index, metainfo , language_xml):
    try:    
        twitter_from_dict = my_split_string(str(metainfo['twitter']))
        twitterMatch = False
        if len(twitter_from_dict) > 1:
            for twitter in twitter_from_dict:
                add_dict = count_new_index(namespace, person)
                if add_dict['idno'] == 0:

                    #twitter
                    twitterelement = ET.Element(namespace +'idno')
                    twitterelement.set('type', 'URI')
                    twitterelement.set('subtype', 'twitter')
                    twitterelement.text = str(twitter)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['death'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, twitterelement)

                #one or more idno already exist
                else:
                #twitter
                    countidnoelement = list()
                    for indo in person.findall(namespace + 'idno'):
                        if indo.attrib['subtype']=="twitter":
                            countidnoelement.append(indo.text)
                    for cidno in countidnoelement:
                        if str(twitter) == cidno:
                            twitterMatch = True
                    if twitterMatch == False:   
                        twitterelement = ET.Element(namespace + 'idno')
                        twitterelement.set('type', 'URI')
                        twitterelement.set('subtype', 'twitter')
                        
                        twitterelement.text = str(twitter)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['death'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, twitterelement)

            else:
                pass
    
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
            #twitter
                twitterelement = ET.Element(namespace +'idno')
                twitterelement.set('type', 'URI')
                twitterelement.set('subtype', 'twitter')              
                twitterelement.text = str(twitter_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['death'] + add_dict['affiliation'] + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, twitterelement)
            #one or more idno already exist
            else:
                #twitter
                countidnoelement = list()
                for indo in person.findall(namespace + 'idno'):
                    if indo.attrib['subtype']=="twitter":
                        countidnoelement.append(indo.text)

                for cidno in countidnoelement:
                     if str(twitter_from_dict[0]) == cidno:
                        twitterMatch = True
 
                if twitterMatch == False:   
                    twitterelement = ET.Element(namespace + 'idno')
                    twitterelement.set('type', 'URI')
                    twitterelement.set('subtype', 'twitter')                    
                    twitterelement.text = str(twitter_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['death'] + add_dict['affiliation'] + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, twitterelement)
                twitterMatch = False

    except:
        pass


    #get metainfo from dict/check if available
    #facebook
    try:
        facebook_from_dict = my_split_string(str(metainfo['facebook']))
        facebookMatch = False
        if len(facebook_from_dict) > 1:
            for facebook in facebook_from_dict:
                add_dict =count_new_index(namespace, person)
                #no idno yet in xml
                if add_dict['idno'] == 0:
                    facebookelement = ET.Element(namespace +'idno')
                    facebookelement.set('type', 'URI')
                    facebookelement.set('subtype', 'facebook')                    
                    facebookelement.text = str(facebook)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, facebookelement)

                #one or more idno already exist
                else:
                    
                #check for facebook duplicate already existing in xml
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype']=="facebook":
                            countidnoelement.append(idno.text)

                    for cidno in countidnoelement:
                        if str(facebook) == cidno:
                            facebookMatch = True
                    if facebookMatch == False:
                        facebookelement = ET.Element(namespace + 'idno')
                        facebookelement.set('type', 'URI')
                        facebookelement.set('subtype', 'facebook')                        
                        facebookelement.text = str(facebook)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, facebookelement)
                    facebookMatch = False
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                facebookelement = ET.Element(namespace +'idno')
                facebookelement.set('type', 'URI')
                facebookelement.set('subtype', 'facebook')                
                facebookelement.text = str(facebook_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, facebookelement)

                #one or more idno already exist
            else:
                 #check for facebook duplicate already existing in xml
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype']=="facebook":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(facebook) == cidno:
                        facebookMatch = True
                if facebookMatch == False:
                    facebookelement = ET.Element(namespace + 'idno')
                    facebookelement.set('type', 'URI')
                    facebookelement.set('subtype', 'facebook')
                    
                    facebookelement.text = str(facebook_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, facebookelement)
                facebookMatch = False

    except:
        pass
    
    
    #get metainfo from dict/check if available
    #instagram
    try:
        instagram_from_dict = my_split_string(str(metainfo['instagram']))
        instagramMatch = False

        if len(instagram_from_dict) > 1:
            for instagram in instagram_from_dict:
                #no idno yet in xml
                add_dict = count_new_index(namespace, person)
                if add_dict['idno'] == 0:

                    instagramelement = ET.Element(namespace +'idno')
                    instagramelement.set('type', 'URI')
                    instagramelement.set('subtype', 'instagram')                   
                    instagramelement.text = str(instagram)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, instagramelement)

                    #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype']== "instagram":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(instagram) == cidno:
                            instagramMatch = True
                    if instagramMatch == False:
                        instagramelement = ET.Element(namespace + 'idno')
                        instagramelement.set('type', 'URI')
                        instagramelement.set('subtype', 'instagram')                        
                        instagramelement.text = str(instagram)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, instagramelement)
                    instagramMatch = False
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                instagramelement = ET.Element(namespace +'idno')
                instagramelement.set('type', 'URI')
                instagramelement.set('subtype', 'instagram')               
                instagramelement.text = str(instagram_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation'] + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, instagramelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype']== "instagram":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(instagram_from_dict[0]) == cidno:
                        instagramMatch = True
                if instagramMatch == False:
                    instagramelement = ET.Element(namespace + 'idno')
                    instagramelement.set('type', 'URI')
                    instagramelement.set('subtype', 'instagram')                   
                    instagramelement.text = str(instagram_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, instagramelement)
                instagramMatch = False


    except:
        pass
    
    
    #get metainfo from dict/check if available
    #personal website
    try:
        website_from_dict = my_split_string(str(metainfo['website']))
        websiteMatch = False
        if len(website_from_dict) > 1:
            for website in website_from_dict:
                #no idno yet in xml
                add_dict = count_new_index(namespace, person)
                if add_dict['idno'] == 0:
                    websiteelement = ET.Element(namespace +'idno')
                    websiteelement.set('type', 'URI')
                    websiteelement.set('subtype', 'personal')                   
                    websiteelement.text = str(website)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, websiteelement)

                #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype'] == "personal":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(website) == cidno:
                            websiteMatch = True
                    if websiteMatch == False:
                        websiteelement = ET.Element(namespace + 'idno')
                        websiteelement.set('type', 'URI')
                        websiteelement.set('subtype', 'personal')                       
                        websiteelement.text = str(website)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, websiteelement)
                    websiteMatch = False


        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                websiteelement = ET.Element(namespace +'idno')
                websiteelement.set('type', 'URI')
                websiteelement.set('subtype', 'personal')                
                websiteelement.text = str(website_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, websiteelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype'] == "personal":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(website_from_dict[0]) == cidno:
                        websiteMatch = True
                if websiteMatch == False:
                    websiteelement = ET.Element(namespace + 'idno')
                    websiteelement.set('type', 'URI')
                    websiteelement.set('subtype', 'personal')                   
                    websiteelement.text = str(website_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, websiteelement)
                websiteMatch = False
    except:
        pass

    #wikidata link for person
    try:
        wikidata_from_dict = my_split_string(str(metainfo['wikidata']))
        wikidataMatch = False

        if len(wikidata_from_dict) > 1:
            for wikidata in wikidata_from_dict:
                add_dict = count_new_index(namespace, person)
                #no idno yet in xml
                if add_dict['idno'] == 0:
                    wikidataelement = ET.Element(namespace +'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikidata')                    
                    wikidataelement.text = str(wikidata)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)

                    #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype']== "wikidata":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(wikidata) == cidno:
                            wikidataMatch = True
                    if wikidataMatch == False:
                        wikidataelement = ET.Element(namespace + 'idno')
                        wikidataelement.set('type', 'URI')
                        wikidataelement.set('subtype', 'wikidata')                        
                        wikidataelement.text = str(wikidata)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, wikidataelement)
                    wikidataMatch = False
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:

                wikidataelement = ET.Element(namespace +'idno')
                wikidataelement.set('type', 'URI')
                wikidataelement.set('subtype', 'wikidata')               
                wikidataelement.text = str(wikidata_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, wikidataelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype']== "wikidata":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(wikidata_from_dict[0]) == cidno:
                        wikidataMatch = True
                if wikidataMatch == False:
                    wikidataelement = ET.Element(namespace + 'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikidata')                   
                    wikidataelement.text = str(wikidata_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)
                wikidataMatch = False


    except:
        pass



    #wikipedia language_xml
    try:
        wikipedia_from_dict = my_split_string(str(metainfo['wiki']))
        wikidataMatch = False

        if len(wikipedia_from_dict) > 1:
            for wikidata in wikipedia_from_dict:
                add_dict = count_new_index(namespace, person)
                #no idno yet in xml
                if add_dict['idno'] == 0:
                    wikidataelement = ET.Element(namespace +'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikimedia')
                    wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)                   
                    wikidataelement.text = str(wikidata)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)

                    #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype']== "wikimedia":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(wikidata) == cidno:
                            wikidataMatch = True
                    if wikidataMatch == False:
                        wikidataelement = ET.Element(namespace + 'idno')
                        wikidataelement.set('type', 'URI')
                        wikidataelement.set('subtype', 'wikimedia')
                        wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)                       
                        wikidataelement.text = str(wikidata)                       
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, wikidataelement)
                    wikidataMatch = False
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                wikidataelement = ET.Element(namespace +'idno')
                wikidataelement.set('type', 'URI')
                wikidataelement.set('subtype', 'wikimedia')
                wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)                
                wikidataelement.text = str(wikipedia_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, wikidataelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype']== "wikimedia":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(wikipedia_from_dict[0]) == cidno:
                        wikidataMatch = True
                if wikidataMatch == False:
                    wikidataelement = ET.Element(namespace + 'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikimedia')
                    wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)                    
                    wikidataelement.text = str(wikipedia_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)
                wikidataMatch = False


    except:
        pass

    #wikipedia link in en
    try:
        wikipedia_from_dict = my_split_string(str(metainfo['wiki_en']))
        wikidataMatch = False

        if len(wikipedia_from_dict) > 1:
            for wikidata in wikipedia_from_dict:
                add_dict = count_new_index(namespace, person)
                #no idno yet in xml
                if add_dict['idno'] == 0:
                    wikidataelement = ET.Element(namespace +'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikimedia')
                    wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    wikidataelement.text = str(wikidata)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)

                    #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['subtype']== "wikimedia":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(wikidata) == cidno:
                            wikidataMatch = True
                    if wikidataMatch == False:
                        wikidataelement = ET.Element(namespace + 'idno')
                        wikidataelement.set('type', 'URI')
                        wikidataelement.set('subtype', 'wikimedia')
                        wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                        wikidataelement.text = str(wikidata)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, wikidataelement)
                    wikidataMatch = False
        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                wikidataelement = ET.Element(namespace +'idno')
                wikidataelement.set('type', 'URI')
                wikidataelement.set('subtype', 'wikimedia')
                wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                wikidataelement.text = str(wikipedia_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, wikidataelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['subtype']== "wikimedia":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(wikipedia_from_dict[0]) == cidno:
                        wikidataMatch = True
                if wikidataMatch == False:
                    wikidataelement = ET.Element(namespace + 'idno')
                    wikidataelement.set('type', 'URI')
                    wikidataelement.set('subtype', 'wikimedia')
                    wikidataelement.set('{http://www.w3.org/XML/1998/namespace}lang', 'en') 
                    wikidataelement.text = str(wikipedia_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex'] + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, wikidataelement)
                wikidataMatch = False


    except:
        pass



    #viaf id/link
    try:
        viaf_from_dict = my_split_string(str(metainfo['viaf']))
        websiteMatch = False
        if len(viaf_from_dict) > 1:
            for website in viaf_from_dict:
                #no idno yet in xml
                add_dict = count_new_index(namespace, person)
                if add_dict['idno'] == 0:
                    websiteelement = ET.Element(namespace +'idno')
                    websiteelement.set('type', 'VIAF')
                    websiteelement.text = str(website)
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, websiteelement)

                #one or more idno already exist
                else:
                    countidnoelement = list()
                    for idno in person.findall(namespace + 'idno'):
                        if idno.attrib['type'] == "VIAF":
                            countidnoelement.append(idno.text)
                    for cidno in countidnoelement:
                        if str(website) == cidno:
                            websiteMatch = True
                    if websiteMatch == False:
                        websiteelement = ET.Element(namespace + 'idno')
                        websiteelement.set('type', 'VIAF')
                        websiteelement.text = str(website)
                        current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                        person.insert(current_index, websiteelement)
                    websiteMatch = False


        else:
            add_dict = count_new_index(namespace, person)
            if add_dict['idno'] == 0:
                websiteelement = ET.Element(namespace +'idno')
                websiteelement.set('type', 'VIAF')
                websiteelement.text = str(viaf_from_dict[0])
                current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                person.insert(current_index, websiteelement)

            #one or more idno already exist
            else:
                countidnoelement = list()
                for idno in person.findall(namespace + 'idno'):
                    if idno.attrib['type'] == "VIAF":
                        countidnoelement.append(idno.text)
                for cidno in countidnoelement:
                    if str(viaf_from_dict[0]) == cidno:
                        websiteMatch = True
                if websiteMatch == False:
                    websiteelement = ET.Element(namespace + 'idno')
                    websiteelement.set('type', 'VIAF')
                    websiteelement.text = str(viaf_from_dict[0])
                    current_index = add_dict['persName'] + add_dict['sex']  + add_dict['birth'] + add_dict['affiliation']  + add_dict['occupation'] + add_dict['education'] + add_dict['idno']
                    person.insert(current_index, websiteelement)
                websiteMatch = False
    except:
        pass


def handle_tag_figure(person, namespace, current_index, metainfo):
    
    try:
        image_from_dict = my_split_string(str(metainfo['image']))
        wd_figure_found = True
    except:
        wd_figure_found = False


    try:
        imageMatch = False
        image_from_dict = my_split_string(str(metainfo['image']))
        image_from_dict = list(set(image_from_dict))
        image_from_dict = str(urllib.parse.unquote(image_from_dict[0]))
        image_from_dict = image_from_dict.replace(" ", "_")
        figure = person.find(namespace + 'figure')
        figure.find(namespace + 'graphic')
        figurefound = True
        countfigureelement = list()
        for fig in figure.findall(namespace + 'graphic'):
            countfigureelement.append(fig.attrib['url'])
        countfigureelement = list(set(countfigureelement))
        
    except:
        figurefound = False
    #check if there is existing figure element
    #try:
    if figurefound == True:
        for fig in countfigureelement:
            if fig != image_from_dict:
                figure = ET.Element(namespace + 'figure')
                graphic = ET.SubElement(figure, 'graphic')
                graphic.set('url', image_from_dict)
                person.insert(current_index, figure)


    else:
        if wd_figure_found == True:    
            if image_from_dict is list:
                if len(image_from_dict) > 1:
                    figure = ET.Element(namespace + 'figure')
                    person.insert(current_index, figure)
                    for img in image_from_dict:
                        graphic = ET.SubElement(figure, 'graphic')
                        graphic.set('url', img )

            else:
                figure = ET.Element(namespace + 'figure')
                graphic = ET.SubElement(figure, 'graphic')
                graphic.set('url', image_from_dict)
                person.insert(current_index, figure)


def person_wikipedia_en(pers_id,metainfo, language_xml='en'):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + pers_id + " wdt:P31 wd:Q5 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + pers_id + ". "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:inLanguage '" + language_xml + "' ."
        party_wikipedia_query = party_wikipedia_query + " ?link schema:isPartOf <https://"+ language_xml  +".wikipedia.org/> ."
        party_wikipedia_query = party_wikipedia_query + " } "
        party_wikipedia_query = party_wikipedia_query + " } "

        sparql.setQuery(party_wikipedia_query)
        sparql.setReturnFormat(JSON)
        results_party_wikipedia = sparql.query().convert()
        results_df_party_wikipedia = pd.json_normalize(results_party_wikipedia['results']['bindings'])
        try: 
            value_wikipedia = results_df_party_wikipedia["link.value"][0]
            metainfo["wiki_en"] = str(urllib.parse.unquote(value_wikipedia))
        except:
            pass        
    except:
        pass


    return metainfo


def person_wikipedia(pers_id,metainfo, language_xml):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + pers_id + " wdt:P31 wd:Q5 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + pers_id + ". "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:inLanguage '" + language_xml + "' ."
        party_wikipedia_query = party_wikipedia_query + " ?link schema:isPartOf <https://"+ language_xml  +".wikipedia.org/> ."
        party_wikipedia_query = party_wikipedia_query + " } "
        party_wikipedia_query = party_wikipedia_query + " } "

        sparql.setQuery(party_wikipedia_query)
        sparql.setReturnFormat(JSON)
        results_party_wikipedia = sparql.query().convert()
        results_df_party_wikipedia = pd.json_normalize(results_party_wikipedia['results']['bindings'])
        try: 
            value_wikipedia = results_df_party_wikipedia["link.value"][0]
            metainfo["wiki"] = str(urllib.parse.unquote(value_wikipedia))
        except:
            pass        
    except:
        pass


    return metainfo

#function to retrieve alias of a person (in 'en') from Wikidata
#@param pers_id: Wikidata Q-id of the person
#@param metainfo: dictionairy all information found about a person in Wikidata is stored
#@param language_xml: language tag retrieved from xml file when reading in, used to set label language for query
#return: enriched metainfo dictionairy
def person_alias(pers_id, metainfo, language_xml='en'):
    try:
        
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        alias_query = str()
        alias_query = "SELECT DISTINCT  ?label "
        alias_query = alias_query + " WHERE { "
        alias_query = alias_query + " ?work wdt:P31? wd:" + pers_id + " . "
        alias_query = alias_query + " ?work (rdfs:label|skos:altLabel) ?label. "
        alias_query = alias_query + " FILTER(lang(?label) = 'en' ) "
        alias_query = alias_query + " } "
        
        sparql.setQuery(alias_query)
        sparql.setReturnFormat(JSON)
        results_alias = sparql.query().convert()
        results_df_alias = pd.json_normalize(results_alias['results']['bindings'])

        try: 
            #try 
            value_alias = results_df_alias["label.value"]
            alias_list = list()
            if len(value_alias) > 1:
                #iterate over alias names and append to list
                for alias in value_alias:
                    alias_list.append(alias)
                #make list unique here
                alias_list = list(set(alias_list))
                #set value 'alias' in metainfo dict to the list
                metainfo["alias"] = alias_list 
            #if no multiple values from df 
            else:
                #set 'alias' in metainfo dict
                ret_list = list()
                ret_list.append(value_alias[0])
                metainfo["alias"] = ret_list
        except:
            pass        
    except:
        pass

    return metainfo

#function to retrieve english name of a party (if available on wikidata)
def party_name_en(party_identifier):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_name_query = str()
        party_name_query = "SELECT DISTINCT ?label WHERE { "
        party_name_query = party_name_query  + " wd:" + party_identifier + " rdfs:label ?label ."
        party_name_query = party_name_query  + " FILTER (langMatches( lang(?label), 'en' ) )  "
        party_name_query = party_name_query  + " } LIMIT 1"

        sparql.setQuery(party_name_query)
        sparql.setReturnFormat(JSON)
        results_party = sparql.query().convert()
        results_df_party = pd.json_normalize(results_party['results']['bindings'])
        party_meta_dict = {}
        try:
            value_name = results_df_party["label.value"][0] #to get rid of unnecessary things (e.g object etc...)
            party_meta_dict['party_name_en'] = value_name              
        except:
            pass

        return party_meta_dict

    except:
        pass

#function to retrieve official website of the party 
#@param party_identifier: wikidata identifier of the party
#@param party_meta_dict: dictionairy to which all party meta-information is saved
#returns party_meta_dict: enriched with website link
def party_website(party_identifier, party_meta_dict):
    #website query
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_website_query = str()
        party_website_query = "SELECT  ?website "
        party_website_query = party_website_query + " WHERE { "
        party_website_query = party_website_query + " wd:" + party_identifier + " wdt:P856 ?website. "
        party_website_query = party_website_query + " }"
        
        sparql.setQuery(party_website_query)
        sparql.setReturnFormat(JSON)
        results_party_website = sparql.query().convert()
        results_df_party_website = pd.json_normalize(results_party_website['results']['bindings'])
        try: 
            value_website = results_df_party_website["website.value"][0]
            party_meta_dict["website"] = str(urllib.parse.unquote(value_website))

        except:
            pass

        return party_meta_dict
    
    except:
        pass


#get wikipedia link based on corpus language
#@param party_identifier: identifier of party in wikidata
#@param language_xml: language spceifiex in teiCorpus tag of the xml (language of the corpus)
#@party_meta_dict: dictionairy where all data is saved to (website, english name, abbr and wikipedia links)
#returns party_meta_dict: enriched with the wikipedia link
def party_wikipedia(party_identifier, language_xml, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + party_identifier + " wdt:P31 wd:Q7278 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + party_identifier + ". "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:inLanguage '" + language_xml + "' ."
        party_wikipedia_query = party_wikipedia_query + " ?link schema:isPartOf <https://"+ language_xml  +".wikipedia.org/> ."
        party_wikipedia_query = party_wikipedia_query + " } "
        party_wikipedia_query = party_wikipedia_query + " } "

        sparql.setQuery(party_wikipedia_query)
        sparql.setReturnFormat(JSON)
        results_party_wikipedia = sparql.query().convert()
        results_df_party_wikipedia = pd.json_normalize(results_party_wikipedia['results']['bindings'])
        try: 
            value_wikipedia = results_df_party_wikipedia["link.value"][0]
            party_meta_dict["wiki"] = str(urllib.parse.unquote(value_wikipedia))
        except:
            pass        

        return party_meta_dict

    except:
        pass


#get wikipedia linkin english
#@param party_identifier: identifier of party in wikidata
#@param language_xml: language spceifiex in teiCorpus tag of the xml (language of the corpus)
#@party_meta_dict: dictionairy where all data is saved to (website, english name, abbr and wikipedia links)
#returns party_meta_dict: enriched with the wikipedia link
def party_wikipedia_en(party_identifier,party_meta_dict, language_xml='en'):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + party_identifier + " wdt:P31 wd:Q7278 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + party_identifier + ". "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:inLanguage '" + language_xml + "' ."
        party_wikipedia_query = party_wikipedia_query + " ?link schema:isPartOf <https://"+ language_xml  +".wikipedia.org/> ."
        party_wikipedia_query = party_wikipedia_query + " } "
        party_wikipedia_query = party_wikipedia_query + " } "

        sparql.setQuery(party_wikipedia_query)
        sparql.setReturnFormat(JSON)
        results_party_wikipedia = sparql.query().convert()
        results_df_party_wikipedia = pd.json_normalize(results_party_wikipedia['results']['bindings'])
        try: 
            value_wikipedia = results_df_party_wikipedia["link.value"][0]
            party_meta_dict["wiki_en"] = str(urllib.parse.unquote(value_wikipedia))
        except:
            pass        
    except:
        pass

    return party_meta_dict

#function to retrieve instagram and twitter usernames for the parties
#@param party_identifier: wikidata identifier for the party
#@param party_meta_dict: dictionairy in which all the party meta-information is stored
#return party_meta_dict: enriched dictionairy
def party_twitter(party_identifier, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_socials_query = str()
        party_socials_query = "SELECT ?twitter  "
        party_socials_query = party_socials_query + " WHERE { "
        party_socials_query = party_socials_query + " wd:"+ party_identifier  + " wdt:P2002 ?twitter . "
        party_socials_query = party_socials_query + " }"
        sparql.setQuery(party_socials_query)
        sparql.setReturnFormat(JSON)
        results_party_socials = sparql.query().convert()
        results_df_party_socials= pd.json_normalize(results_party_socials['results']['bindings'])
        party_meta_dict['wikidata'] = 'http://www.wikidata.org/entity/' + party_identifier
        try: 
            value_twitter = results_df_party_socials["twitter.value"][0]
            party_meta_dict['twitter'] = 'https://twitter.com/' + value_twitter
            
        except:
            pass
               
    except:
        pass

    return party_meta_dict

#function to retrieve instagram usernames for the parties
#@param party_identifier: wikidata identifier for the party
#@param party_meta_dict: dictionairy in which all the party meta-information is stored
#return party_meta_dict: enriched dictionairy with data from WD
def party_instagram(party_identifier, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_socials_query = str()
        party_socials_query = "SELECT ?instagram  "
        party_socials_query = party_socials_query + " WHERE { "
        party_socials_query = party_socials_query + " wd:"+ party_identifier  + " wdt:P2003 ?instagram . "
        party_socials_query = party_socials_query + " }"
        sparql.setQuery(party_socials_query)
        sparql.setReturnFormat(JSON)
        results_party_socials = sparql.query().convert()
        results_df_party_socials= pd.json_normalize(results_party_socials['results']['bindings'])
        try: 
            value_instagram = results_df_party_socials["instagram.value"][0]
            party_meta_dict['instagram'] = 'https://www.instagram.com/' + value_instagram
            
        except:
            pass
                
    except:
        pass

    return party_meta_dict


# function to retrieve party inception date 
# @param: party_identifier: Q-identifier of party/group
# @param: party_meta_dict: dictionairy containing all retrieved data
# return party_meta_dict enriched with inception date of party/group
def party_event(party_identifier, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_socials_query = str()
        party_socials_query = "SELECT ?event ?dissolved "
        party_socials_query = party_socials_query + " WHERE { "
        party_socials_query = party_socials_query + "OPTIONAL{ wd:"+ party_identifier  + " wdt:P571 ?event .}"
        party_socials_query = party_socials_query + "OPTIONAL{ wd:"+ party_identifier  + " wdt:P576 ?dissolved .} "
        party_socials_query = party_socials_query + " }"
        sparql.setQuery(party_socials_query)
        sparql.setReturnFormat(JSON)
        results_party_socials = sparql.query().convert()
        results_df_party_socials= pd.json_normalize(results_party_socials['results']['bindings'])

        try: 
            value_event = results_df_party_socials["event.value"][0]
            party_meta_dict['event'] =  value_event  

        except:
            pass
           
    except:
        pass

    return party_meta_dict

# function to retrieve the dissolvement date of a party or group
# @param party_identifier: Q-id of the party/group
# @param party_meta_dict: dictionairy into which retrieved data from WD is added
# return party_meta_dict with added dissolvement data 
def party_dissolved(party_identifier, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_socials_query = str()
        party_socials_query = "SELECT ?event ?dissolved "
        party_socials_query = party_socials_query + " WHERE { "
        party_socials_query = party_socials_query + " wd:"+ party_identifier  + " wdt:P576 ?dissolved . "
        party_socials_query = party_socials_query + " }"
        sparql.setQuery(party_socials_query)
        sparql.setReturnFormat(JSON)
        results_party_socials = sparql.query().convert()
        results_df_party_socials= pd.json_normalize(results_party_socials['results']['bindings'])

        try: 
            value_dissolved = results_df_party_socials["dissolved.value"][0]
            party_meta_dict['dissolved'] =  value_dissolved 

        except:
            pass
           
    except:
        pass

    return party_meta_dict



# function to find abbreviations for party in corpus language 
# abbreviations are considered everything in P:shortname or labels that is all capital letters
# @param party_identifier: Q-id of party/group
# @param party_meta_dict: dictionairy containing all retrieved data
# @param language_xml: language code from corpus root to add to query
# return enriched party_meta_dict
def party_abbrev(party_identifier, party_meta_dict, language_xml):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_abbrev = str()
        party_abbrev = "PREFIX wd: <http://www.wikidata.org/entity/> "
        party_abbrev = party_abbrev + " PREFIX wdt: <http://www.wikidata.org/prop/direct/> "
        party_abbrev = party_abbrev + " PREFIX skos: <http://www.w3.org/2004/02/skos/core#> "
        party_abbrev = party_abbrev + " PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        party_abbrev = party_abbrev + " SELECT ?shortname WHERE { "
        party_abbrev = party_abbrev + " wd:" + party_identifier + " (wdt:P1813|skos:altLabel|rdfs:label) ?shortname ."
        party_abbrev = party_abbrev + " FILTER(lang(?shortname) = '" + language_xml + "' || lang(?shortname) = 'en') "
        party_abbrev = party_abbrev + " }"

        sparql.setQuery(party_abbrev)
        sparql.setReturnFormat(JSON)
        results_party_abb = sparql.query().convert()
        results_df_party_abb= pd.json_normalize(results_party_abb['results']['bindings'])
        abbreviation_list = []
        try:
            for item in results_df_party_abb['shortname.value']:
                if item.isupper():
                    abbreviation_list.append(item)
                    party_meta_dict['abb'] = abbreviation_list          
        except:
            pass

        return party_meta_dict

    except:
        pass

# function to keep indices up to date
# return dictionairy with new indicess
def count_new_index(namespace, person):
    count_list = []
    return_dict = {}                                                                
    search_list = ['persName', 'sex', 'birth', 'death', 'occupation', 'education', 'affiliation', 'figure', 'idno']
    for item in search_list:
        count_list = []
        for node in person.findall(namespace + item):
            count_list.append(node)
        return_dict[item] = len(count_list)
    
    return return_dict

# function to find affiliations of speakers (member of political party)
# @param person_id: Q-id of person
# @param language_xml: language code from corpus root
# @party_full_dict: dictionairy containing parties from corpus
def find_affiliation(person_id, language_xml, party_full_dict):

    politician_affiliation_list = list() #list containing all names & alias names of the party(ies) a politician is associated with
    party_id_list = list()
    
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        affiliation_query = str()
        affiliation_query = "SELECT DISTINCT ?alternative ?partyLabel  {  "
        affiliation_query = affiliation_query + " wd:" + person_id + " wdt:P102 ?party. "
        affiliation_query = affiliation_query + " OPTIONAL { ?party skos:altLabel ?alternative . } "
        affiliation_query = affiliation_query + " SERVICE wikibase:label { "
        affiliation_query = affiliation_query + " bd:serviceParam wikibase:language '" + language_xml + "' . "
        affiliation_query = affiliation_query + " } "
        affiliation_query = affiliation_query + "  } "
        
        sparql.setQuery(affiliation_query)
        sparql.setReturnFormat(JSON)
        results_affiliation = sparql.query().convert()
        results_df_affiliation= pd.json_normalize(results_affiliation['results']['bindings'])
        
        for affiliation in results_df_affiliation['partyLabel.value']:
            politician_affiliation_list.append(affiliation)

        for alt in results_df_affiliation['alternative.value']:
            politician_affiliation_list.append(alt)
        
        politician_affiliation_list = list(set(politician_affiliation_list))
        
        for aff in politician_affiliation_list:
            
            try:
                if party_full_dict[aff] != None:                    
                    party_id_list.append(str(party_full_dict[aff]))

            except:
                pass
        
    except:
        pass
    
    return party_id_list

def handle_tag_affiliation(person, namespace, current_index, party_id ):

    if len(party_id) > 1:
        for party in party_id:
            affiliation = ET.Element(namespace + 'affiliation')
            #role set to member because from Wikidata retrieved 'member of political party'
            affiliation.set('role', 'member')
            affiliation.set('ref', str(party))
            person.insert(current_index, affiliation)

    if len(party_id) == 1:
        affiliation = ET.Element(namespace + 'affiliation')
        #role set to member because from Wikidata retrieved 'member of political party'
        affiliation.set('role', 'member')
        affiliation.set('ref', str(party_id[0]))
        person.insert(current_index, affiliation)



def party_count_new_index(namespace, org):
    count_list = []
    return_dict = {}                                                                
    search_list = ['orgName', 'event', 'idno', 'desc', 'listEvent']
    for item in search_list:
        count_list = []
        for node in org.findall(namespace + item):
            count_list.append(node)
        return_dict[item] = len(count_list)
    
    return return_dict



def main():
    
    #command line arguments
    parser = argparse.ArgumentParser(description='Get file parameters.')
    parser.add_argument('--infile', type=str, nargs=1, required=True)
    parser.add_argument('--outfile', type=str, nargs=1, required=False)
    parser.add_argument('--validation', type=str, nargs=1, required=True)
    args = parser.parse_args()


    try:
        with open(args.infile[0], 'r') as fh:
            fh.close()      
    except FileNotFoundError:
        return print('file ' + str(args.infile[0]) + ' not found')

    try:
            
        with open(args.validation[0], 'r') as fh:
            fh.close()  
    except FileNotFoundError:
        return print('file ' + str(args.validation) + ' not found')
    

    try:
        args.outfile[0]

        if args.outfile[0] != None:
            try:
                with open(args.outfile[0], 'r') as fh:
                    fh.close()  
            except FileNotFoundError:
                with open(str(args.outfile[0]), 'x') as fh:
                    fh.write(' ')
                fh.close()
    except:
        pass

    tree = ET.parse(args.infile[0])

    
    root = tree.getroot()
    namespace = ""
    namespace = root.tag
    id_bracket = namespace.index('}')
    namespace = namespace[:id_bracket+1]  
    namespaceuri = namespace[1:id_bracket] 
    ET.register_namespace("", namespaceuri)
    language_xml = ""
    language_xml = root.attrib['{http://www.w3.org/XML/1998/namespace}lang']
    corpus_id = root.attrib['{http://www.w3.org/XML/1998/namespace}id']
    if '.ana' in corpus_id:
        findslash = corpus_id.index('-')
        finddot = corpus_id.index('.')
        country_id = corpus_id[findslash + 1: finddot]

    else:
        findslash = corpus_id.index('-')
        country_id = corpus_id[findslash +1:]

    party_identifier = {}
    countorgname = list()
    addtoevent = list()
    init = list()
    addtoname = list()
    addtoname = list()
    addtoidnoparty = list()
    countorgname = list()

    #dictionairy to store party xml ids (e.g. party.Bf) and the corresponding text as value
    party_tag_dict = {}

    #list containing all party names to later check for affiliation
    party_full_list = list()
    party_full_dict = {}   #name as key, id as value

    count_org = 0
    count_person = 0
    
    nowikiid_filename = str(corpus_id) + '-nowikiid_' + language_xml + '.txt'
    filepnowikiid = open(nowikiid_filename, "w", encoding="UTF-8")
    

    for org in root.iter(namespace + "org"):
        countorgname = []
        if (org.attrib["role"] == "politicalParty") or (org.attrib["role"] == "politicalGroup"):
            for orgname in org.iter(namespace + "orgName"):
                if orgname.attrib["full"] == "yes":
                    try: 
                        if (orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == language_xml) :
                            party_full_list.append(orgname.text)
                            party_full_dict[orgname.text] = org.attrib['{http://www.w3.org/XML/1998/namespace}id']
                    except:
                        party_full_list.append(orgname.text)
                        party_full_dict[orgname.text] = org.attrib['{http://www.w3.org/XML/1998/namespace}id']



    for org in root.iter(namespace + "org"):
        countorgname = []
        if (org.attrib["role"] == "politicalParty") or (org.attrib["role"] == "politicalGroup"):
            for orgname in org.iter(namespace + "orgName"):
                if orgname.attrib["full"] == "yes":
                    try: 
                        if (orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == language_xml) :
                            count_org += 1
                            print('org: ' + str(count_org) + "    " + str(orgname.text))
                            
                            #get wikidata identifier of party via name (e.g. Q1234)
                            party_identifier = findPartyinWiki(orgname.text, country_id)
                            #get english name of the party (save to dict)
                            party_meta_dict = party_name_en(party_identifier)

                            #get inception date of party
                            party_meta_dict = party_event(party_identifier, party_meta_dict)
                            party_meta_dict = party_dissolved(party_identifier, party_meta_dict)
                            #get link to official website of parts (save to dict)
                            party_meta_dict = party_website(party_identifier, party_meta_dict)
                            #gets wikipedia link in corpus language (e.g. 'tr')
                            party_meta_dict = party_wikipedia(party_identifier, language_xml, party_meta_dict)
                            #get wikipedia link in english ('en')
                            party_meta_dict = party_wikipedia_en(party_identifier, party_meta_dict)

                            party_meta_dict = party_twitter(party_identifier, party_meta_dict)
                            party_meta_dict = party_instagram(party_identifier, party_meta_dict)
                            

                            party_meta_dict = party_abbrev(party_identifier, party_meta_dict, language_xml)

                    except:
                        count_org += 1
                        print('org: ' + str(count_org) + "    " + str(orgname.text))
                        party_identifier = findPartyinWiki(orgname.text, country_id)
                        #get english name of the party (save to dict)
                        party_meta_dict = party_name_en(party_identifier)
                        #get inception date of party
                        party_meta_dict = party_event(party_identifier, party_meta_dict)
                        party_meta_dict = party_dissolved(party_identifier, party_meta_dict)
                        #get link to official website of parts (save to dict)
                        party_meta_dict = party_website(party_identifier, party_meta_dict)
                        #gets wikipedia link in corpus language (e.g. 'tr')
                        party_meta_dict = party_wikipedia(party_identifier, language_xml, party_meta_dict)
                        #get wikipedia link in english ('en')
                        party_meta_dict = party_wikipedia_en(party_identifier, party_meta_dict)

                        party_meta_dict = party_twitter(party_identifier, party_meta_dict)
                        party_meta_dict = party_instagram(party_identifier, party_meta_dict)
                        party_meta_dict = party_abbrev(party_identifier, party_meta_dict, language_xml)


                countorgname.append(orgname)

                if orgname.attrib['full'] == 'yes':
                    try: 
                        if (orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == language_xml) :
                            party_tag_dict[org.attrib['{http://www.w3.org/XML/1998/namespace}id']] = orgname.text
                    except:
                        party_tag_dict[org.attrib['{http://www.w3.org/XML/1998/namespace}id']] = orgname.text

            try:
                orgName = org.find(namespace + 'orgName')                
                indexorgname = list(org).index(orgName)
                addtoname = list()
                for name in org.findall(namespace + 'orgName'):
                    if name.attrib['full'] == 'yes':
                        addtoname.append(name.text)
            except:
                pass
                
            addtorgnameindex = len(countorgname)
                        
            try:
                name_en= party_meta_dict['party_name_en']
                if name_en not in addtoname:
                    new_idno = ET.Element(namespace + 'orgName')
                    new_idno.set('full', 'yes')
                    
                    new_idno.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    new_idno.text = name_en
                    #do not add num of all idno elements on top so wikipedia link in corpus language is always 
                    #first idno
                    org.insert(indexorgname + len(addtoname)  , new_idno)
                else:
                    pass
            except:
                pass

            #count all full orgNames again to know where to insert init abberviation
            try:
                addtoname = []
                for name in org.findall(namespace + 'orgName'):
                    if name.attrib['full'] == 'yes':
                        addtoname.append(name.text)

            except:
                pass

           
            try:
                init =[]
                for name in org.findall(namespace + 'orgName'):
                    if name.attrib['full'] == 'init':
                        init.append(name.text)

            except:
                pass

            
            try:
                abbreviation= party_meta_dict['abb']
                abbreviation = list(set(abbreviation))
                for abb in abbreviation:
                    if abb not in init:
                        
                        new_idno = ET.Element(namespace + 'orgName')
                        new_idno.set('full', 'init')
                        new_idno.text = abb
                        #do not add num of all idno elements on top so wikipedia link in corpus language is always 
                        #first idno
                        org.insert(indexorgname + len(addtoname) , new_idno)
                    else:
                        pass
            except:
                pass
                #print('Error abbreviation')



            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] 
            try:
                event_found = org.find(namespace + 'event') 
                event_found.attrib['from']
                
            except:
                try:
                    event = party_meta_dict['event']
                    if 'T' in event:
                        index_t = event.index('T')
                        event_final = event[:index_t]
                    else:
                        event_final = event
                    new_event = ET.Element(namespace + 'event')
                    new_event.set('from', event_final )

                    org.insert(party_current_index, new_event)
                    label = ET.SubElement(new_event, namespace + 'label')
                    label.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    label.text = 'existence'

                    try: 
                        dissolved = party_meta_dict['dissolved']
                        if 'T' in dissolved:
                            index_t_dissolved = dissolved.index('T')
                            dissolved_final = dissolved[:index_t_dissolved]
                        else:
                            dissolved_final = dissolved
                        new_event.set('to', dissolved_final)
                    except:
                        pass
                    
                except:
                    pass



            
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']

            #wiki link in corpus language
            try:
                wiki= party_meta_dict['wiki']
                
                if wiki not in addtoidnoparty:
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'wikimedia')
                    
                    new_idno.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)
                    new_idno.text = wiki
                    #do not add num of all idno elements on top so wikipedia link in corpus language is always 
                    #first idno
                    org.insert(party_current_index  , new_idno)
                else:
                    pass
            except:
                pass
                #print('Error wikipedia')
            
            

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']


            #wiki link in english (if available)
            try:
                wiki= party_meta_dict['wiki_en']
                
                
                if wiki not in addtoidnoparty:
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'wikimedia')
                    new_idno.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    new_idno.text = wiki
                    #do not add num of all idno elements on top only +1 so wiki en is always directly after wiki
                    org.insert(party_current_index  , new_idno)
                else:
                    pass
        
            except:
                pass
                #print('Error wikipedia en')
            

            

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']

            try:
                wikidata= party_meta_dict['wikidata']
                if wikidata not in addtoidnoparty:
                    
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'wikidata')
                    new_idno.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    new_idno.text = wikidata
                    #do not add num of all idno elements on top only +1 so wiki en is always directly after wiki
                    org.insert(party_current_index , new_idno)
                    

                else:
                    pass
            except:
                #print('Error wikidata')
                pass




            
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']

            #add official website if available
            try:
                website = party_meta_dict['website']
                if website not in addtoidnoparty:
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'politicalParty')
                    new_idno.text = website
                    org.insert(party_current_index , new_idno)
                else:
                    pass
            except:
                #print('Error website')
                pass

            #update idno count in case official website element has been added
            
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            #add idnos to xml
            #twitter
            try:
                twitter = party_meta_dict['twitter']
                if len(addtoidnoparty) == 0:
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'twitter')
                    new_idno.text = twitter
                    org.insert(party_current_index , new_idno)
                else:
                    if twitter not in addtoidnoparty:
                        new_idno = ET.Element(namespace + 'idno')
                        new_idno.set('type', 'URI')
                        new_idno.set('subtype', 'twitter')
                        new_idno.text = twitter
                        org.insert(party_current_index , new_idno)
                    else:
                        pass
            
            except:
                #print('Error twitter')
                pass

            #count idno again, in case twitter idno element has been added
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            #add instagram idno element
            try:
                instagram = party_meta_dict['instagram']
                if instagram not in addtoidnoparty:
                    new_idno = ET.Element(namespace + 'idno')
                    new_idno.set('type', 'URI')
                    new_idno.set('subtype', 'instagram')
                    new_idno.text = instagram
                    org.insert(party_current_index , new_idno)
                else:
                    pass
            except:
                #print('Error instagram')
                pass




            ET.indent(org)    

 

#####################person !!!!!!!!!!!!!!!!!!!!!!!!!!!
    #dict in case some sex tags are missing in corpus
    #(only works if there are some annotated genders already in corpus, else default: just value="M" or "F")
    missing_gender_dict = {}
    for genderperson in root.iter(namespace + "person"):
        try:
            gendertag = genderperson.find(namespace + "sex")
            if gendertag.attrib['value'] == 'M':
                if gendertag.text != None:
                    missing_gender_dict['M'] = gendertag.text
            if gendertag.attrib['value'] == 'F':
                if gendertag.text != None:
                    missing_gender_dict['F'] = gendertag.text

        except:
            pass



    personNames = str()
    birthdateFound = ''
    
    #iterate over all person tags in parsed xml
    for person in root.iter(namespace + "person"):
        #build a dict (if there are texts for sex) and save them to later build new sex tags if there is missing sex tag
        try: 
            birthtag = person.find(namespace + "birth")
            if birthtag.attrib['when'] != None:
                birthdateFound = birthtag.attrib['when']

        except:
            birthdateFound = None
            print('no birth  ', str(birthdateFound))
        
        #iterate over all persName tags
        for personnode in person.iter(namespace + 'persName'):
            personNames = ""
            #build forename of current person
            for forename in personnode.iter(namespace + 'forename'):
                if forename.text:
                    personNames = personNames + forename.text + " "

            for namelink in personnode.iter(namespace + 'nameLink'):
                if namelink.text:
                    personNames = personNames + namelink.text + " "
            #build last name of current person
            for surname in personnode.iter(namespace + 'surname'):
                if surname.text:
                    personNames = personNames + surname.text + " "

            count_person += 1
            personNames = personNames.strip()
            print('person: ' + str(count_person) + "    " + str(personNames))
            
            if args.outfile != None:
                out_filename = args.outfile[0]
                filename_out = ntpath.basename(out_filename)

            else:
                out_filename = args.infile[0]
                filename_out = ntpath.basename(out_filename)
            
            #call function with built name of person
            persid = findPersoninWiki(personNames, language_xml, person, tree, party_tag_dict, namespace, nowikiid_filename, filepnowikiid, birthdateFound, country_id )
            #call function with retrieved identifier of person
            metainfo = getwikimetainfo(persid, language_xml)
        persName_count_list = []
        for persName in person.findall(namespace + 'persName'):
            persName_count_list.append(persName)



        #handle addName (alias)
        try:
            name = person.find(namespace + 'persName')
            addName = name.find(namespace + 'addName')

            #build a list of text content for all addNames
            addName_list = list()
            for add in name.findall(namespace + 'addName'):
                addName_list.append(add)

            metainfo = person_alias(persid, metainfo, language_xml)
            
            alias_from_dict = metainfo['alias']
            temp_alias_from_dict = list()
            new_alias_from_dict = list()
            
            #check if list from dict contains , if so split (Sayeeda Warsi, Baroness Warsi)
            if len(alias_from_dict) > 1:
                
                for item in alias_from_dict:
                    if ',' in item:
                        temp_alias_from_dict = item.split(',')
                    else:
                        item = item.strip()
                        new_alias_from_dict.append(item)
                for temp in temp_alias_from_dict:
                    temp = temp.strip()
                    new_alias_from_dict.append(temp)
                
                new_alias_from_dict_uniq = list(set(new_alias_from_dict))



                #there is a addName tag already
                #check if the alias matches the values from metainfo dict 'alias'
                #if yes do not add another addName tag else add one
                if addName != None:
                    #if return from dict is a list iterate over it
                    if len(new_alias_from_dict) > 1:
                        #if text of existing addName is in dict list do nothing
                        if addName.text in new_alias_from_dict:
                            pass
                        else:
                            #else if it is not in tag yet, add it as subelement
                            for aka in new_alias_from_dict:
                                #make sure the alias is not the same as the forename surname combination from
                                #those respective xml tags
                                personNames = personNames.strip()
                                if aka != personNames:
                                    if aka not in addName_list:
                                        addName_node = ET.SubElement(name, namespace + 'addName')
                                        addName_node.text = aka
                                        addName_list.append(aka)

                    if len(new_alias_from_dict) == 1:
                        if addName.text == new_alias_from_dict[0]:
                            pass
                        else:
                            personNames = personNames.strip()
                            if new_alias_from_dict[0] != personNames:
                                if new_alias_from_dict[0] not in addName_list:
                                        addName_node = ET.SubElement(name, namespace + 'addName')
                                        addName_node.text = new_alias_from_dict[0]
                                        addName_list.append(new_alias_from_dict[0])


                if addName == None:
                    addName_list = list()
                    if len(new_alias_from_dict) > 1:
                        for aka in new_alias_from_dict:
                                #make sure the alias is not the same as the forename surname combination from
                                #those respective xml tags
                                personNames = personNames.strip()
                                if aka != personNames:
                                    if aka not in addName_list:
                                        addName_node = ET.SubElement(name, namespace + 'addName')
                                        addName_node.text = aka
                                        addName_list.append(aka)

                    if len(new_alias_from_dict) == 1:
                        personNames = personNames.strip()
                        if new_alias_from_dict[0] != personNames:
                            if new_alias_from_dict[0] not in addName_list:
                                    
                                addName_node = ET.SubElement(name, namespace + 'addName')
                                addName_node.text = new_alias_from_dict[0]
                                addName_list.append(new_alias_from_dict[0])


            if len(alias_from_dict) == 1:
                
                if ',' in alias_from_dict[0]:
                    temp_alias_from_dict = item.split(',')
                else:
                    item = alias_from_dict[0].strip()
                    new_alias_from_dict.append(item)

               

                #there is a addName tag already
                #check if the alias matches the values from metainfo dict 'alias'
                #if yes do not add another addName tag else add one
                if addName != None:
                    #if return from dict is a list iterate over it
                    #if len(new_alias_from_dict) > 1:
                    #if text of existing addName is in dict list do nothing
                    if addName.text in new_alias_from_dict:
                        pass
                    else:
                        #else if it is not in tag yet, add it as subelement
                        #for aka in new_alias_from_dict[0]:
                        #make sure the alias is not the same as the forename surname combination from those respective xml tags
                        personNames = personNames.strip()
                        if new_alias_from_dict[0] != personNames:
                            if new_alias_from_dict[0] not in addName_list:
                                addName_node = ET.SubElement(name, namespace + 'addName')
                                addName_node.text = new_alias_from_dict[0]
                                addName_list.append(new_alias_from_dict[0])

                    

                if addName == None:
                    addName_list = list()
                    #make sure the alias is not the same as the forename surname combination from
                    #those respective xml tags
                    personNames = personNames.strip()
                    if new_alias_from_dict[0] != personNames:
                        if new_alias_from_dict[0] not in addName_list:
                            addName_node = ET.SubElement(name, namespace + 'addName')
                            addName_node.text = new_alias_from_dict[0]
                            addName_list.append(new_alias_from_dict[0])

                    


        except:
            pass




        #find tag 'sex' of current person
        try:     
            gender = person.find(namespace + 'sex')
            #get index of that 'sex' tag of current person
            if gender.text:
                pass
            else:
                if len(missing_gender_dict) == 0:
                    try:
                        ###this can be changed to not doing anything
                        #currently this inserts value found on wikidata (might be flawed?)
                        new_txt = metainfo['gender']
                        gender.text = new_txt[0]
                    except:
                        pass
                if len(missing_gender_dict) != 0:
                    try:
                        gender_attrib = gender.attrib['value']
                        new_txt = missing_gender_dict[gender_attrib]
                        gender.text = new_txt
                    except:
                        pass

            indexgender = list(person).index(gender)
        except:
            indexgender = 0
            index_dict = count_new_index(namespace, person)
            current_index = index_dict['persName'] 
            handle_tag_gender(person, namespace, current_index, metainfo, language_xml, missing_gender_dict)


        gender_count_list = []
        for sex in person.findall(namespace + 'sex'):
            gender_count_list.append(sex)

        

        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex']

        handle_tag_birth(person, namespace, current_index, metainfo)
        


        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex']  + index_dict['birth']

        handle_tag_death(person, namespace, current_index, metainfo)



        try:

            affiliation = person.find(namespace + 'affiliation')
            if affiliation != None:
                pass
            else:
                party_id = find_affiliation(persid, language_xml, party_full_dict)
                index_dict = count_new_index(namespace, person)
                current_index = index_dict['persName'] + index_dict['sex']  + index_dict['birth'] + index_dict['death']

                handle_tag_affiliation(person, namespace, current_index, party_id)
            
        
        except:
            pass
        
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation']

        handle_tag_occupation(person, namespace, current_index, metainfo, language_xml)

        
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] 

        handle_tag_education(person, namespace, current_index, metainfo, language_xml)


        
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']
        
        metainfo = person_wikipedia_en(persid, metainfo, language_xml='en')
        metainfo = person_wikipedia(persid, metainfo, language_xml)
        handle_tag_idno(person, namespace, current_index, metainfo, language_xml )
       
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education'] + index_dict['idno']

        handle_tag_figure(person, namespace, current_index, metainfo)

        
        ET.indent(person)
        
        if args.outfile != None:
            out_filename = args.outfile[0]
        # #write xml structure to new xml file
        # #should be to old file ?
            with open(out_filename, 'wb') as f:
                tree.write(f, encoding='utf-8')
        
        else:
            out_file = str()
            out_file = args.infile[0]
            find_dot = out_file.index('.')
            out_filename = out_file[:find_dot] + "_out" + out_file[find_dot:]
            
            with open(out_filename, 'wb') as f:
                tree.write(f, encoding='utf-8')


    filepnowikiid.close()


    #validation below
    #args.validation
    #if no validation file entered in command line, use standard file below
    if args.validation == None:
        p = subprocess.run("java -jar jing.jar " + "ParlaMint-teiCorpus.rng" + " " + out_filename, capture_output=True, text=True)
        result = p.returncode
        print('Validating xml:')
        if int(result) == 0:
            print('FILE IS VALID')  

        if int(result) != 0:
            print('FILE IS NOT VALID')  
            print('Found the following error(s):\n')
            print(p.stdout)
    #use file entered by user
    else:
        p = subprocess.run("java -jar jing.jar " + str(args.validation[0]) + " " + out_filename, capture_output=True, text=True)
        result = p.returncode
        print('Validating xml:')
        if int(result) == 0:
            print('FILE IS VALID')  

        if int(result) != 0:
            print('FILE IS NOT VALID') 
            print('Found the following error(s):\n')
            print(p.stdout)

    
if __name__ == "__main__":
    main() 
