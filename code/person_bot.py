from SPARQLWrapper import SPARQLWrapper, JSON
import requests

from datetime import datetime
#!/usr/bin/python3
import pywikibot
import argparse


#function for pywikibot  to create new Wikidata pages for the persons who were not found to have one
#@param wiki_property_ids: dictionairy containing property ids for the needed Wikidata properties needed for the new page
#@param store_values_dict: dictionairy containing the text information about a person retrieved from corpus/file that was written when no wiki id was found
#@param fixed_identifiers: dictionairy containing q identifiers that are always the same and needed e.g female, male , politician etc
def mypywikibot(wiki_property_ids, store_values_dict, fixed_identifiers, language_tag):
    site = pywikibot.Site("test", "wikidata")

    #function to create new page
    #change name 
    def create_page(site, label_dict):
        new_item = pywikibot.ItemPage(site)
        new_item.editLabels(labels=label_dict, summary="Setting labels")
        # Add description here or in another function
        return new_item.getID()
    

    
    
    try:
        forename_str = ""
        surname_str = ""
        #build full name from lists in dictionairy
        if isinstance(store_values_dict['forename'], list):
            for forename in store_values_dict['forename']:
                forename_str = forename_str + " " + forename
        else:
            forename_str = store_values_dict['forename']
        
        if isinstance(store_values_dict['surname'], list):
            for surname in store_values_dict['surname']:
                surname_str = surname_str + " " + surname
        else:
            surname_str = store_values_dict['surname']

        name = forename_str + " " + surname_str

    except:
        pass


    some_labels = {"en": name, language_tag: name}
    new_item_id = create_page(site, some_labels)

    repo = site.data_repository()
    #needs change to create new site
    item = pywikibot.ItemPage(repo, new_item_id)
    itemdata = item.get() 


    #set labels and description for the new page
    mydescriptions = {'en': 'politician', 'de': 'Politiker', 'fr': 'personnalité politique','is':'stjórnmálamaður'}
    my_labels = {'en': name , language_tag : name}
    item.editDescriptions(mydescriptions, summary= u'Setting/updating descriptions.')
    for key in mydescriptions:
        item.editDescriptions({key: mydescriptions[key]},
            summary="Setting description: {} = '{}'".format(key, mydescriptions[key]))

    for key in my_labels:
        item.editLabels({key: my_labels[key]},
            summary="Setting label: {} = '{}'".format(key, my_labels[key]))


    #get all claims
    all_claims = item.get(u'claims')

    #get property ids to check if there is an existing claim for this already
    instance_of = ""
    human = ""
    try: 
        instance_of = wiki_property_ids['instance of']
        human = fixed_identifiers['human']

        if instance_of in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have instance human!')
        else:
            #add instance of claim to page
            human_claim = pywikibot.Claim(repo, instance_of)
            target = pywikibot.ItemPage(repo, human)
            human_claim.setTarget(target)
            item.addClaim(human_claim, summary='Adding claim')

    except:
        print('no instance of property found')

    
    #set gender property on page (if claim not already there)
    gender_p = ""
    gender_q = ""
    try:
        
        gender_p = wiki_property_ids['sex or gender']
        if store_values_dict['gender'] == 'F':
            gender_q = fixed_identifiers['female']
        if store_values_dict['gender'] == 'M':
            gender_q = fixed_identifiers['male']

        if gender_p in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have gender!')
        else:
        #add gender claim to page
            gender_claim = pywikibot.Claim(repo, gender_p)
            target = pywikibot.ItemPage(repo, gender_q)
            gender_claim.setTarget(target)
            item.addClaim(gender_claim, summary='Adding claim')

    except:
        print("no gender property was found")


    #set date of birth property if not already found in claims
    dateofbirth_p = ""
    dateofbirth_value = ""
    try:
        dateofbirth_p = wiki_property_ids['date of birth']
        dateofbirth_value = store_values_dict['birth']
        dateofbirth_value = datetime.utcnow().strftime(dateofbirth_value)
        #split date of birth value to fit the required wikidata format
        dateofbirth_value = dateofbirth_value.split('-')

        if dateofbirth_p in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have birthdate!')
        else:
            #add birthdate claim to page
            birth_claim = pywikibot.Claim(repo, dateofbirth_p)
            dateOfBirth = pywikibot.WbTime(year=int(dateofbirth_value[0]), month=int(dateofbirth_value[1]), day=int(dateofbirth_value[2]))
            birth_claim.setTarget(dateOfBirth)
            item.addClaim(birth_claim, summary='Adding claim')

    except:
        print("no birthdate property was found")


    #set official websote property
    website_p = ""
    website_value = ""
    try:
        website_p = wiki_property_ids['official website']
        website_value = store_values_dict['idno']

        if website_p in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have official website!')
        else:
            #add image claim to page
            website_claim = pywikibot.Claim(repo, website_p)
            website_claim.setTarget(website_value) #Using a string
            item.addClaim(website_claim, summary=u'Adding string claim')
    except:
        print("no website property found")



    #set occupation property (this is always set to politician, because there probably wont be anything in corpus)
    occupation_p = ""
    occupation_value = ""

    try:
        occupation_p = wiki_property_ids['occupation']
        #all are by default set to politician as there probably will not come back any occupation value from corpus
        occupation_value = fixed_identifiers['politician']
        if occupation_p in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have occupation!')
        else:
            #add occupation claim to page
            occ_claim = pywikibot.Claim(repo, occupation_p)
            target = pywikibot.ItemPage(repo, occupation_value)
            occ_claim.setTarget(target)
            item.addClaim(occ_claim, summary='Adding claim')
    
    except:
        print("no occupation property found")
    

    #set affiliation property
    affiliation_p = ""
    affiliation_value = ""

    try:
        affiliation_p = wiki_property_ids['member of']
        #all are by default set to politician as there probably will not come back any occupation value from corpus
        affiliation_value = fixed_identifiers['affiliation']
        if affiliation_p in all_claims[u'claims']: 
            pywikibot.output(u'Error: Already have affiliation!')
        else:
            #add occupation claim to page

            if affiliation_value != None:
                for val in affiliation_value:
                    occ_claim = pywikibot.Claim(repo, affiliation_p)
                    target = pywikibot.ItemPage(repo, val)
                    occ_claim.setTarget(target)
                    item.addClaim(occ_claim, summary='Adding claim')
            else: 
                pass
    
    except:
        print("no occupation property found")





