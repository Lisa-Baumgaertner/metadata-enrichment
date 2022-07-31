#from curses.ascii import isupper
from email import header
from json.tool import main
from pickle import TRUE
from sys import addaudithook
from SPARQLWrapper import SPARQLWrapper, JSON

import pandas as pd
import xml.etree.ElementTree as ET
import urllib.parse
import argparse
import os
import re
import requests
import lxml.etree as mytree

country_dict = {'BE':'Belgium', 'BG':'Bulgaria', 'CZ':'Czech Republic', 'DK':'Denmark', 'ES': 'Spain', 'FR':'France', 'GB':'United Kingdom', 'HR':'Croatia', 'HU':'Hungary', 'IS':'Iceland', 'IT':'Italy', 'LT':'Lithuania', 'LV':'Latvia', 'NL':'Netherlands', 'PL':'Poland', 'SI':'Slovenia', 'TR':'Turkey'}

#function to get the Wikidata identifier (e.g. Q1234) of a person
#based on the name of the person
#@param personName: name of person for which you need the wiki identifier
#return personwikiidentifier: identifier of the person on Wikidata (if available)
#if not available return Error
def findPersoninWiki(personName, language_xml, birthdateFound, country_id):
    
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
        personQuery = personQuery + "bd:serviceParam mwapi:language '" +language_xml+ "'."
        personQuery = personQuery + "?item wikibase:apiOutputItem mwapi:item."
        personQuery = personQuery + "?num wikibase:apiOrdinal true."
        personQuery = personQuery + "}"
        #personQuery = personQuery + "?item (wdt:P279|wdt:P31) ?type"
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
            #global ct_person_query1
            #ct_person_query1 += 1
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
            #personQuery = personQuery + "?item (wdt:P279|wdt:P31) ?type"
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
                #global ct_person_query2
                #ct_person_query2 += 1
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
    #personQuery = personQuery + "?item (wdt:P279|wdt:P31) ?type"
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
        #global ct_person_query3
        #ct_person_query3 += 1
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
        #personQuery = personQuery + "?item (wdt:P279|wdt:P31) ?type"
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
            #global ct_person_query4
            #ct_person_query4 += 1
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
                    #sparql_2 = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
                        #personQuery_2 = str()
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
                    #global ct_person_query5
                    #ct_person_query5 += 1
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
                            #global ct_person_query6 
                            #ct_person_query6 += 1
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
                #personQuery_2 = personQuery_2 + "FILTER('"+ birthdateFound +"'^^xsd:dateTime = ?dob)"
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
                    #global ct_person_query7
                    #ct_person_query7 += 1
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
                            #global ct_person_query8
                            #ct_person_query8 += 1
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
                                #global ct_person_query9
                                #ct_person_query9 += 1
                                return str(personwikiidentifier)
                            except:
                                pass




def getwikimetainfo(identifier, language_xml):

    if identifier != None:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        metaquery = str()
        metaquery = "SELECT ?givennameLabel ?familynameLabel ?birthLabel ?placeLabel ?deathLabel ?deathplaceLabel ?genderLabel ?educationLabel ?employLabel ?imageLabel ?twitterLabel ?facebookLabel ?instagramLabel ?websiteLabel"
        metaquery = metaquery + " WHERE{"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P735   ?givenname.}"
        metaquery = metaquery + " OPTIONAL{ wd:" + identifier + " wdt:P734   ?familyname.}"
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
        metaquery = metaquery + " SERVICE wikibase:label{bd:serviceParam wikibase:language '" + language_xml + "' .}"
        metaquery = metaquery + " }"
        
        
        sparql.setQuery(metaquery)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        

        if language_xml != "en":
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
            givenname= list()
            givenname = results_df['givennameLabel.value']
            metadict["givenname"] = list(set(givenname))
        except:
            pass

        try:
            familyname= list()
            familyname = results_df['familynameLabel.value']
            metadict["familyname"] = list(set(familyname))
        except:
            pass

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
            metadict["occupation"] = list(set(occupation))
        except:
            pass

        try:
            occupation_en = list()
            occupation_en = results_df_en['employLabel.value']
            metadict["occupation_en"] = list(set(occupation_en))
        except:
            pass

        
        try:
            education = list()
            education = results_df['educationLabel.value']
            metadict["education"] = list(set(education))
        except:
            pass

        try:
            education_en = list()
            education_en = results_df_en['educationLabel.value']
            metadict["education_en"] = list(set(education_en))
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
        
        return metadict

def find_affiliation(person_id, language_xml, party_full_dict):


    politician_affiliation_list = list() #list containing all names & alias names of the party(ies) a politician is associated with
    party_id_list = list()
    
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        affiliation_query = str()
        affiliation_query = "SELECT DISTINCT  ?partyLabel  {  "
        affiliation_query = affiliation_query + " wd:" + person_id + " wdt:P102 ?party. "
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
            
                
        politician_affiliation_list = list(set(politician_affiliation_list))
        for aff in politician_affiliation_list:
            try:
                if party_full_dict[aff]: 
                    ref = '#' + str(party_full_dict[aff])
                    party_id_list.append(str(ref))
                    
                else:
                    pass
                   

            except:
                party_id_list.append(str(aff))

        
    except:
        pass

    return party_id_list


def person_wikipedia(q_id, language_xml, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + q_id + " wdt:P31 wd:Q5 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + q_id + ". "
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



def person_wikipedia_en(q_id,  metainfo):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_wikipedia_query = str()
        party_wikipedia_query = "PREFIX schema: <http://schema.org/> "
        party_wikipedia_query = party_wikipedia_query + " SELECT ?link WHERE { "
        party_wikipedia_query = party_wikipedia_query + " wd:" + q_id + " wdt:P31 wd:Q5 ."
        party_wikipedia_query = party_wikipedia_query + " OPTIONAL { "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:about wd:" + q_id + ". "
        party_wikipedia_query = party_wikipedia_query + " ?link schema:inLanguage 'en' ."
        party_wikipedia_query = party_wikipedia_query + " ?link schema:isPartOf <https://en.wikipedia.org/> ."
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


        return metainfo

    except:
        pass


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
        #global ct_org_query1
        #ct_org_query1 += 1
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
            #global ct_org_query2
            #ct_org_query2 += 1
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
                #global ct_org_query3
                #ct_org_query3 += 1
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
                    #global ct_org_query4
                    #ct_org_query4 += 1
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
                        #global ct_org_query5
                        #ct_org_query5 += 1
                        return str(partywikiidentifier)

                    except:
                        #global ct_org_notfound
                        #ct_org_notfound += 1
                        print('party/group not found')



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
            
        except:
            pass
        abbreviation_list = list(set(abbreviation_list))
        party_meta_dict['abb'] = abbreviation_list
        return party_meta_dict

    except:
        pass


def party_name_en(party_identifier, party_meta_dict, language_xml):
    #if language_xml != 'en':
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
        
        try:
            value_name = results_df_party["label.value"][0] #to get rid of unnecessary things (e.g object etc...)
            party_meta_dict['party_name_en'] = value_name              
        except:
            pass


        return party_meta_dict

    except:
        pass

    #else:
    #    pass



def party_name(party_identifier, language_xml):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_name_query = str()
        party_name_query = "SELECT DISTINCT ?label WHERE { "
        party_name_query = party_name_query  + " wd:" + party_identifier + " rdfs:label ?label ."
        party_name_query = party_name_query  + " FILTER (langMatches( lang(?label), '" + language_xml + "' ) )  "
        party_name_query = party_name_query  + " } LIMIT 1"

        sparql.setQuery(party_name_query)
        sparql.setReturnFormat(JSON)
        results_party = sparql.query().convert()
        results_df_party = pd.json_normalize(results_party['results']['bindings'])
        party_meta_dict = {}
        try:
            value_name = results_df_party["label.value"][0] #to get rid of unnecessary things (e.g object etc...)
            party_meta_dict['party_name'] = value_name              

        except:
            pass


        return party_meta_dict

    except:
        pass

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


def regex_for_qid(string):
    return re.search('^Q\d', string)


#function to retrieve party inception date for event tag in xml file 
#@param party_identifier: WikiData identifier for the party
#@param party_meta_dict: dictionairy which holds all information about the party
#@return party_meta_dict: added inception date (if found on WikiData)
def party_event(party_identifier, party_meta_dict):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        party_socials_query = str()
        party_socials_query = "SELECT ?event ?dissolved "
        party_socials_query = party_socials_query + " WHERE { "
        party_socials_query = party_socials_query + "OPTIONAL{ wd:"+ party_identifier  + " wdt:P571 ?event .}"
        #party_socials_query = party_socials_query + "OPTIONAL{ wd:"+ party_identifier  + " wdt:P576 ?dissolved .} "
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

#function to retrieve party dissolvement date for event tag in xml file 
#@param party_identifier: WikiData identifier for the party
#@param party_meta_dict: dictionairy which holds all information about the party
#@return party_meta_dict: added dissolvment date (if found on WikiData)
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


def main():

    #set parameters for calling program on command line
    #set input file argument, output file argument and xslt file for visualisation
    parser = argparse.ArgumentParser(description='Get file parameters.')
    parser.add_argument('--infile', type=str, nargs=1, required=True)
    parser.add_argument('--outfile', type=str, nargs=1, required=True)
    parser.add_argument('--style', type=str, nargs=1, required=True)
    
    args = parser.parse_args()
    
    #check if input file exists
    try:
        with open(args.infile[0], 'r') as fh:
            fh.close()      
    except FileNotFoundError:
        return print('file ' + str(args.infile[0]) + ' not found')

    #check if xslt file exists
    try:   
        with open(args.style[0], 'r') as fh:
            fh.close()  
    except FileNotFoundError:
        return print('file ' + str(args.style) + ' not found')
    
    #check if output file exists
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
                #return print('file ' + str(args.outfile[0]) + ' not found')
    except:
        pass


    
    #parse input file into the tree
    tree = ET.parse(args.infile[0])
    #get root
    root = tree.getroot()
    
    #register tei namespace
    namespace = ""
    namespace = root.tag
    id_bracket = namespace.index('}')
    namespace = namespace[:id_bracket+1]  
    namespaceuri = namespace[1:id_bracket] 
    ET.register_namespace("", namespaceuri)
    
    #get language code of the corpus from root element
    language_xml = ""
    language_xml = root.attrib['{http://www.w3.org/XML/1998/namespace}lang']
    corpus_id = root.attrib['{http://www.w3.org/XML/1998/namespace}id']
    #findslash = corpus_id.index('-')
    #country_id = corpus_id[findslash +1:]
    if '.ana' in corpus_id:
        findslash = corpus_id.index('-')
        finddot = corpus_id.index('.')
        country_id = corpus_id[findslash + 1: finddot]

    else:
        findslash = corpus_id.index('-')
        country_id = corpus_id[findslash +1:]

    #fill party_full_dict to include all party names and their ids included in the corpus
    party_full_dict = {}   #name as key, id as value
    party_full_list = ()
    for org in root.iter(namespace + "org"):
        countorgname = []
        if org.attrib["role"] == "politicalParty":
            for orgname in org.iter(namespace + "orgName"):
                if orgname.attrib["full"] == "yes":
                    try:
                        #orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang']

                        if (orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == language_xml) :
                            party_full_dict[orgname.text] = org.attrib['{http://www.w3.org/XML/1998/namespace}id']
                    except:
                        party_full_dict[orgname.text] = org.attrib['{http://www.w3.org/XML/1998/namespace}id']
    
    
    count_org = 0
    for org in root.iter(namespace + "org"):
        all_parties_from_xml = list()
        parties_from_wiki = list()
        if org.attrib["role"] == "politicalParty":
            for orgname in org.findall(namespace + 'orgName'):
                count_org += 1
                
                print(str(count_org) + '   ' + str(orgname.text))
                orgname_txt = orgname.text.strip()
                all_parties_from_xml.append(orgname_txt)
                if orgname.attrib['full'] == 'yes':
                    try: 
                        #orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                        #check if the orgname has a lang attribute
                        if (orgname.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == language_xml) :
                            party_id = findPartyinWiki(orgname.text, country_id)
                            party_wiki_dict = party_name(party_id, language_xml)
                            party_wiki_dict = party_name_en(party_id, party_wiki_dict, language_xml) #get English name of party
                            party_wiki_dict = party_abbrev(party_id, party_wiki_dict, language_xml)
                            #get inception date of party
                            party_wiki_dict = party_event(party_id, party_wiki_dict)
                            party_wiki_dict = party_dissolved(party_id, party_wiki_dict)
                            party_wiki_dict = party_wikipedia(party_id, language_xml, party_wiki_dict)
                            party_wiki_dict = party_wikipedia_en(party_id, party_wiki_dict, language_xml='en')
                            party_wiki_dict = party_twitter(party_id, party_wiki_dict)
                            party_wiki_dict = party_instagram(party_id, party_wiki_dict)
                            party_wiki_dict = party_website(party_id, party_wiki_dict)

                    except:
                        
                        party_id = findPartyinWiki(orgname.text, country_id)
                        party_wiki_dict = party_name(party_id, language_xml)
                        party_wiki_dict = party_name_en(party_id, party_wiki_dict, language_xml) #get English name of party
                        party_wiki_dict = party_abbrev(party_id, party_wiki_dict, language_xml)
                        party_wiki_dict = party_event(party_id, party_wiki_dict)
                        party_wiki_dict = party_dissolved(party_id, party_wiki_dict)
                        party_wiki_dict = party_wikipedia(party_id, language_xml, party_wiki_dict)
                        party_wiki_dict = party_wikipedia_en(party_id, party_wiki_dict, language_xml='en')
                        party_wiki_dict = party_twitter(party_id, party_wiki_dict)
                        party_wiki_dict = party_instagram(party_id, party_wiki_dict)
                        party_wiki_dict = party_website(party_id, party_wiki_dict)

            try:
                if party_wiki_dict['party_name']:
                    if regex_for_qid(party_wiki_dict['party_name']) == None:
                        parties_from_wiki.append(party_wiki_dict['party_name'])
                    else:
                        pass
            except:
                pass

            try:
                if party_wiki_dict['party_name_en']:
                    if regex_for_qid(party_wiki_dict['party_name_en']) == None:
                        parties_from_wiki.append(party_wiki_dict['party_name_en'])
                    else:
                        pass
            except:
                pass

            try:
                abbrev_list = party_wiki_dict['abb']
                if len(abbrev_list) >1:
                    for abbrev in abbrev_list:
                        if regex_for_qid(abbrev) == None:
                            parties_from_wiki.append(abbrev)
                        else:
                            pass
            except:
                pass


            #sort list to later add elements in right order
            parties_from_wiki = list(sorted(parties_from_wiki, key = len))
            parties_from_wiki = list(set(parties_from_wiki))
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName']

            #add alternative name and abbreviation
            try:
                for wiki_party in parties_from_wiki:
                    if wiki_party not in all_parties_from_xml:
                        
                        if wiki_party.isupper() == False:
                            name = ET.Element(namespace + 'orgName')
                            name.text = wiki_party
                            name.set('wd', 'alternative')
                            name.set('full', 'yes')
                            org.insert(party_current_index, name)

                        #if it is abbreviation (assumption: abbreviations are all caps)
                        if wiki_party.isupper() == True:
                            name = ET.Element(namespace + 'orgName')
                            name.text = wiki_party
                            name.set('wd', 'alternative')
                            name.set('full', 'init')
                            org.insert(party_current_index, name)
                        
            except:
                pass

            inception_list = list()
            dissollved_list = list()
            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event']
            
            try:
                for event in org.findall(namespace + 'event'):
                    if event.attrib['from']:
                        inception_list.append(event.attrib['from'])
                    if event.attrib['to']:
                        dissollved_list.append(event.attrib['to'])

            except:
                pass

            inceptionFound = False
            dissolvedFound = False

            try:
        
                item = party_wiki_dict['event']
                inception = item.split('T')

                if inception[0] not in inception_list:
                    if org.find(namespace + 'event') != None:
                        inceptionFound = True
                        difference = ET.Element(namespace + 'event')
                        difference.set('wd', 'alternative')
                        difference.set('from', inception[0])
                            

                diss = party_wiki_dict['dissolved']
                dissolved = diss.split('T')

                if dissolved[0] not in dissollved_list:
                    if org.find(namespace + 'event') != None:
                        dissolvedFound = True
                        difference.set('to', dissolved[0])

            except:
                pass
            
            if (inceptionFound == True) and (dissolvedFound == True):
                difference = ET.Element(namespace + 'event')
                difference.set('wd', 'alternative')
                difference.set('from', inception[0])
                difference.set('to', dissolved[0])
                org.insert(party_current_index, difference)
            else:
                if (inceptionFound == True) and (dissolvedFound == False):
                    difference = ET.Element(namespace + 'event')
                    difference.set('wd', 'alternative')
                    difference.set('from', inception[0])
                    org.insert(party_current_index, difference)

                if (inceptionFound == False) and (dissolvedFound == True):
                    difference = ET.Element(namespace + 'event')
                    difference.set('wd', 'alternative')
                    difference.set('to', dissolved[0])
                    org.insert(party_current_index, difference)
                   

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']

            idno_party_list = list()
            for idno in org.findall(namespace + 'idno'):
                idno_party_list.append(idno.text)
            party_website_list = list()
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'politicalParty':
                    party_website_list.append(idno.text)
            
            party_wiki_en_list = list()
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'wikimedia':
                    if 'en.wikipedia' in idno.text:
                        party_wiki_en_list.append(idno.text)

            party_wikidata_list = list()
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'wikidata':
                    party_wikidata_list.append(idno.text)

            party_twitter_list = list()
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'twitter':
                    party_twitter_list.append(idno.text)

            party_instagram_list = list()
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'instagram':
                    party_instagram_list.append(idno.text)

            party_wiki_list = list()
            wikidata_str = str(language_xml) + '.wikipedia'
            for idno in org.findall(namespace + 'idno'):
                if idno.attrib['type'] == 'wikimedia':
                    if wikidata_str in idno.text:
                        party_wiki_list.append(idno.text)


            try:
                ig = party_wiki_dict['instagram']
                if len(party_instagram_list) != 0:
                    if ig not in party_instagram_list:
                        idnoelement = ET.Element(namespace + 'idno')
                        idnoelement.set('wd', 'alternative')
                        idnoelement.set('type', 'instagram')
                        idnoelement.text = ig
                        org.insert(party_current_index, idnoelement)

            except:
                pass 


            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            try:
                twitter = party_wiki_dict['twitter']
                if len(party_twitter_list) != 0:
                    if twitter not in party_twitter_list:
                        twitterelement = ET.Element(namespace + 'idno')
                        twitterelement.set('wd', 'alternative')
                        twitterelement.set('type', 'twitter')
                        twitterelement.text = twitter
                        org.insert(party_current_index, twitterelement)

            except:
                pass 

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            try:
                website = party_wiki_dict['website']
                if len(party_website_list) != 0:
                    #do not check for if 'website' in string, because no consistent schema for website links
                    if website not in party_website_list:
                        websiteelement = ET.Element(namespace + 'idno')
                        websiteelement.set('wd', 'alternative')
                        websiteelement.set('type', 'politicalParty')
                        websiteelement.text = website
                        org.insert(party_current_index, websiteelement)

            except:
                pass 

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            try:
                wikidata_str = str(language_xml) + '.wikipedia'
                wiki = party_wiki_dict['wiki']
                if len(party_wiki_list) != 0:
                    if wiki not in party_wiki_list:
                        wikielement = ET.Element(namespace + 'idno')
                        wikielement.set('wd', 'alternative')
                        wikielement.set('type', 'wikimedia')
                        wikielement.set('{http://www.w3.org/XML/1998/namespace}lang', language_xml)
                        wikielement.text = wiki
                        org.insert(party_current_index, wikielement)

            except:
                pass 

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            try:
                wiki_en = party_wiki_dict['wiki_en']
                if len(party_wiki_en_list) != 0:                    
                    if wiki_en not in party_wiki_en_list:
                        wiki_en_element = ET.Element(namespace + 'idno')
                        wiki_en_element.set('wd', 'alternative')
                        wiki_en_element.set('type', 'wikimedia')
                        wiki_en_element.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                        wiki_en_element.text = wiki_en
                        org.insert(party_current_index, wiki_en_element)

            except:
                pass 

            party_index_dict = party_count_new_index(namespace, org)
            party_current_index = party_index_dict['orgName'] + party_index_dict['event'] + party_index_dict['idno']
            try:
                wikidata = party_wiki_dict['wikidata']
                if len(party_wikidata_list) != 0:
                    if wikidata not in party_wikidata_list:
                        wikidata_element = ET.Element(namespace + 'idno')
                        wikidata_element.set('wd', 'alternative')
                        wikidata_element.set('type', 'wikidata')
                        wikidata_element.text = wikidata
                        org.insert(party_current_index, wikidata_element)

            except:
                pass 
            ET.indent(org, '  ')

    personNames = str()
    count_pers = 0
    #iterate over all person tags in parsed xml
    for person in root.iter(namespace + "person"):
        count_pers += 1  
        try: 
            birthtag = person.find(namespace + "birth")
            if birthtag.attrib['when'] != None:
                birthdateFound = birthtag.attrib['when']
        except:
            birthdateFound = None    
        #iterate over all persName tags
        for personnode in person.iter(namespace + 'persName'):
            personNames = ""
            #build forename of current person
            for forename in personnode.iter(namespace + 'forename'):
                forename_txt = forename.text.strip()
                personNames = personNames + forename_txt + " "
            #build last name of current person
            for surname in personnode.iter(namespace + 'surname'):
                surname_txt = surname.text.strip()
                personNames = personNames + surname_txt + " "
        
        print(str(count_pers) + '    ' + str(personNames))
        q_id = findPersoninWiki(personNames, language_xml, birthdateFound, country_id)
        metainfo = getwikimetainfo(q_id, language_xml)

        surname_list = list()
        try:
            for persname in person.findall(namespace + 'persName'):
                for surname in persname.findall(namespace + 'surname'):
                    surname_list.append(surname.text)

        except:
            pass

        try:
            for item in metainfo['familyname']:
                if item not in surname_list:
                    if regex_for_qid(item) == None:                        
                        persNameElement = person.find(namespace + 'persName')
                        if persNameElement.find(namespace + 'surname') != None:
                            difference = ET.SubElement(persNameElement, namespace + 'surname')
                            difference.text = item
                            difference.set('wd', 'alternative' )
                    else:
                        pass
            

        except:
            pass

        forename_list = list()
        try:
            for persname in person.findall(namespace + 'persName'):
                for forename in persname.findall(namespace + 'forename'):
                    forename_list.append(forename.text)

        except:
            pass

        try:
       
            for item in metainfo['givenname']:
                if item not in forename_list:
                    if regex_for_qid(item) == None:
                        persNameElement = person.find(namespace + 'persName')
                        if persNameElement.find(namespace + 'forename') != None:
                            difference = ET.SubElement(persNameElement, namespace + 'forename')
                            difference.set( 'wd',  'alternative' )
                            difference.text = item
                    else:
                        pass

        except:
            pass

        gender_text_list = list()
        gender_attrib_list = list()

        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] 
        try:
            for gender in person.findall(namespace + 'sex'):
                gender_text_list.append(gender.text)
                if gender.attrib['value']:
                    gender_attrib_list.append(gender.attrib['value'])

        except:
            pass

        try:
       
            for item in metainfo['gender_en']:
                if item == 'male':
                    temp_item = 'M'
                if item == 'female':
                    temp_item = 'F'
                if temp_item not in gender_attrib_list:
                    if person.find(namespace + 'sex') != None:
                        difference = ET.Element( namespace + 'sex')
                        difference.set( 'wd', 'alternative')
                        difference.set('value' , temp_item)
                        person.insert(current_index, difference)

        except:
            pass


        try:
       
            for item in metainfo['gender']:
                if item not in gender_text_list:
                    if regex_for_qid(item) == None:
                        if person.find(namespace + 'sex') != None:
                            genderElement = person.find(namespace + 'sex')
                            difference = ET.Element( namespace + 'sex')
                            difference.text = item
                            difference.set('wd', 'alternative')
                            person.insert(current_index, difference)
                    else:
                        pass

        except:
            pass
        

        birthdate_list = list()
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] 
        try:
            for birth in person.findall(namespace + 'birth'):
                birthdate_list.append(birth.attrib['when'])

        except:
            pass

        try:
       
            for item in metainfo['birthdate']:
                item = item.split('T')
                if item[0] not in birthdate_list:
                    if person.find(namespace + 'birth') != None:
                        persNameElement = person.find(namespace + 'birth')
                        difference = ET.Element(namespace + 'birth')
                        difference.set('wd', 'alternative')
                        difference.set('when', item[0])
                        person.insert(current_index, difference)

        except:
            pass

        birthplace_list = list()
        try:
            for birth in person.findall(namespace + 'birth'):
                for place in persname.findall(namespace + 'placeName'):
                    birthplace_list.append(place.text)

        except:
            pass

        try:
       
            for item in metainfo['birthplace']:
                if item not in birthplace_list:
                    if regex_for_qid(item) == None:
                        if person.find(namespace + 'birth') != None:
                            birth = person.find(namespace + 'birth')
                            place = birth.find(namespace + 'placeName')
                            difference = ET.SubElement(birth, namespace + 'placeName')
                            difference.text = item
                            difference.set('wd', 'alternative')
                    else:
                        pass

        except:
            pass



        deathdate_list = list()
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth']
        try:
            for death in person.findall(namespace + 'death'):
                deathdate_list.append(death.attrib['when'])

        except:
            pass

        try:
       
            for item in metainfo['deathdate']:
                item = item.split('T')
                if item[0] not in deathdate_list:
                    if person.find(namespace + 'death') != None:
                        persNameElement = person.find(namespace + 'death')
                        difference = ET.Element(namespace + 'death')
                        difference.set('wd', 'alternative')
                        difference.set('when', item[0])
                        person.insert(current_index, difference)

        except:
            pass

        deathplace_list = list()
        try:
            for death in person.findall(namespace + 'death'):
                for place in persname.findall(namespace + 'placeName'):
                    deathplace_list.append(place.text)

        except:
            pass

        try:
       
            for item in metainfo['deathplace']:
                if item not in deathplace_list:
                    if regex_for_qid(item) == None:
                        if person.find(namespace + 'death') != None:
                            death = person.find(namespace + 'death')
                            place = death.find(namespace + 'placeName')
                            difference = ET.SubElement(death, namespace + 'placeName')
                            difference.text = item
                            difference.set('wd', 'alternative')
                    else:
                        pass

        except:
            pass

        ret_list = find_affiliation(q_id, language_xml, party_full_dict) #list retrieving names of parties
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death']

        try:
            aff_from_xml = list()
            for affiliation in person.findall(namespace + 'affiliation'):
                if affiliation.attrib['role'] == 'member':
                    aff_from_xml.append(str(affiliation.attrib['ref']))

            for ret_item in ret_list:
                if ret_item in aff_from_xml:
                    #already contains affiliation
                    pass
                if ret_item not in aff_from_xml:
                    aff = ET.Element(namespace + 'affiliation')
                    aff.set('wd', 'alternative')
                    aff.set('role', "member")
                    aff.set('ref', ret_item)
                    person.insert(current_index, aff )
            
        except:
            pass
               
        occupation_list = list()
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation']
        try:
            for occupation in person.findall(namespace + 'occupation'):
                occupation_list.append(occupation.text)

        except:
            pass

        try:
       
            for item in metainfo['occupation']:
                if item not in occupation_list:
                    if regex_for_qid(item) == None:
                        if person.find(namespace + 'occupation') != None:
                            persNameElement = person.find(namespace + 'occupation')
                            difference = ET.Element(namespace + 'occupation')
                            difference.text = item
                            difference.set('wd', 'alternative')
                            person.insert(current_index, difference)
                    else:
                        pass

        except:
            pass


        education_list = list()
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation']
        try:
            for education in person.findall(namespace + 'education'):
                education_list.append(education.text)

        except:
            pass

        try:
            temp = metainfo['education']
            for i in temp:
                if i not in education_list:
                    if regex_for_qid(i) == None:
                        if person.find(namespace + 'education') != None:
                            difference = ET.Element( namespace + 'education')
                            difference.text = i
                            difference.set('wd', 'alternative' )
                            person.insert(current_index, difference)
                    else:
                        pass

        except:
            pass


        idno_list = list()
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']
        try:
            for idno in person.findall(namespace + 'idno'):
                idno_list.append(idno.text)

        except:
            pass

        try:
            for item in metainfo['twitter']:
                for xml_idno in idno_list:
                    if 'twitter' in xml_idno:
                        if item not in idno_list:
                            if person.find(namespace + 'idno').attrib['type'] == 'twitter':
                                persNameElement = person.find(namespace + 'idno')
                                difference = ET.Element( namespace + 'idno')
                                difference.set('wd', 'alternative')
                                difference.set('type', 'twitter')
                                difference.text = item
                                person.insert(current_index, difference)

        except:
            pass


        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education'] 

        try:

            for item in metainfo['website']:
                if item not in idno_list:
                    if person.find(namespace + 'idno').attrib['type'] == 'personal':
                        persNameElement = person.find(namespace + 'idno')
                        difference = ET.Element( namespace + 'idno')
                        difference.set('wd', 'alternative' )
                        difference.set('type', 'personal')
                        difference.text = item
                        person.insert[current_index, difference]

        except:
            pass


        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']

        try:

            for item in metainfo['facebook']:
                for xml_idno in idno_list:
                    if 'facebook' in xml_idno:
                        if item not in idno_list:
                            if person.find(namespace + 'idno').attrib['type'] == 'facebook':
                                persNameElement = person.find(namespace + 'idno')
                                difference = ET.Element( namespace + 'idno')
                                difference.set('wd', 'alternative')
                                difference.set('type', 'facebook')
                                difference.text = item
                                person.insert(current_index, difference)

        except:
            pass

        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']

        try:

            for item in metainfo['instagram']:
                for xml_idno in idno_list:
                    if 'instagram' in xml_idno:
                        if item not in idno_list:
                            if person.find(namespace + 'idno').attrib['type'] == 'instagram':
                                persNameElement = person.find(namespace + 'idno')
                                difference = ET.Element( namespace + 'idno')
                                difference.set('wd', 'alternative')
                                difference.set('type', 'instagram')
                                difference.text = item
                                person.insert(current_index, difference)

        except:
            pass

        metainfo = person_wikipedia(q_id, language_xml, metainfo)
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']

        try:
            
            item = metainfo['wiki']
            wikipedia_lang = str(language_xml) + ".wikipedia"

            for xml_idno in idno_list:
                    if wikipedia_lang in xml_idno:
                        if item not in idno_list:
                            if person.find(namespace + 'idno').attrib['type'] == 'wikimedia':
                                persNameElement = person.find(namespace + 'idno')
                                difference = ET.Element( namespace + 'idno')
                                difference.set('wd', 'alternative')
                                difference.set('type', 'wikimedia')
                                difference.text = item
                                person.insert(current_index, difference)

        except:
            pass

        metainfo = person_wikipedia_en(q_id,  metainfo)
        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education']

        try:

            item = metainfo['wiki_en']
            wikipedia_lang =  "en.wikipedia"
            for xml_idno in idno_list:
                if wikipedia_lang in xml_idno:
                    if item not in idno_list:
                        if person.find(namespace + 'idno').attrib['type'] == 'wikimedia':
                            persNameElement = person.find(namespace + 'idno')
                            difference = ET.Element( namespace + 'idno')
                            difference.set('wd', 'alternative')
                            difference.set('type', 'wikimedia')
                            difference.text = item
                            person.insert(current_index, difference)

        except:
            pass


        index_dict = count_new_index(namespace, person)
        current_index = index_dict['persName'] + index_dict['sex'] + index_dict['birth'] + index_dict['death'] + index_dict['affiliation'] + index_dict['occupation'] + index_dict['education'] + index_dict['idno']
        figure_list = list()

        try:
            for figure in person.findall(namespace + 'figure'):
                figure_list.append(figure.text)

        except:
            pass

        try:
            temp = metainfo['image']
            for i in temp:
                if i not in education_list:
                    if person.find(namespace + 'figure') != None:
                        difference = ET.Element( namespace + 'figure')
                        difference.set('wd', 'alternative')
                        person.insert(current_index, difference)
                        graphic = ET.SubElement(difference, namespace + 'graphic')
                        graphic.set('wd', 'alternative')
                        graphic.set( 'url' , i)


        except:
            pass

        ET.indent(person)


    temp_filename = str(args.outfile[0]).replace('.xml', '_tmp.xml')
    with open(temp_filename, 'wb') as f:
        #need to specify encoding, otherwise e.g. turkish special characters
        #will be displayed as HTML 
        tree.write(f, encoding='utf-8', xml_declaration=True)
    f.close()
    
    #new_tree = ET.parse("C:\\Users\\Uni\\Desktop\\turkeydifflist.xml")
    new_tree = ET.parse(temp_filename)
    new_root = new_tree.getroot()
    
    final_root = ET.Element('difference')
    final_tree = ET.ElementTree(final_root)


    count_id = 1
    
    for org_node in new_root.iter(namespace + 'org'):
        orgAdded = False
        for orgName in org_node.findall(namespace + 'orgName'):
            try:
                orgName.attrib['wd']
                if orgName.attrib['wd']:
                    final_root.insert(count_id, org_node)
                    count_id += 1
                    orgAdded = True
                    break
            except:
                pass

        if orgAdded == False:
            orgAdded = False
            for event in org_node.findall(namespace + 'event'):
                try:
                    event.attrib['wd']
                    if event.attrib['wd']:
                        final_root.insert(count_id, org_node)
                        count_id += 1
                        orgAdded = True
                        break
                except:
                    pass

        if orgAdded == False:
            orgAdded = False
            for idno in org_node.findall(namespace + 'idno'):
                try:
                    idno.attrib['wd']
                    if idno.attrib['wd']:
                        final_root.insert(count_id, org_node)
                        count_id += 1
                        orgAdded = True
                        break
                except:
                    pass
    
    for pers_node in new_root.iter(namespace + 'person'):
        personAdded = False
        persName = pers_node.find(namespace + 'persName')
        for forename in persName.findall(namespace + 'forename'):
            try:
                forename.attrib['wd']
                if forename.attrib["wd"]:
                    final_root.insert(count_id, pers_node)
                    count_id += 1
                    personAdded = True
                    break
            except:
                pass

        if personAdded == False:
            for surname in persName.findall(namespace + 'surname'):
                try:
                    surname.attrib['wd']
                    if surname.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass
        
        if personAdded == False:
            for gender in pers_node.findall(namespace + 'sex'):
                try:
                    gender.attrib['wd']
                    if gender.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass

        if personAdded == False:
            for birth in pers_node.findall(namespace + 'birth'):
                try:
                    birth.attrib['wd']
                    if birth.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass

        if personAdded == False:

            for birth in pers_node.findall(namespace + 'birth'):
                try:
                    for place in birth.findall(namespace + 'placeName'):
                        place.attrib['wd']
                        if place.attrib["wd"]:
                            final_root.insert(count_id, pers_node)
                            count_id += 1
                            personAdded = True
                            break
                except:
                    pass

        if personAdded == False:
            for death in pers_node.findall(namespace + 'death'):
                try:
                    death.attrib['wd']
                    if death.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass   


        if personAdded == False:

            for death in pers_node.findall(namespace + 'death'):
                try:
                    for place in death.findall(namespace + 'placeName'):
                        place.attrib['wd']
                        if place.attrib["wd"]:
                            final_root.insert(count_id, pers_node)
                            count_id += 1
                            personAdded = True
                            break
                except:
                    pass


        if personAdded == False:
            for aff in pers_node.findall(namespace + 'affiliation'):
                try:
                    aff.attrib['wd']
                    if aff.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass  
            
        if personAdded == False:
            for occ in pers_node.findall(namespace + 'occupation'):
                try:
                    occ.attrib['wd']
                    if occ.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass  

        if personAdded == False:
            for edu in pers_node.findall(namespace + 'education'):
                try:
                    edu.attrib['wd']
                    if edu.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass

        if personAdded == False:
            for idno in pers_node.findall(namespace + 'idno'):
                try:
                    idno.attrib['wd']
                    if idno.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass 

        if personAdded == False:
            for figure in pers_node.findall(namespace + 'figure'):
                try:
                    figure.attrib['wd']
                    if figure.attrib["wd"]:
                        final_root.insert(count_id, pers_node)
                        count_id += 1
                        personAdded = True
                        break
                except:
                    pass    



    ET.indent(final_root)
    with open(args.outfile[0], 'wb') as f:
        #need to specify encoding, otherwise e.g. turkish special characters
        #will be displayed as HTML 
        final_tree.write(f, encoding='utf-8', xml_declaration=True)

    #delete temp file 
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    else:
        print("The file does not exist")

    final_diff = open(args.outfile[0], 'r', encoding='utf-8')
    final_diff_list = list()
    lines = final_diff.readlines()
    for line in lines:
        line_str = line.replace(' xmlns="http://www.tei-c.org/ns/1.0"', '') 
        final_diff_list.append(line_str)

    final_diff.close()

    final_diff = open(args.outfile[0], 'w',encoding='utf-8')
    final_diff.writelines((final_diff_list))
        
    final_diff.close()


    #stylesheet
    xml = mytree.parse(args.outfile[0])
    xslt = mytree.parse(args.style[0])
    transform = mytree.XSLT(xslt)
    xmltransformed = transform(xml)
    style_name = str(args.outfile[0]).replace('.xml', '.html')
    stylesheet = open(style_name, 'wb')

    
    #stylesheet = open(args.html, 'wb')
    stylesheet.write(mytree.tostring(xmltransformed, pretty_print=False))
    stylesheet.close()




if __name__ == "__main__":
    main()  