def main():
    #set argument for strarting program from command line
    #set input file argument
    parser = argparse.ArgumentParser(description='Set input file')
    parser.add_argument('--infile', type=str, nargs=1, required=True)
    args = parser.parse_args()

    try:
        with open(args.infile[0], 'r') as fh:
            fh.close()      
    except FileNotFoundError:
        return print('file ' + str(args.infile[0]) + ' not found')

    #get values from corpuslist of people for which no info has been found 
    store_values_dict = {}
    multiples = []
    #get language tag from file anme to use for populating the wikidata page
    find_dot = str(args.infile[0]).index('.txt')
    find_underscore = str(args.infile[0]).index('_')
    language_tag = str(args.infile[0])[find_underscore + 1:find_dot] 

    f = open(args.infile[0], "r", encoding="utf-8")

    for line in f:
        multiples = list()
        store_values_dict = {}
        multiples = []
        split_line = line.split(';')

        for item in split_line:
            item_split = item.split(',')
        
        # #check to see if key already in dict, if so make list to keep all values, else overwritten
            if len(item_split) == 2:
                if store_values_dict.get(item_split[0]):
                    multiples.append(store_values_dict.get(item_split[0]))
                    multiples.append(item_split[1])
                    store_values_dict[item_split[0]] = multiples
                    multiples = list()
                else:
                    store_values_dict[item_split[0]] = item_split[1]

    
        
        wiki_property_ids = {}
        properties_to_retrieve = ['instance of', 'sex or gender', 'name in native language', 'date of birth', 'member of', 'official website', 'occupation']

        for prop in properties_to_retrieve:
        #query to retrieve P identifier of properties by name 
            params_prop = dict (
                    action='wbsearchentities',
                    format='json',
                    language='en',
                    uselang='en',
                    type='property',
                    search= prop
                    )

            #response = requests.get('https://www.wikidata.org/w/api.php?', params_prop).json() #api address for real wikidata
            response = requests.get('https://test.wikidata.org/w/api.php?', params_prop).json() 
            wiki_property_ids[prop] = response.get('search')[0]['id']

        #search to get wikidata item identifiers for fixed values that have to be entered as identifiers (not strings)
        #e.g. gender, human and party

        #list to search for 
        fixed_identifier_list = ['human', 'male', 'female', 'politician']
        fixed_identifiers = {}
        for fixedid in fixed_identifier_list:
            params_ident = dict (
                        action='wbsearchentities',
                        format='json',
                        language='en',
                        uselang='en',
                        type='item',
                        search= fixedid
                        )

            #response = requests.get('https://www.wikidata.org/w/api.php?', params_ident).json() 
            response = requests.get('https://test.wikidata.org/w/api.php?', params_ident).json() 
            fixed_identifiers[fixedid] = response.get('search')[0]['id']
        

        try:
            #find Q identifier for party affiliation
            res = list()
            searchaffiliation = store_values_dict['affiliation']

            if searchaffiliation is list:
                for item in searchaffiliation:
                    params_ident = dict (
                                action='wbsearchentities',
                                format='json',
                                language='en',
                                uselang='en',
                                type='item',
                                search= item#searchaffiliation
                                )

                    #response = requests.get('https://www.wikidata.org/w/api.php?', params_ident).json() 
                    response = requests.get('https://test.wikidata.org/w/api.php?', params_ident).json() 
                    res.append(response.get('search')[0]['id'] )

            if searchaffiliation is not list:
                params_ident = dict (
                            action='wbsearchentities',
                            format='json',
                            language='en',
                            uselang='en',
                            type='item',
                            search= searchaffiliation
                            )

                #response = requests.get('https://www.wikidata.org/w/api.php?', params_ident).json() 
                response = requests.get('https://test.wikidata.org/w/api.php?', params_ident).json() 
                res.append(response.get('search')[0]['id'] )
            fixed_identifiers['affiliation'] = res   

        except:
            fixed_identifiers['affiliation'] = None

        
        
        #build name to check test wikidata for person (make sure page does really not exist)
        try:
            forename = store_values_dict['forename']
            surname = store_values_dict['surname']
            full_name = str(forename) + " " + str(surname)
            full_name = full_name.replace("'", "")
            full_name = full_name.replace("[", "")
            full_name = full_name.replace("]", "")
            full_name = full_name.replace(",", "")
            print(full_name)
            
            params_name = dict (
                action='wbsearchentities',
                format='json',
                language='en',
                uselang='en',
                type='item',
                search= full_name
                )

            #response_exists = requests.get('https://www.wikidata.org/w/api.php?', params_name).json() 
            response_exists = requests.get('https://test.wikidata.org/w/api.php?', params_name).json() 
            try:
                #if there is result returned, do not run bot, page already exists
                output = response_exists.get('search')[0]['id']
                
            except:
                #if there is no q id returned run the bot, to create a page
                mypywikibot(wiki_property_ids, store_values_dict, fixed_identifiers, language_tag)

        except:
            pass



if __name__ == "__main__":
    main() 